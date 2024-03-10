from re import IGNORECASE

from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.internal.matcher import Matcher
from nonebot.plugin.on import on_regex
from nonebot_plugin_hammer_core.util.message_factory import reply_text

from .handle_utils import end_line, do_request
from .. import group_mapping
from ..http.http_client import client
from ..http.http_models import CityCardStatus
from ..http.http_utils import json_dict_from_response

city_all_updated_place_query = on_regex(r'^(机厅列表|jtlb)$', flags=IGNORECASE)


@city_all_updated_place_query.handle()
async def handle_city_all_updated_place_query(
        matcher: Matcher,
        event: GroupMessageEvent,
):
    city_name = group_mapping[event.group_id]

    ##########
    async def do():
        response = await client.get(url=f'/city/{city_name}/card')
        data = CityCardStatus(**json_dict_from_response(response))
        if len(data.updatedPlaces) == 0:
            result = f'自今日API重置后，{city_name}还没有任何机厅的卡数被更新过。'
        else:
            sum_card_count = 0
            for d in data.updatedPlaces:
                sum_card_count += d.cardCount
            result = f"""自今日API重置后，{city_name}共有{len(data.updatedPlaces)}所机厅的卡数被更新过，在勤人数{sum_card_count}，按其当前卡数的正序、更新时间的倒序排列如下：
{end_line.join([f"- {d.to_str()}" for d in data.updatedPlaces])}"""

        if len(data.nonUpdatedPlacesWithAnnouncements) > 0:
            result += '\n\n'
            result += f"""以下{len(data.nonUpdatedPlacesWithAnnouncements)}个机厅的卡数还没有被更新过，但存在公告：
{end_line.join([f"- {d.name}（{len(d.announcements)}条公告）" for d in data.nonUpdatedPlacesWithAnnouncements])}"""
        await matcher.finish(reply_text(result, event))

    ##########

    await do_request(matcher, event, city_name, do)
