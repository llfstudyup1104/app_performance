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