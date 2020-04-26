#-*- coding: utf-8 -*-

import configparser
from pathlib import Path, PurePath
from loguru import logger
import os
import traceback

project_folder = Path(os.path.dirname(__file__))
config_file = Path.joinpath(project_folder.parent, 'config/settings.ini')

class ConfigUtil(object):
    def __init__(self, filename):
        self.config = configparser.ConfigParser()
        self.filename = filename

    def read(self, filename):
        """
        读取配置文件
        :param filename: 配置文件路径
        """
        self.config.read(self.filename, encoding="utf-8-sig")
    
    def get(self, _options, _section='db'):
        """
        获取某个section下option的值
        :param _options: option
        :param _section: section
        """
        try:
            value = self.config.get(section=_section, option=_options)
        except Exception as e:
            print(f"No value for option {_options}")
            value = None
        return value

    def get_options_key_value(self, _section):
        """
        以列表(name, value)形式返回section中的每个值
        :param _section: 某个section
        :return list[turple(key, value)]
        """
        return self.config.items(_section)

    def get_all_section(self):
        """
        获取所有section
        """
        return self.config.sections()

    def get_options_by_section(self, _section):
        """
        获取section下所有可用的options
        """
        keys = self.config.options(_section)
        return keys
    
    def assert_section_in_config(self, _section):
        """
        判断section是否存在
        :param _section: 需要判断的section
        """
        return _section in self.config
    
    def assert_options_in_section(self, _section, _options):
        """
        判断options是否存在某个section中
        :param _section: section
        :param _options: 需要判断的options的key
        """
        return _options in self.config[_section]
        
    def set_config_value(self, section, option, value):
        try:
            if not self.config.has_section(section):
                self.config.add_section(section)
    
            self.config.set(section, option, value)
            
            with open(self.filename, 'w+') as configfile:    
                self.config.write(configfile)
        except:
            logger.error(traceback.format_exc())
            logger.error("saving configuration failed")


def main():
    configUtil = ConfigUtil(config_file)
    configUtil.read(config_file)
    print(configUtil.get("username"))
    print(configUtil.get_all_section())
    print(configUtil.assert_section_in_config("server"))
    print(configUtil.get_options_by_section("es"))
    print(configUtil.assert_options_in_section("es", "username"))
    print(configUtil.get_options_key_value("es"))
    configUtil.set_config_value('server', 'login', 'root')


if __name__ == '__main__':
    main()