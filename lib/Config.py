import os.path
import json
from collections import OrderedDict


class Config(object):
    data = None

    @staticmethod
    def __load_once():
        """ Load config data from file to Config.data variable once """
        if Config.data is not None:
            return
        config_filename = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/config.json'
        with open(config_filename) as config_file:
            Config.data = json.load(config_file, object_pairs_hook=OrderedDict)

    @staticmethod
    def get(path, fallback=None):
        """ Get config value by the dots-separated keys path (like 'db.user') """
        Config.__load_once()
        keys = path.split('.')
        value = Config.data
        for key in keys:
            if key in value:
                value = value[key]
            else:
                return fallback
        return value

    @staticmethod
    def old_get(section, key=None, fallback=None):
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
