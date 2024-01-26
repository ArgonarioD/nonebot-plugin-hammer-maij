from typing import Union, Annotated

from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot_plugin_hammer_core.util.message_factory import reply_text

from .. import group_mapping, random_command_start
from ..http.http_client import client

configure_group = on_command('maij.config', permission=SUPERUSER, block=True, force_whitespace=True)
disable_group = on_command('maij.disable', permission=SUPERUSER, block=True, force_whitespace=True)

__config_command_lint = f"本指令格式为{random_command_start}maij.config <城市名> [目标群号...]。"
__disable_command_lint = f"本指令格式为{random_command_start}maij.disable [目标群号...]。"


@configure_group.handle()
async def handle_configure_group(
        event: Union[MessageEvent, GroupMessageEvent],
        args: Annotated[Message, CommandArg()]
):
    arg_list = str(args).split(' ')
    if len(arg_list) == 0 or (len(arg_list) == 1 and arg_list[0] == ''):
        await configure_group.finish(reply_text(__config_command_lint, event))
    target_location = arg_list[0].strip()
    groups: list[int] = []
    for arg in arg_list[1:]:
        try:
            groups.append(int(arg))
        except ValueError:
            await configure_group.finish(reply_text(__config_command_lint, event))
    if len(groups) == 0:
        if not isinstance(event, GroupMessageEvent):
            await configure_group.finish(reply_text("请在群内使用本指令或使用指令参数指定群号。", event))
        groups.append(event.group_id)

    data = (await client.get(url="/city")).json()
    city_available = False
    for d in data:
        if d['name'] == target_location:
            city_available = True

    if not city_available:
        await configure_group.finish(reply_text(f"Hammer-MaiJ API暂不支持城市：{target_location}。", event))

    group_strs: list[str] = []
    for group_id in groups:
        group_strs.append(f'群{group_id}')
        group_mapping[group_id] = target_location

    group_mapping.write_to_disk()
    await configure_group.finish(reply_text(f"成功将 {'，'.join(group_strs)} 的地区设置为 {target_location}。", event))


@disable_group.handle()
async def handle_disable_group(
        event: Union[MessageEvent, GroupMessageEvent],
        args: Annotated[Message, CommandArg()]
):
    arg_list = str(args).split(' ')
    groups: list[int] = []
    for arg in arg_list:
        try:
            groups.append(int(arg))
        except ValueError:
            await configure_group.finish(reply_text(__disable_command_lint, event))
    if len(groups) == 0:
        if not isinstance(event, GroupMessageEvent):
            await configure_group.finish(reply_text("请在群内使用本指令或使用指令参数指定群号。", event))
        groups.append(event.group_id)

    group_strs: list[str] = []
    for group_id in groups:
        group_strs.append(f'群{group_id}')
        del group_mapping[group_id]

    group_mapping.write_to_disk()
    await configure_group.finish(reply_text(f"成功删除 {'，'.join(group_strs)} 的地区设置。", event))
