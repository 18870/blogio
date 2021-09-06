# -*- encoding=utf8 -*-

"""
copy from LmeSzinc/AzurLaneAutoScript module/config/config.py
"""

import codecs
import configparser
import copy

from module.config.update import get_config
from module.logger import logger


class Config:
    """
    Basic Config.
    """
    CONFIG_FILE = ''
    config = configparser.ConfigParser(interpolation=None)

    # Global
    PASSWORD = ''
    AES_KEY = '123456789abc'

    # Cookie
    PATH = '/'
    DOMAIN = '/'
    SAMESITE = None
    SECURE = True

    # Vaptcha
    VID = ''
    SERVER = ''
    SCENE = 1


    def merge(self, other):
        """
        Args:
            other (Config, Config):

        Returns:
            Config
        """
        config = copy.copy(self)
        for attr in dir(config):
            if attr.endswith('__'):
                continue
            if hasattr(other, attr):
                value = other.__getattribute__(attr)
                if value is not None:
                    config.__setattr__(attr, value)

        return config

    def load_config_file(self, name='config'):
        self.CONFIG_FILE = f'./config/{name}.ini'
        self.config = get_config(ini_name=name)
        self.load_from_config(self.config)
        self.config_check()

    def config_check(self):
        pass

    def save(self):
        self.config.write(codecs.open(self.CONFIG_FILE, "w+", "utf8"))

    def load_from_config(self, config):
        """
        Args:
            config(configparser.ConfigParser):
        """

        # Global
        option = config['Global']
        self.PASSWORD = option['password']
        self.AES_KEY = option['aes_key']

        # Cookie
        option = config['Cookie']
        self.PATH = option['path']
        self.DOMAIN = option['domain']
        self.SAMESITE = option['samesite']
        self.SECURE = to_bool(option['secure'])

        # Vaptcha
        option = config['Vaptcha']
        self.VID = option['VID']
        self.SERVER = option['server']
        self.SCENE = int(option['scene'])

    def __init__(self, ini_name='config'):
        """
        Args:
            ini_name (str): Config to load.
        """
        self.load_config_file(ini_name)


dic_bool = {
    'yes': True,
    'no': False,
    'True': True,
    'False': False,
}

def to_bool(string):
    return dic_bool.get(string, string)

def to_list(string):
    if string.isdigit():
        return None
    out = [int(letter.strip()) for letter in string.split(',')]
    return out



config = Config()