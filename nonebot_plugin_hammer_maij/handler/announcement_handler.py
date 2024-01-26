from re import DOTALL
from typing import Annotated, Any

from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot
from nonebot.internal.matcher import Matcher
from nonebot.params import RegexDict
from nonebot.plugin.on import on_regex
from nonebot_plugin_hammer_core.util.message_factory import reply_text

from .handle_utils import do_request
from .. import group_mapping
from ..http.http_client import client
from ..http.http_models import Announcement
from ..http.http_utils import json_dict_from_response

announcement_add = on_regex(r'^(?:添加(?:一[个条])?|[加发]一?[个条])公告 (?P<place>.+?)\s(?P<content>.+)', flags=DOTALL)
announcement_renewal = on_regex(r'^续一?[续下发]公告 (?P<place>.+?) (?P<announcementId>\d+)$')
announcement_delete = on_regex(r'^(?:[删移]除(?:一[个条])?|删一?[个条])公告 (?P<place>.+?) (?P<announcementId>\d+)$')


@announcement_add.handle()
async def handle_announcement_add(
        matcher: Matcher,
        bot: Bot,
        event: GroupMessageEvent,
        r: Annotated[dict[str, Any], RegexDict()]
):
    city_name = group_mapping[event.group_id]
    place_name = r['place'].strip()
    content = r['content'].strip()

    ##########
    async def do():
        response = await client.post(
            url=f'/place/{city_name}/{place_name}/announcement',
            json={'uploaderId': event.user_id, 'uploaderGroupId': event.group_id, 'content': content}
        )
        data = Announcement(**json_dict_from_response(response))
        await matcher.finish(reply_text(f"""成功为 {data.place.name} 添加了一条公告，公告内容如下：
{await data.to_str(bot, event.group_id)}""".strip(), event))

    ##########

    await do_request(matcher, event, place_name, do)


@announcement_renewal.handle()
async def handle_announcement_renewal(
        matcher: Matcher,
        bot: Bot,
        event: GroupMessageEvent,
        r: Annotated[dict[str, Any], RegexDict()]
):
    city_name = group_mapping[event.group_id]
    place_name = r['place'].strip()
    announcement_id = r['announcementId']

    ##########
    async def do():
        response = await client.put(url=f'/place/{city_name}/{place_name}/announcement/{announcement_id}/renewal', )
        data = Announcement(**json_dict_from_response(response))
        await matcher.finish(reply_text(f"""成功为 {data.place.name} 的第 {announcement_id} 号公告续期一周，公告内容如下：
{await data.to_str(bot, event.group_id)}""".strip(), event))

    ##########

    await do_request(matcher, event, place_name, do)


@announcement_delete.handle()
async def handle_announcement_delete(
        matcher: Matcher,
        bot: Bot,
        event: GroupMessageEvent,
        r: Annotated[dict[str, Any], RegexDict()]
):
    city_name = group_mapping[event.group_id]
    place_name = r['place'].strip()
    announcement_id = r['announcementId']

    ##########
    async def do():
        response = await client.delete(url=f'/place/{city_name}/{place_name}/announcement/{announcement_id}')
        data = Announcement(**json_dict_from_response(response))
        await matcher.finish(reply_text(f"""成功为 {data.place.name} 删除了第 {announcement_id} 号公告，公告内容如下：
{await data.to_str(bot, event.group_id)}""".strip(), event))

    ##########

    await do_request(matcher, event, place_name, do)
