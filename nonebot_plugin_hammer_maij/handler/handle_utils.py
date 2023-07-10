import traceback
from io import StringIO

from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.internal.matcher import Matcher
from nonebot_plugin_hammer_core.util.message_factory import reply_text

from ..data_classes import Announcement, Place
from ..http.response_exception import NotFoundError, MultipleChoicesError, ResponseError
from ..maij_config import plugin_config

end_line = '\n'


def get_group_location(group_id: int) -> str:
    if group_id not in plugin_config.group_location:
        raise ValueError('本群尚未配置地区')
    return plugin_config.group_location[group_id]


def get_place_list_str(places: list[Place, ...]) -> str:
    result_list = [
        f'- {place.placeName}：{place.cardCount}（{place.updateTime}）{f"（{len(place.announcements)}条公告）" if len(place.announcements) > 0 else ""}'
        for place in places]
    return end_line.join(result_list)


async def get_announcement_list_str(bot: Bot, event: GroupMessageEvent, announcements: list[Announcement, ...]) -> str:
    if len(announcements) == 0:
        return ''
    else:
        result = StringIO()
        result.write(f'该地点有{len(announcements)}条公告。\n')
        for announcement in announcements:
            result.write(await announcement.display_str(bot, event))
            result.write(end_line)
        return result.getvalue()


async def do_request(matcher: Matcher, event: GroupMessageEvent, place_name: str, func, handle_not_found: bool = False):
    try:
        await func()
    except NotFoundError:
        if handle_not_found:
            await matcher.send(reply_text(f'找不到被称为{place_name}的地点。', event))
    except MultipleChoicesError as me:
        await matcher.send(reply_text(f'''找到多个匹配地名{place_name}对应的地点，请用更具体一点的名称问我。
匹配到的地点全称如下：
{end_line.join([f" - {s}" for s in me.choices])}''', event))
    except ResponseError as rese:
        await matcher.send(reply_text(f'{rese.message}。', event))
    except RuntimeError:
        await matcher.send(reply_text('出了点小错误，请稍后再试。', event))
        traceback.print_exc()
