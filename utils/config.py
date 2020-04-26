# -*- coding: utf-8 -*-
__version__ = '0.0.1'

import configparser as ConfigParser
import logging  
import os
import traceback

logger = logging.getLogger(__name__)

class Configure(object):
    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        self.configPath = os.path.join(os.path.dirname(__file__), '../config/settings.ini')
        self.config.read(self.configPath)
    
    def get_config_value(self, section, option):
        try:
            return self.config.get(section, option)
        except:
            logger.error(traceback.format_exc())
            return None
        
    def set_config_value(self, section, option, value):
        try:
            for item in self.config.sections():
                for subItem in self.config.options(item):
                        self.config.set(item, subItem, self.get_config_value(item, subItem))
            
            if not self.config.has_section(section):
                self.config.add_section(section)
    
            self.config.set(section, option, value)
            
            with open(self.configPath, 'w') as configfile:    
                self.config.write(configfile)
        except:
            logger.error(traceback.format_exc())
            logger.error("saving configuration failed")


if __name__ == '__main__':
    cf = Configure()
    print(cf.get_config_value("app", "page"))
    print(cf.get_config_value("app", "activity"))
