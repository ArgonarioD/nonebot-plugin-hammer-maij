from os import path

from nonebot_plugin_hammer_core.util.constant import ConstNamespace

consts = ConstNamespace.hammer_maij
consts.CONFIG_DIR = path.join('.', 'config', 'hammer', 'maij')
consts.CONFIG_PATH = path.join(consts.CONFIG_DIR, 'config.json')
consts.API_URL = 'https://api.hammer-hfut.tk:233/maij'
consts.PLUGIN_NAME = 'hammer-maij'
