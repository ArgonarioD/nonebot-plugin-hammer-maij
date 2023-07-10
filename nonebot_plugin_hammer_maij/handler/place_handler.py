from re import IGNORECASE
from typing import Annotated, Any

from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot
from nonebot.internal.matcher import Matcher
from nonebot.params import RegexGroup
from nonebot.plugin.on import on_regex, on_fullmatch
from nonebot_plugin_hammer_core.util.message_factory import reply_text

from .handle_utils import get_group_location, do_request, get_place_list_str, get_announcement_list_str
from ..const import consts
from ..data_classes import Place
from ..http.http_client import client
from ..http.http_utils import json_dict_from_response

maij = on_regex(r'(.+?)(j|jr|几|有?(几|多少)[人卡])$', flags=IGNORECASE)
put_maij = on_regex(r'(.+?)( ?([+-] ?[1-9][0-9]*卡)|(\+\+|--))$')
set_maij = on_regex(r'(.+?)( ?= ?(0|([1-9][0-9]*))卡)$')
place_asc_list = on_fullmatch('机厅列表')


@maij.handle()
async def handle_maij(
        matcher: Matcher,
        bot: Bot,
        event: GroupMessageEvent,
        r: Annotated[tuple[Any, ...], RegexGroup()]
):
    location = get_group_location(event.group_id)
    place_name = r[0].strip()

    ##########
    async def do():
        response = client.get(url=f'{consts.API_URL}/place/{location}/{place_name}')
        data = Place(**json_dict_from_response(response))
        if not data.updated:
            result = f'查询到{data.placeName}的卡数今天还没有被更新过。'
        else:
            result = f"查询到{data.placeName}的当前卡数为{data.cardCount}\n上次更新时间为{data.updateTime}"

        await matcher.send(
            reply_text(f"{result.strip()}\n\n{await get_announcement_list_str(bot, event, data.announcements)}".strip(),
                       event))

    ##########

    await do_request(matcher, event, place_name, do)


@put_maij.handle()
async def handle_put_maij(
        matcher: Matcher,
        bot: Bot,
        event: GroupMessageEvent,
        r: Annotated[tuple[Any, ...], RegexGroup()]
):
    location = get_group_location(event.group_id)
    place_name = r[0].strip()
    mutate_str = r[1].strip()
    if '++' in mutate_str:
        mutate_str = '+1卡'
    elif '--' in mutate_str:
        mutate_str = '-1卡'
    operate_count = int(mutate_str.replace(' ', '')[:-1])

    ##########
    async def do():
        response = client.put(url=f'{consts.API_URL}/place/{location}/{place_name}', json={
            "qqId": event.user_id,
            "qqGroupId": event.group_id,
            "operateCount": operate_count
        })
        data = Place(**json_dict_from_response(response))
        await matcher.send(
            reply_text(
                f'''成功在{data.placeName}的队伍中{"添加" if operate_count > 0 else "移除"}{abs(operate_count)}张卡
当前排卡数为{data.cardCount}

{await get_announcement_list_str(bot, event, data.announcements)}'''.strip(), event))

    ##########

    await do_request(matcher, event, place_name, do, handle_not_found=True)


@set_maij.handle()
async def handle_set_maij(
        matcher: Matcher,
        bot: Bot,
        event: GroupMessageEvent,
        r: Annotated[tuple[Any, ...], RegexGroup()]
):
    location = get_group_location(event.group_id)
    place_name = r[0].strip()
    operate_count = int(r[2].strip())

    ##########
    async def do():
        response = client.put(url=f'{consts.API_URL}/place/{location}/{place_name}/set', json={
            "qqId": event.user_id,
            "qqGroupId": event.group_id,
            "operateCount": operate_count
        })
        data = Place(**json_dict_from_response(response))
        await matcher.send(
            reply_text(f'''成功将{data.placeName}的卡数设置为{data.cardCount}张卡

{await get_announcement_list_str(bot, event, data.announcements)}'''.strip(), event))

    ##########

    await do_request(matcher, event, place_name, do)


@place_asc_list.handle()
async def handle_place_asc_list(
        matcher: Matcher,
        event: GroupMessageEvent,
):
    location = get_group_location(event.group_id)

    ##########
    async def do():
        response = client.get(url=f'{consts.API_URL}/place/list/{location}')
        data = json_dict_from_response(response)
        await matcher.send(
            reply_text(f'''自今日API重置后，{location}共有{data['total']}所机厅的卡数被更新过，按其当前卡数的正序、更新时间的倒序排列如下：
{get_place_list_str([Place(**place_dict) for place_dict in data['records']])}''', event))

    ##########

    await do_request(matcher, event, location, do)
