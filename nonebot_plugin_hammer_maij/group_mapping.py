import json
import pathlib

from nonebot.exception import FinishedException


class GroupMappingFile:
    def __init__(self, file: pathlib.Path):
        self.file = file
        self.group_mapping = dict[int, str]()
        if not self.file.exists():
            self.file.parent.mkdir(parents=True, exist_ok=True)
            with self.file.open(mode='w') as f:
                json.dump({}, f)
        else:
            self.__load()

    def __load(self):
        with self.file.open(mode='r') as f:
            group_mapping_data = json.load(f)
            # 需要手动添加，否则key会变成字符串
            for group_id, city_name in group_mapping_data.items():
                self.group_mapping[int(group_id)] = city_name

    def write_to_disk(self):
        with self.file.open(mode='w') as f:
            json.dump(self.group_mapping, f, ensure_ascii=False)

    def __getitem__(self, item: int):
        if item not in self.group_mapping:
            raise FinishedException
        return self.group_mapping[item]

    def __setitem__(self, key: int, value: str):
        self.group_mapping[key] = value

    def __delitem__(self, key: int):
        del self.group_mapping[key]
