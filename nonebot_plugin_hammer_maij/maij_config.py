import json

from nonebot import require

require('nonebot_plugin_localstore')
import nonebot_plugin_localstore as store
from json import JSONEncoder

from .const import consts

key_group_location = 'group_location'
config_file_name = 'config.json'


class Config:
    group_location = dict[int, str]()

    def __init__(self):
        self.__config_file = store.get_config_file(consts.PLUGIN_NAME, config_file_name)
        if not self.__config_file.exists():
            self.__config_file.parent.mkdir(parents=True, exist_ok=True)
            with self.__config_file.open('w') as f:
                json.dump({key_group_location: {}}, f)
        self.load()

    def load(self):
        with self.__config_file.open() as f:
            config_data = json.load(f)
            # 需要手动添加，否则key会变成字符串
            for group_id, locate in config_data[key_group_location].items():
                self.group_location[int(group_id)] = locate

    def write_to_disk(self):
        with self.__config_file.open('w') as f:
            json.dump(self, f, cls=ConfigEncoder, ensure_ascii=False)


class ConfigEncoder(JSONEncoder):
    def default(self, o: Config):
        return {key_group_location: o.group_location}


plugin_config = Config()
