import asyncio
from typing import Annotated, Any

from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot
from nonebot.internal.matcher import Matcher
from nonebot.params import RegexDict
from nonebot.plugin.on import on_regex
from nonebot_plugin_hammer_core.util.message_factory import reply_text

from .handle_utils import do_request, announcement_list_str, end_line
from .. import group_mapping
from ..http.http_client import client
from ..http.http_models import PlaceForLogs
from ..http.http_utils import json_dict_from_response

place_log_query = on_regex(r'^(?P<place>[^\s]+)都?有谁$')


@place_log_query.handle()
async def handle_place_log_query(
        matcher: Matcher,
        bot: Bot,
        event: GroupMessageEvent,
        r: Annotated[dict[str, Any], RegexDict()]
):
    city_name = group_mapping[event.group_id]
    place_name = r['place'].strip()

    ##########
    async def do():
        response = await client.get(url=f'/place/{city_name}/{place_name}', params={'queryType': 'forLogs'})
        data = PlaceForLogs(**json_dict_from_response(response))
        if len(data.logs) == 0:
            await matcher.finish(reply_text(f'查询到{data.name}的卡数今天还没有被更新过。', event))
        logs = await asyncio.gather(*[log.to_str(bot, event.group_id) for log in data.logs])
        result = f"""{data.name}的卡数更新记录如下：
{end_line.join(logs)}

{await announcement_list_str(bot, event, data.announcements)}""".strip()
        await matcher.finish(reply_text(result, event))

    ##########

    await do_request(matcher, event, place_name, do)
