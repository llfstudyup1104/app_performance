import configparser
from pathlib import Path, PurePath
from loguru import logger
import os

project_folder = Path(os.path.dirname(__file__))
config_file = Path.joinpath(project_folder.parent, 'config/settings.ini')    
config = configparser.ConfigParser()

def config_read(st_num):  
    try:
        config.read(config_file, encoding="utf-8-sig")
    except Exception as e:
        logger.info("The file not exist")
        print(e)
    else:     
        # 获取所有section节点信息，返回结果为列表
        section = config.sections()
        print(f'Sections: {section}')
        #显示section[st_num]下的所有option信息
        options = config.options(section[st_num])
        print(f'options: {options}')
        #显示section[st_num]下的所有key，value值
        items_section = config.items(section[st_num])
        print(f'Items in section 0 is {items_section}')
        for k, v in items_section:
            print('key = {0}, value = {1}'.format(k, v))

def get(_options, _section='db'):
        """查"""
        try:
            value = config.get(section=_section, option=_options)
        except Exception as e:
            print(f"No value for option {_options}")
            value = None
        return value

def config_add():
    """增"""
    with open(config_file, 'a+') as f:
        config.add_section('es')
        config.set('es', 'username', 'root')
        config.set('es', 'passwd', 'byton[]\\')
        config.set('es', 'host', '10.13.3.92')
        config.write(f)

def config_del():
    """删"""
    try:
        config.read(config_file, encoding="utf-8-sig")
    except Exception as e:
        logger.info("The file not exist")
        print(e)
    else:
        #删除一个option
        config.remove_option('db', 'host')
        #删除section
        config.remove_section('es')
        
        with open(config_file, 'w') as f:
            config.write(f)

def config_update():
    """改"""
    config.read(config_file, encoding="utf-8-sig")
    sections = config.sections()
    print(sections)
    for section in sections:
        if section == 'db':
            config.set(section, 'username', 'byton')
            with open(config_file, 'w') as f:
                config.write(f)
            break
    

if __name__ == '__main__':
    config_read(1)
    # config_add()
    # config_del()
    # config_update()
    print(config.get(section='es', option='username'))


