import nonebot
from nonebot import get_driver, require

require('nonebot_plugin_localstore')

import nonebot_plugin_localstore as store

from .group_mapping import GroupMappingFile
from .config import Config

__plugin_meta__ = nonebot.plugin.PluginMetadata(
    name='hammer-maij',
    description='Nonebot2 对接 MaiJ API 3.0',
    usage='''机厅列表 查询本城市中自当日API重置后所有更新过卡数的机厅按卡数正序排列、更新时间倒序排列的列表
<机厅名称>j/jr/几/几人/几卡/有几人/有多少人/有几卡 查询指定机厅中的卡数
<机厅名称>+/-<数字>卡 为指定机厅添加/移除指定卡数
<机厅名称>++/-- 为指定机厅添加/移除一张卡
<机厅名称>[=]<数字>卡 将指定机厅设置为指定卡数（如果机厅名称的最后一个字符是数字，必须要在机厅名称后添加等号或空格）
<机厅名称>[都]有谁 查询指定机厅今日的卡数变更记录
<机厅名称>[的本]周[的]出勤情况 发送由API记录的指定机厅七天以内的出勤情况折线图

发[一](条|个)公告 <地名> <内容> - 发送一条公告，内容支持换行，在不续期的情况下一周后自动删除
续[一](续|发|下)公告 <地名> <公告ID> - 为指定公告续期一周
删[一](条|个)公告 <地名> <公告ID> - 删除指定的公告，只有发布者可以删除
注：API管理员会不定时检查公告内容，如有违规内容（如色情内容、商业性质广告）或无意义灌水会删除，严重者禁用本功能使用权限。

本插件使用的查卡API为由 ArgonarioD 提供的开放API，欢迎接入本服务与其他玩家共享信息！文档链接https://docs.argonariod.tech/maij/''',
    supported_adapters={"~onebot.v11"},
    extra={
        "version": "2.0.0",
    }
)

driver = get_driver()
global_config = driver.config
config = Config.parse_obj(global_config)
group_mapping = GroupMappingFile(store.get_data_file('nonebot_plugin_hammer_maij', 'group_mapping.json'))
plugin_cache_dir = store.get_cache_dir('nonebot_plugin_hammer_maij')

for s in global_config.command_start:
    random_command_start = s
    break

from .handler import *
