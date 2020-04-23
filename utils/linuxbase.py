import paramiko
import re
import traceback
import subprocess
import os, sys
import select
import tty
import time
import termios
from loguru import logger
from stat import S_ISDIR as isdir


class LinuxDevNetConnection(object):
    def __init__(self, host, user, password, port=22):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.ssh_obj = None

    def __del__(self):
        self.close()

    def _connect_ssh(self, timeout=10, banner_timeout=None):
        ret = None
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

        for _ in range(0, 3):
            try:
                ssh.connect(hostname=self.host,
                            username=self.user,
                            password=self.password,
                            timeout=timeout,
                            banner_timeout=banner_timeout)
                tr = ssh.get_transport()
                tr.set_keepalive(1)
                logger.debug(
                    f"connected to remote host({self.user}:{self.password}@{self.host}:{self.port})"
                )
            except Exception as err:
                logger.info(
                    "connect remote host({0}:{1}@{2}:{3}) err by {4}.".format(
                        self.user, self.password, self.host, self.port, err))
            else:
                ret = ssh
                break
        return ret

    def connect(self, timeout=10, banner_timeout=None):
        if not self.ssh_obj:
            self.ssh_obj = self._connect_ssh()

    def reconnect(self):
        if not self.ssh_obj:
            self.close()
            self.connect()

    def close(self):
        if self.ssh_obj:
            self.ssh_obj.close()
            # del self.ssh_obj, stdin, stdout, stderr
            self.ssh_obj = None
            logger.debug(
                f"disconnected to remote host({self.host}:{self.port})")

    def send_command(self, command, timeout=20):
        try:
            stdin, stdout, stderr = self.ssh_obj.exec_command(command,
                                                              timeout=timeout)
            ret = stdout.read().decode() + stderr.read().decode()
            logger.debug('execute command({0}), return: {1}'.format(
                command, ret))
        except Exception as err:
            logger.info('exexcution command({0}) err by {1}\n{2}'.format(
                command, traceback.format_exc(), err))
            ret = None
        return ret

    def check_ssh(self):
        res = self.send_command('echo hello!')
        if res:
            ret = True if 'hello' in res else False
            logger.info("SSH connection is successful!")
        else:
            ret = None
        if not ret:
            logger.info("ssh failed: cannot connect to device {0}".format(
                self.host))
        return ret

    def check_connection(self):
        ret = None
        cmd = f'ping -c 1 -t 1 -s 1 {self.host}'
        response = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            shell=True).communicate(timeout=30)[0].decode(
                sys.getdefaultencoding(),
                errors='replace').encode().decode('utf-8', errors='replace')
        # print("=====" + response + "=====")
        # print(type(response))
        # print(len(response))
        if 'ttl=' in response.lower():
            logger.debug("ping succeeded for {0}".format(self.host))
            ret = True
        else:
            logger.info("ping failed: cannot connect to device {0}".format(
                self.host))
            ret = False
        return ret

    def check_connection02(self):
        ret = None
        cmd = f'ping -c1 -t1 -s1 {self.host}'
        response = os.popen(cmd).readlines()
        for line in response:
            if 'ttl' in line:
                # logger.debug("ping succeeded for {0}".format(self.host))
                ret = True
                break
            else:
                # logger.info("ping failed: cannot connect to device {0}".format(self.host))
                ret = False
                continue
        return ret

    def xshell_tranport(self):
        '''
        实现一个xshell登录系统的效果，登录到系统就不断输入命令同时返回结果
        支持自动补全，直接调用服务器终端

        '''

        # 建立一个socket
        trans = paramiko.Transport((self.host, self.port))
        # 启动一个客户端
        trans.start_client()

        # 如果使用rsa密钥登录的话
        '''
        default_key_file = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
        prikey = paramiko.RSAKey.from_private_key_file(default_key_file)
        trans.auth_publickey(username='super', key=prikey)
        '''
        # 如果使用用户名和密码登录
        trans.auth_password(username=self.user, password=self.password)
        # 打开一个通道
        channel = trans.open_session()
        # 获取终端
        channel.get_pty()
        # 激活终端，这样就可以登录到终端了，就和我们用类似于xshell登录系统一样
        channel.invoke_shell()

        # 获取原操作终端属性
        oldtty = termios.tcgetattr(sys.stdin)
        try:
            # 将现在的操作终端属性设置为服务器上的原生终端属性,可以支持tab了
            tty.setraw(sys.stdin)
            channel.settimeout(0)

            while True:
                readlist, writelist, errlist = select.select([
                    channel,
                    sys.stdin,
                ], [], [])
                # 如果是用户输入命令了,sys.stdin发生变化
                if sys.stdin in readlist:
                    # 获取输入的内容，输入一个字符发送1个字符
                    input_cmd = sys.stdin.read(1)
                    # 将命令发送给服务器
                    channel.sendall(input_cmd)

                # 服务器返回了结果,channel通道接受到结果,发生变化 select感知到
                if channel in readlist:
                    # 获取结果
                    result = channel.recv(1024)
                    # 断开连接后退出
                    if len(result) == 0:
                        print("\r\n**** EOF **** \r\n")
                        break
                    # 输出到屏幕
                    sys.stdout.write(result.decode())
                    sys.stdout.flush()
        finally:
            # 执行完后将现在的终端属性恢复为原操作终端属性
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

        # 关闭通道
        channel.close()
        # 关闭链接
        trans.close()

    def down_from_remote(self, remote_dir_name, local_dir_name):
        def _check_local_dir(self, local_dir_name):
            if not os.path.exists(local_dir_name):
                os.mkdirs(local_dir_name)
        def _down_from_remote(sftp_obj, remote_dir_name, local_dir_name):
            remote_file = sftp_obj.stat(remote_dir_name)
            if isdir(remote_file.st_mode):
                _check_local_dir(local_dir_name)
                logger.info('start download folder: ' + remote_dir_name)
                for remote_file_name in sftp_obj.listdir(remote_dir_name):
                    sub_remote = os.path.join(remote_dir_name, remote_file_name)
                    sub_remote = sub_remote.replace('\\', '/')
                    sub_local = os.path.join(local_dir_name, remote_file_name)
                    sub_local = sub_local.replace('\\', '/')
                    _down_from_remote(sftp_obj, sub_remote, sub_local)
            else:
                logger.info('start download file: ' + remote_dir_name)
                sftp.get(remote_dir_name, local_dir_name)
        
        sftp = self.ssh_obj.open_sftp()

        try:
            _down_from_remote(sftp, remote_dir_name, local_dir_name)
            ret = True
        except Exception as err:
            logger.warning(f'download file error by {err}\n{traceback.format_exc()}')
            ret = False
        sftp.close()
        return ret

    def put_to_remote(self, local_dir_name, remote_dir_name):
        def _put_to_remote(sftp_obj, local_dir_name, remote_dir_name):
            logger.info('start put file: ' + local_dir_name)
            sftp_obj.put(local_dir_name, remote_dir_name)
        sftp = self.ssh_obj.open_sftp()

        try:
            _put_to_remote(sftp, local_dir_name, remote_dir_name)
            ret = True
        except Exception as err:
            logger.warning(f'put file error by {err}\n{traceback.format_exc()}')
            ret = False
        sftp.close()
        return ret
    
    def uptime(self):
        '''
        [byton@doubled]: uptime
        05:59:57 up 13 days,  3:31,  load average: 11.51, 11.60, 11.78
        08:06:35 up 6 days, 44 min,  load average: 5.71, 5.92, 6.04
        15:44:29 up 1:37, 0 users
        '''
        upt = self.send_command('uptime')
        days = 0
        hours = 0
        minutes = 0
        try:
            extract_day = re.search("up (\d+) days", upt)
            if extract_day:
                days = int(extract_day.group(1))
            
            extract_time = re.search("\s+(\d+):(\d+),", upt)
            if extract_time:
                hours = int(extract_time.group(1))
                minutes = int(extract_time.group(2))
            
            extrac_time = re.search("\s+(\d+) min,", upt)
            if extract_time:
                minutes = int(extract_time.group(1))
            
            total_seconds = ((days * 24 +hours) * 60 + minutes) * 60
        except Exception as err:
            logger.error(f"convert uptime from '{upt}' error by {err}")
            total_seconds = None
        return total_seconds
    
    def send_interactive_command(self, command, prom='#', timeout= 120):
        ch = self.ssh_obj.invoke_shell()
        ch.settimeout(5)
        ch.send(command)
        ret = False
        rst = ''
        s_time = time.time()
        while True:
            time.sleep(0.2)
            try:
                tmp = ch.recv(1024)
            except Exception as err:
                logger.warning(
                    f'Recevie promt error by {err}\n{rst}')
                # break
            rst += tmp.decode('utf-8')
            if prom in rst:
                ret = True
                break
            elif (time.time() - s_time) > float(timeout):
                logger.info(
                    'Wait promt({0}) timeout({1}s)'.format(prom, timeout))
                break
        ch.close()
        logger.debug('output after input {0}: {1}'.format(command, rst))
        return rst

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
        self.tmp_log_path = "/var/file.txt"
        self.send_command(f"rm -f {self.tmp_log_path}")
        bl_path = '/var/log/bytonlogs/slog2'
        if rep:
            cmd = f"tail -f {bl_path} |grep -E '{rep}' > {self.tmp_log_path} &\r"
        else:
            cmd = f"tail -f {bl_path} > {self.tmp_log_path} &\r"
        ret = self.send_interactive_command(cmd)
        self.use_tmp_log = True if ret is not None else False
        return ret


if __name__ == '__main__':
    tk = LinuxDevNetConnection(host='192.168.111.60',
                               user='root',
                               password='')
    tk.connect()
    
    reg = 'SLOG2_INFO'

    start_time = time.time()
    print('Action: {}'.format(start_time))

    if tk.start_capture_byton_qnx_log(reg):
        end_time = time.time()
        print('End: {}'.format(end_time))
