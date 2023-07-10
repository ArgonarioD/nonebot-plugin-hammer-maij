from typing import Annotated, Any

from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot
from nonebot.internal.matcher import Matcher
from nonebot.params import RegexGroup
from nonebot.plugin.on import on_regex
from nonebot_plugin_hammer_core.util.message_factory import reply_text
from nonebot_plugin_hammer_core.util.onebot_utils import get_qq_nickname_with_group

from .handle_utils import get_group_location, do_request, end_line, get_announcement_list_str
from ..const import consts
from ..data_classes import LogListResult
from ..http.http_client import client
from ..http.http_utils import json_dict_from_response

maij_log = on_regex(r'(.+?)都?有谁$')


@maij_log.handle()
async def handle_maij_log(
        bot: Bot,
        matcher: Matcher,
        event: GroupMessageEvent,
        r: Annotated[tuple[Any, ...], RegexGroup()]
):
    location = get_group_location(event.group_id)
    place_name = r[0]

    ###########
    async def do():
        response = client.get(url=f'{consts.API_URL}/place/{location}/{place_name}/log')
        data = LogListResult(**json_dict_from_response(response))
        if data.total == 0:
            result = f"{data.placeName}目前还没有人排过卡。".strip()
        else:
            result_list = [
                ' - {} 在{}{}{}张卡，卡数变为{}'.format(
                    await get_qq_nickname_with_group(bot, log.qqId, event.group_id, log.qqGroupId),
                    log.createTime,
                    '添加' if log.operateCount > 0 else '移除',
                    abs(log.operateCount),
                    log.afterCount
                ) for log in data.records
            ]
            result = f"{data.placeName}的卡数变更记录如下：\n{end_line.join(result_list)}".strip()

        await matcher.send(
            reply_text(f"{result}\n\n{await get_announcement_list_str(bot, event, data.announcements)}".strip(), event))

    ###########

    await do_request(matcher, event, place_name, do)
