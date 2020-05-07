import os
import re
import time
import logging
from datetime import datetime, timedelta
from icebot.utils.config import config
from icebot.utils.linuxbase import LinuxDevNetConnection


logger = logging.getLogger(__name__)


class PIC(LinuxDevNetConnection):
    DATA_RE = re.compile(r'^(\w+\s+\d{2})\s+\d{2}:\d{2}:\d{2}\.\d{3}')

    def __init__(self, hostname=None, user=None, password=None, port=None):
        config = config.Configure()
        if host is None:
            host = config.get_config_value('PIC', 'host')
        if user is None:
            user = config.get_config_value('PIC', 'user')
        if password is None:
            password = config.get_config_value('PIC', 'pwd')
        if port is None:
            port = config.get_config_value('PIC', 'port')
        
        super().__init__(host, user, password, port)
        self.reboot_no = 0
        self.previous_uptime = 0
        self.tmp_log_path = '/var/file.txt'
        self.use_tmp_log = None
        self._net_interface = config.get_config_value('PIC', 'net_interface')
        self._power_switch_module = config.get_config_value('TestBench', 'power_switch_module')
        self._power_measure_module = config.get_config_value('TestBench', 'power_measure_module')
        self._ict = ICTDP(config.get_config_value('ICT', 'url'),
                            config.get_config_value('ICT', 'user'),
                            config.get_config_value('ICT', 'password'))
        self._power_slot = config.get_config_value('ICT', 'pic_slot')
        self.power_relay_obj = Relay()
        self.power_relay_port = config.get_config_value('Relay', 'port')
        self.power_relay_slot = config.get_config_value('Relay', 'pic')
    
    def hard_reboot(self, delay=5):
        if self._power_measure_module == 'ict':
            self._ict.set_slot_switch(self._power_slot, 'Off')
            time.sleep(delay)
            self._ict.set_slot_switch(self._power_slot, 'On')
        else:
            como = self.power_relay_obj.init_board(self.power_relay_port)
            self.power_relay_obj.switch_off(self.power_relay_slot)
            time.sleep(delay)
            self.power_relay_obj.switch_on(self.power_relay_slot)
            como.close()
    
    @property
    def power_info(self):
        if self._power_measure_module == 'ict':
            power_info = self._ict.get_slot_status(self._power_slot)
            return (float(power_info[0]) if power_info[0] else 0.0,
                    float(power_info[1]) if power_info[1] else 0.0)
        else:
            return 0.0, 0.0
    
    def connect(self):
        super().connect(timeout=15, banner_timeout=150)
        self.send_command('mkdir /root')
    
    @property
    def software_version(self):
        v = self.send_command('byton_info.sh')
        if v:
            m = re.search(r'Byton Build Name \[([^\]]+)\].*\n.*Byton Build Time \[([^\]]+)\]', v)
            build_name = m.group(1) if m else ''
            logger.info(f'get pic version is {build_name}')
            return build_name
        return ''
    
    @property
    def net_stats(self):
        net_stats = dict(bytes_rx=0, packets_rx=0, bytes_tx=0, packets_tx=0):
        command_net_stats = 'nicinfo -s' + self._net_interface
        res = self.send_command(command_net_stats)
        if res:
            m = re.search(
                r'Packets Transmitted OK \.* ([0-9]+)\s[\S\s]*Bytes Transmitted OK \.* ([0-9]+)\s[\S\s]*Packets Received OK \.* ([0-9]+)\s[\S\s]*Bytes Received OK \.* ([0-9]+)', res)
            net_stats['bytes_rx'] = m.group(4) if m else ''
            net_stats['packets_rx'] = m.group(3) if m else ''
            net_stats['bytes_tx'] = m.group(2) if m else ''
            net_stats['packets_tx'] = m.group(1) if m else ''
        return net_stats
    
    @property
    def num_of_reboot(self):
        upt = self.uptime

        if upt is not None and upt < self.previous_uptime:
            self.reboot_no = self.reboot_no +1 
        
        if upt is not None:
            self.previous_uptime = upt
        
        return self.reboot_no
    
    @property
    def top_info(self):
        cpu_usr, cpu_kernel = 0, 0
        mem_total, mem_free = 0, 0
        proc_min, proc_max, proc_avg = 0, 0, 0
        itop = self.send_command('top -i 1 -b', 120)
        rea = re.search(
            "CPU states: (\d+.*\d*)% user, (\d+.*\d*)%[\s\S]+Memory: (\d+[MmKk]) total,[\s]+(\d+[MmKk]) avail,[\s\S]+"\
                "Processes:\s+(\d+)\s+(\d+)\s+(\d+)[\s\S]+Threads:\s+(\d+)\s+(\d+)\s+(\d+)", itop)
        if rea:
            cpu_usr, cpu_kernal = float(rea.group(1)), float(rea.group(2))
            mem_total, mem_free = self.change_memort_to_kb(rea.group(3)), self.change_memort_to_kb(rea.group(4))
            proc_min, proc_max, proc_avg = int(rea.group(5)), int(rea.group(6)), int(rea.group(7))
        
        return cpu_usr, cpu_kernal, mem_total, mem_free, proc_min, proc_max, proc_avg

    @property
    def disk_info(self):
        idisk = self.send_command('df -h', 120)
        ret = dict()
        for line in idisk.split('\n'):
            tmp = re.search('(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s*', line)
            if tmp:
                ret[tmp.group(6)] = {'size': tmp.group(2), 'used': tmp.group(3), 'available': tmp.group(4),
                                'use%': tmp.group(5).replace('%', ''), 'disk': tmp.group(1)}
        return ret

    @property
    def process_info(self):
        prc_dict = dict()
        ihogs = self.send_command('hogs -i 1', 120)
        for line in ihogs.split('\n'):
            tmp = re.search('(\d+)\s+(\S+)\s+(\d+)\s+(\d+)%\s+(\d+)%\s+(\d+[MmKk])\s+(\d+)%', line)
            if tmp:
                prc_dict[tmp.group(2)] = {'pid': tmp.group(1), 'msec': tmp.group(3), 'pids': tmp.group(4),
                                'sys%': tmp.group(5), 'mem': self.change_memory_to_kb(tmp.group(6)), 'mem%': tmp.group(7)}
        
        return prc_dict
    
    @property
    def system_temp(self):
        tmp = self.send_command('cat /var/pps/IceDeviceManager/Sensor/temp_sensor')
        m = re.search(r'tsens0_temp:n:(\d+).*', tmp)
        sys_temp = m.group(1) if m else 0
        return sys_temp

    @property  
    def byton_log_path(self):
        v = self.software_version
        try:
            bd_num = int(v.split('_')[2])
            bd_ver = float(v.split('_')[0][3:])
        except Exception as err:
            logger.info(f'get build num err by {err}')
            bd_num = 999
            bd_ver = 0.1
        if bd_ver >= 0.5:
            if bd_num < 699:
                bl_path = '/var/log/slog2'
            else:
                bl_path = '/var/log/bytonlogs/slog2'
        else:
            bl_path = '/var/log/bytonlogs/slog2'
        
        return bl_path
    
    def start_capture_byton_qnx_log(self, rep=None):
        self.close()
        self.connect()
        self.send_command(f'rm -f {self.tmp_log_path}')
        bl_path = self.byton_log_path
        if rep:
            cmd = f "tail -f {bl_path} | grep -E '{rep}' > {self.tmp_log_path} &\r"
        else:
            cmd = f"tail -f {bl_path} > {self.tmp_log_path} &\r"
        ret = self.send_interactive_command(cmd)
        self.use_tmp_log = True if ret is not None else False
        return ret
    
    def get_log(self, rep=None, line_count=None, encoding='utf-8', local_log_dir=""):
        try:
            os.remove(local_log_dir+'pic_slog2')
        except Exception as err:
            logger.info(f'remove slog2 file error by {err}')
        if self.use_tmp_log:
            self.down_from_remote(self.tmp_log_path, local_log_dir+'pic_slog2')
            self.close()
            self.connect()
            self.use_tmp_log = False
        else:
            bl_path = self.byton_log_path
            self.down_from_remote(bl_path, local_log_dir+'pic_slog2')
        with open(local_log_dir+'pic_slog2', mode='rb') as f:
            f.seek(0, io.SEEK_END)
            file_size = f.tell()
            if file_size == 0:  # or line_count <= 0:
                return ""
            lines = []
            prev_char = None
            curr_line = bytearray()
            chars_read = 0
            f.seek(-1, io.SEEK_END)
            while True:
                curr_char = f.read(1)
                chars_read += 1
                if curr_char not in (b'\n', b'\r') or chars_read == file_size:
                    curr_line.extend(curr_char)
                if curr_char == b'\n' or (curr_char == b'\r' and not prev_char == b'\n') or chars_read == file_size:
                    curr_line.reverse()
                    tmp = bytes(curr_line).decode(encoding)
                    if rep:
                        if re.search(rep, tmp):
                            lines.append(tmp)
                        else:
                            logger.debug('log: {0} not match'.format(tmp))
                    else:
                        lines.append(tmp)
                    curr_line.clear()
                if line_count:
                    if len(lines) == int(line_count):
                        break
                if chars_read == file_size:
                    break
                f.seek(-2, io.SEEK_CUR)
                prev_char = curr_char
            lines.reverse()
        logger.info('Get {0} lines of log'.format(len(lines)))
        return '\n'.join(lines)
    
    def find_log(self, alog, olog):
        ret = {}
        if isinstance(olog, str):
            oolog = [olog]
        else:
            oolog = olog.copy()
        j = oolog.pop(0)
        for i in alog.split('\n'):
            for j in i:
                ret[j] = i
                logger.info('match log({0}): {1}'.format(ret[j], i))
                if oolog:
                    j = oolog.pop(0)
                else:
                    break
        if len(ret) != len(oolog):
            logger.info('can not find log')
        
        return ret
    
    def get_log_time(self, olog):
        m = self.DATA_RE.match(olog)
        if m:
            ret = m.group()
            logger.info("find log time: {0}".format(ret))
        else:
            ret = ''
            logger.info("can not find log time")
        return ret
    
    def get_log_difftime(self, t1, t2):
        dd1 = datetime.strptime(t1, "%b %d %H:%M:%S.%f")
        dd2 = datetime.strptime(t2, "%b %d %H:%M:%S.%f")
        ret = (dd2 - dd1).total_seconds
        logger.info("diff time: {0}".format(ret))
        return ret
    
    def clear_log(self):
        bl_path = self.byton_log_path
        return self.send_command(f'cat /dev/null > {bl_path}')
    
    def set_time(self):
        st = 'date {0}'.format(datetime.utcnow().strftime(
            '%m%d%H%M%Y.%S'))
        self.send_command(st)
        dt = self.send_command('date')
        logger.info(f'set PIC QNX system time to {dt[:-1]} by {st}')
        return dt[:-1]
    
    def sync_time_by_ntp(self, ntp_srv='pool.ntp.org'):
        st = self.send_command(f'ping -c 3 {ntp_srv}')
        if 'ttl=' not in st:
            logger.info(f"ping {ntp_srv} error: {st}")
        self.send_command('ntpd stop')
        for _ in range(0, 30):
            st = self.send_command('slay ntpd')
            time.sleep(0.1)
            if 'Unable to find process' in st:
                break
        st = self.send_command(f'/usr/sbin/ntpdate {ntp_srv}')
        if 'the NTP socket is in use, exiting' in st:
            logger.info(f'Sync PIC QNX system time error. {st}')
        self.send_command('ntpd restart')
        dt = self.send_command('date')
        logger.info(f'Sync PIC QNX system time to {dt[:-1]} with {ntp_srv}')
        return dt[:-1]
    
    def get_time(self):
        dt = self.send_command('date -t')
        dt = datetime.utcfromtimestamp(float(dt)).strftime("%b %d %H:%M%S.%f")
        logger.info(f'PIC QNX system time: {dt}')
        return dt
    
    def reboot(self):
        return self.send_interactive_command('reset\r', 'Shutdown complete')
    
    def qnx_screeshot(self, filename='screenshot.png'):
        self.send_command('cd /var; rm -rf *.png')
        self.send_command('cd /usr/sbin; ./qtscreen_capture.sh; sleep 0.5')
        scnm = self.send_command(
            'ls /var | grep -E "Dashboard_Screen_Shot"')[:-1]
        logger.info(f'get screenshot file name on QNX is: {scnm}')
        if not self.down_frome_remote(f'/var/{scnm}', filename):
            filename = False
        return filename
    
    def get_errortime_period(self, time_error, period):
        period_time = []
        dt = datetime.strptime(time_error, "%Y-%m-%d-%H:%M:%S")
        logger.info(f'get datetime {time_error}')
        dt1 = dt - timedelta(minutes=period)
        dt2 = dt + timedelta(minutes=period + 1)
        period_time.append(dt1)
        period_time.append(dt2)

        for i in range(2):
            period_time[i] = period_time[i].strftime("%b %d %H:%M")
        logger.info(f'target period time: {dt1}, {dt2-timedelta(minutes=1)}')
        return period_time
    
    def downlog_from_remote(self):
        logger.info("start downloading log from remote")
        logpath_remote = self.byton_log_path
        logpath_local = os.path.expanduser('~')
        logpath_local_file = []
        logpath_remote_file = [f"{logpath_remote}_9",
                                f"{logpath_remote}_8",
                                f"{logpath_remote}_7",
                                f"{logpath_remote}_6",
                                f"{logpath_remote}_5",
                                f"{logpath_remote}_4",
                                f"{logpath_remote}_3",
                                f"{logpath_remote}_2",
                                f"{logpath_remote}_1",
                                logpath_remote]
        for i in range(10):
            local_file = f"{logpath_local}/slog2_{str(i)}"
            logpath_local_file.append(local_file)
            try:
                os.remove(local_file)
            except Exception as err:
                logger.info(f"remove failed: {err}")
            self.downlog_from_remote(logpath_remote_file, local_file)
            logger.info(f"downloading success, logpath_local_file: {local_file}")
        return logpath_local_file

    def get_period_log(self, time_error, logpath_local_file, period=2):
        period_time = self.get_errortime_period(time_error, period)
        time_now = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
        error_log = os.path.expanduser('~') + f"/error_log_{time_now}.txt"
        logger.info(f"error_log: {error_log}")
        flog = open(erro_log, 'a+')
        st = False
        ed = False
        for path in logpath_local_file:
            f = open(path, 'r', encoding='utf-8')
            logger.info(f"open files: {path}")
            for i in f.readlines():
                if period_time[0] in i:
                    flog.writelines(i)
                    st = True
                elif period_time[1] in i:
                    ed = True
                    logger.info(f"end log path: {path}")
                    break
                elif st == True:
                    flog.writelines(i)
            if ed == True:
                break
            f.close()
        flog.close()
        return error_log
    
    def ota_update(self, package_path):
        package_name = package_path.split('/')[-1]
        self.send_command('rm -f /data/*.tar.gz')
        result = self.put_to_remote(package_path, f"/data/{package_name}")
        if result != True:
            logger.warning(f'upload ota file ({package_path}) to dut failed')
            return None
        reps = self.send_interactive_command
            f'ota-update /data/{package_name}\r', 'Reset system', 2000)
        if 'Reset system' in reps:
            return None
        else:
            return False


        





        
    

