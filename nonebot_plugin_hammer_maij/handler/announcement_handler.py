from typing import Annotated, Any

from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot
from nonebot.internal.matcher import Matcher
from nonebot.params import RegexGroup
from nonebot.plugin.on import on_regex
from nonebot_plugin_hammer_core.util.message_factory import reply_text

from .handle_utils import get_group_location, do_request
from ..const import consts
from ..data_classes import Announcement
from ..http.http_client import client
from ..http.http_utils import json_dict_from_response

add_announcement = on_regex(r'^(?:添加(?:一[个条])?|[加发]一?[个条])公告 (.+?)\s(.+)')
renewal_announcement = on_regex(r'^续一?[续下发]公告 (.+?) (\d+)')
delete_announcement = on_regex(r'^(?:[删移]除(?:一[个条])?|删一?[个条])公告 (.+?) (\d+)')


@add_announcement.handle()
async def handle_add_announcement(
        matcher: Matcher,
        bot: Bot,
        event: GroupMessageEvent,
        r: Annotated[tuple[Any, ...], RegexGroup()]
):
    location = get_group_location(event.group_id)
    place_name: str = r[0].strip()
    content: str = r[1].strip()

    ##########
    async def do():
        response = client.post(url=f'{consts.API_URL}/place/{location}/{place_name}/announcement', json={
            'uploaderId': event.user_id,
            'uploaderGroupId': event.group_id,
            'announcementContent': content
        })
        data = Announcement(**json_dict_from_response(response))
        await matcher.send(reply_text(f'''成功为{data.place.placeName}创建公告，公告内容如下：
{await data.display_str(bot, event)}'''.strip(), event))

    ##########

    await do_request(matcher, event, place_name, do)


@renewal_announcement.handle()
async def handle_renewal_announcement(
        matcher: Matcher,
        bot: Bot,
        event: GroupMessageEvent,
        r: Annotated[tuple[Any, ...], RegexGroup()]
):
    location = get_group_location(event.group_id)
    place_name: str = r[0].strip()
    try:
        announcement_id: int = int(r[1].strip())
    except ValueError:
        await matcher.send(reply_text('请输入正确的公告ID。', event))
        return

    ##########
    async def do():
        response = client.put(
            url=f'{consts.API_URL}/place/{location}/{place_name}/announcement/{announcement_id}/renewal',
            json={
                "operator": event.user_id,
            })
        data = Announcement(**json_dict_from_response(response))
        await matcher.send(
            reply_text(
                f'''成功为{data.place.placeName}的第{data.announcementId}号公告续期一周，其内容如下：
{await data.display_str(bot, event)}'''.strip(), event))

    ##########

    await do_request(matcher, event, place_name, do, handle_not_found=True)


@delete_announcement.handle()
async def handle_delete_announcement(
        matcher: Matcher,
        bot: Bot,
        event: GroupMessageEvent,
        r: Annotated[tuple[Any, ...], RegexGroup()]
):
    location = get_group_location(event.group_id)
    place_name: str = r[0].strip()
    try:
        announcement_id: int = int(r[1].strip())
    except ValueError:
        await matcher.send(reply_text('请输入正确的公告ID。', event))
        return

    ##########
    async def do():
        response = client.delete(
            url=f'{consts.API_URL}/place/{location}/{place_name}/announcement/{announcement_id}',
            json={
                "deleterId": event.user_id,
            })
        data = Announcement(**json_dict_from_response(response))
        await matcher.send(
            reply_text(f'''成功为{data.place.placeName}删除了第{data.announcementId}号公告，其内容如下：
{await data.display_str(bot, event)}'''.strip(), event))

    ##########

    await do_request(matcher, event, place_name, do)
