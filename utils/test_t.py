import configparser
import os


class ConfigUtil(object):
    def __init__(self, filename):
        self.filename = filename
        self.config = None

    def read_config(self):
        config_t = configparser.ConfigParser()
        try:
            config_t.read(self.filename, encoding="utf-8-sig")
        except FileExistsError as err:
            print(f"Config file not found! The error is {err}")
        else:
            self.config = config_t
        return config_t
    
    @property
    def sections(self):
        if self.config is not None:
            value = self.config.sections()
        return value

    def get_options(self, _section):
        if self.config is not None:
            value = self.config.options(_section)
        return value

    def get_items(self, _section):
        if self.config is not None:
            items = self.config.items(_section)
        return items

    def get_option_key_value(self, _section, _key):
        if self.config is not None:
            res = self.get_items(_section)
            for k, v in res:
                if _key == k:
                    value = v
            return value

    def assert_key(self, _section, _key):
        options = self.get_options(_section)
        if _key not in options:
            print(f"The {_key} is not in section")
            return False


if __name__ == '__main__':
    filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            'config/settings_app.ini')
    config_u = ConfigUtil(filename)
    config_u.read_config()
    options = config_u.get_options('db')
    print(options)
    items = config_u.get_items('db')
    print(items)

    value = config_u.get_option_key_value('db', 'username')
    print(f"The value of username in db is: {value}")

    config_u.assert_key('db', 'username')