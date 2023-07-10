from nonebot.adapters.onebot.v11 import GroupMessageEvent, GROUP_MEMBER, Bot, Message
from nonebot.params import CommandArg
from nonebot.plugin.on import on_command
from nonebot_plugin_hammer_core.util.message_factory import reply_text

from ..maij_config import plugin_config
from ..const import consts
from ..http.http_client import client
from ..http.http_utils import json_dict_from_response

configure_group = on_command('maij.设置本群地区')  # /maij.设置本群地区 <省市名>


@configure_group.handle()
async def handle_configure_group(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    if await GROUP_MEMBER(bot, event) and event.user_id != 739062975:
        await configure_group.finish(reply_text('您没有足够的权限执行该指令。', event))

    target_location = args.extract_plain_text().strip()
    response = client.get(url=f'{consts.API_URL}/place/supported')
    data = json_dict_from_response(response)
    if len(list(filter(lambda l: l['cityName'] == target_location, data['records']))) == 0:
        await configure_group.finish(reply_text('Hammer-MaiJ API暂不支持本城市。', event))

    plugin_config.group_location[event.group_id] = target_location
    plugin_config.write_to_disk()
    await configure_group.finish(reply_text(f"成功将本群的地区设置为{target_location}。", event))
