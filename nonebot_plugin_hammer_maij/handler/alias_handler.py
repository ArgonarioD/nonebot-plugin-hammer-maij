from typing import Annotated, Any

from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.internal.matcher import Matcher
from nonebot.params import RegexDict
from nonebot.plugin.on import on_regex
from nonebot_plugin_hammer_core.util.message_factory import reply_text

from .handle_utils import do_request
from .. import group_mapping
from ..http.http_client import client
from ..http.http_models import PlaceForAliases
from ..http.http_utils import json_dict_from_response

place_aliases_query = on_regex(r'^(?P<place>[^\s]+)(有什么别名|的别名都?[是有]什么)$')


@place_aliases_query.handle()
async def handle_place_aliases_query(
        matcher: Matcher,
        event: GroupMessageEvent,
        r: Annotated[dict[str, Any], RegexDict()]
):
    city_name = group_mapping[event.group_id]
    place_name = r['place'].strip()

    ##########
    async def do():
        response = await client.get(url=f'/place/{city_name}/{place_name}', params={'queryType': 'forAliases'})
        data = PlaceForAliases(**json_dict_from_response(response))
        await matcher.finish(reply_text(data.to_str(), event))

    ##########

    await do_request(matcher, event, place_name, do)
