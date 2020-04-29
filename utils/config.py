# -*- coding: utf-8 -*-
__version__ = '0.0.1'

import configparser
import logging
import os
import traceback
import shutil

logger = logging.getLogger(__name__)


class Configure(object):
    def __init__(self):
        self.lib_config = configparser.ConfigParser()
        self.lib_config_path = os.path.join(os.path.dirname(__file__),
                                            '../config/settings.ini')
        self.lib_config.read_string(self._read_file(self.lib_config_path))

        self.ice_config = configparser.ConfigParser()
        self.ice_config_path = os.path.join(
            os.path.expanduser('~'), 'icebot.ini')
        if not os.path.exists(self.ice_config_path):
            shutil.copy(self.lib_config_path, self.ice_config_path)
            
        self.ice_config.read_string(self._read_file(self.ice_config_path))

    def _read_file(self, filename):
        with open(filename, 'r', encoding='utf-8-sig') as f:
            conf_str = f.read()
        return conf_str

    def get_config_value(self, section, option):
        try:
            val = self.ice_config.get(section, option, fallback=None)
            print(val)
            if val is None:
                logger.warning("Can not get config value from user config")
                lval = self.lib_config.get(section, option, fallback=None)
                if lval is not None:
                    self.set_config_value(section, option, lval)
                val = self.ice_config.get(section, option, fallback=None)
        except Exception as err:
            val = None
            logger.err(f'get config failed by {err}\n{traceback.format_exc()}')
        return val

    def set_config_value(self, section, option, value):
        try:
            if not self.ice_config.has_section(section):
                self.ice_config.add_section(section)
            self.ice_config.set(section, option, str(value))

            with open(self.ice_config_path, 'w') as f:
                self.ice_config.write(f)
        except Exception as err:
            logger.error(f'put file error by {err}\n{traceback.format_exc()}')
            logger.error(f"saving config failed! [{section}:{option}:{value}]")


if __name__ == '__main__':
    cf = Configure()
    print(cf.get_config_value("server", "ww"))
