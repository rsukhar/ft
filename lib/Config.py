import os.path
from configparser import ConfigParser, NoSectionError


class Config(object):
    data = None

    @staticmethod
    def __load_once():
        """ Load config data from file to Config.data variable once """
        if Config.data is not None:
            return
        parser = ConfigParser()
        config_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/config.ini'
        parser.read(config_file)
        Config.data = {}
        for section in parser.sections():
            Config.data[section] = {}
            for key, value in parser.items(section):
                Config.data[section][key] = value

    @staticmethod
    def get(section, key=None, fallback=None):
        """ Get the requested config value or section """
        Config.__load_once()
        if section not in Config.data:
            return fallback
        elif key is None:
            return Config.data[section]
        elif key not in Config.data[section]:
            return fallback
        else:
            return Config.data[section][key]
