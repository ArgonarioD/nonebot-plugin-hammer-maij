from re import IGNORECASE
from typing import Annotated, Any

from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot
from nonebot.internal.matcher import Matcher
from nonebot.params import RegexDict
from nonebot.plugin.on import on_regex
from nonebot_plugin_hammer_core.util.message_factory import reply_text

from .handle_utils import do_request, announcement_list_str
from ..time_utils import format_time
from .. import group_mapping
from ..http.http_client import client
from ..http.http_models import PlaceCommon
from ..http.http_utils import json_dict_from_response

place_common_query = on_regex(r'^(?P<place>[^\s]+)(jr?|几|有?(几|多少)[人卡])$', flags=IGNORECASE)
place_update = on_regex(r'^(?P<place>[^\s]+)(((?P<expression1>[+＋=＝\-－]\s?\d+)\s?卡)|(?P<expression2>\+\+|--)\s?)$')
place_update_implicit = on_regex(r'^(?P<place>([^\s]*[^\s\d])|([^\s]+\s))\s?((?P<count>\d+)\s?卡)$', priority=100)


@place_common_query.handle()
async def handle_place_common_query(
        matcher: Matcher,
        bot: Bot,
        event: GroupMessageEvent,
        r: Annotated[dict[str, Any], RegexDict()]
):
    city_name = group_mapping[event.group_id]
    place_name = r['place'].strip()

    ##########
    async def do():
        response = await client.get(url=f'/place/{city_name}/{place_name}', params={'queryType': 'common'})
        data = PlaceCommon(**json_dict_from_response(response))
        if not data.isUpdated:
            result = f'查询到{data.name}的卡数今天还没有被更新过。'
        else:
            result = f"查询到{data.name}的当前卡数为{data.cardCount}。\n最后更新时间为{format_time(data.updateTime)}"

        await matcher.send(
            reply_text(f"""{result.strip()}
            
{await announcement_list_str(bot, event, data.announcements)}""".strip(), event))

    ##########

    await do_request(matcher, event, place_name, do, False)


async def __update_place(
        bot: Bot,
        event: GroupMessageEvent,
        place_name: str,
        expression: str,
) -> str:
    city_name = group_mapping[event.group_id]
    response = await client.put(
        url=f'/place/{city_name}/{place_name}',
        json={'uploaderId': event.user_id, 'uploaderGroupId': event.group_id, 'updateExpression': expression}
    )
    data = PlaceCommon(**json_dict_from_response(response))
    return f"""成功将{data.name}的卡数更新为{data.cardCount}。
    
{await announcement_list_str(bot, event, data.announcements)}""".strip()


@place_update.handle()
async def handle_place_update(
        matcher: Matcher,
        bot: Bot,
        event: GroupMessageEvent,
        r: Annotated[dict[str, Any], RegexDict()]
):
    place_name = r['place'].strip()
    if expression1 := r['expression1'] is not None:
        expression: str = expression1.replace('＋', '+').replace('＝', '=').replace('－', '-')
    else:
        expression: str = r['expression2'].replace('++', '+1').replace('--', '-1')

    ##########
    async def do():
        result = await __update_place(bot, event, place_name, expression)
        await matcher.send(reply_text(result, event))

    ##########

    await do_request(matcher, event, place_name, do)


@place_update_implicit.handle()
async def handle_place_update_implicit(
        matcher: Matcher,
        bot: Bot,
        event: GroupMessageEvent,
        r: Annotated[dict[str, Any], RegexDict()]
):
    place_name = r['place'].strip()
    expression = f"={r['count']}"

    ##########
    async def do():
        result = await __update_place(bot, event, place_name, expression)
        await matcher.send(reply_text(result, event))

    ##########

    await do_request(matcher, event, place_name, do, False)
