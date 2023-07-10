import nonebot
from nonebot import get_driver

from .config import Config
from .const import consts
from .handler import *
from .maij_config import plugin_config

__plugin_meta__ = nonebot.plugin.PluginMetadata(
    name=consts.PLUGIN_NAME,
    description='Nonebot2对接MaiJ API',
    usage='''机厅列表 查询本城市中自当日API重置后所有更新过卡数的机厅按卡数正序排列、更新时间倒序排列的列表
<机厅名称>j/jr/几/几人/几卡/有几人/有多少人/有几卡 查询指定机厅中的卡数
<机厅名称>+/-<数字>卡 为指定机厅添加/移除指定卡数
<机厅名称>++/-- 为指定机厅添加/移除一张卡
<机厅名称>=<数字>卡 将指定机厅设置为指定卡数
<机厅名称>[都]有谁 查询指定机厅今日的卡数变更记录

发[一](条|个)公告 <地名> <内容> - 发送一条公告，内容支持换行，在不续期的情况下一周后自动删除
续[一](续|发|下)公告 <地名> <公告ID> - 为指定公告续期一周
删[一](条|个)公告 <地名> <公告ID> - 删除指定的公告，只有发布者可以删除
注：API管理员会不定时检查公告内容，如有违规内容（如色情内容、商业性质广告）或无意义灌水会删除，严重者禁用本功能使用权限。

本插件使用的查卡API为由Hammer提供的开放API，欢迎接入本服务与其他玩家共享信息！文档链接https://docs.hammer-hfut.tk:233/maij/''',
    extra={
        "version": "1.0.0",
    }
)

global_config = get_driver().config
config = Config.parse_obj(global_config)
