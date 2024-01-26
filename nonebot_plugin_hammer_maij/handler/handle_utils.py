import asyncio

from nonebot import logger
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot
from nonebot.exception import FinishedException
from nonebot.internal.matcher import Matcher
from nonebot_plugin_hammer_core.util.message_factory import reply_text

from ..http.http_models import Announcement
from ..http.response_exception import NotFoundError, MultipleChoicesError, ClientError, \
    ServerError

end_line = '\n'
double_end_line = '\n\n'


async def announcement_list_str(bot: Bot, event: GroupMessageEvent, announcements: list[Announcement]) -> str:
    if len(announcements) == 0:
        return ''
    results = await asyncio.gather(*[a.to_str(bot, event.group_id) for a in announcements])
    return f"""该地点共有 {len(announcements)} 条公告：
{double_end_line.join(results)}"""


async def do_request(matcher: Matcher, event: GroupMessageEvent, place_name: str, func, handle_not_found: bool = True):
    try:
        await func()
    except FinishedException:
        pass
    except NotFoundError:
        if handle_not_found:
            await matcher.send(reply_text(f'找不到被称为{place_name}的地点。', event))
    except MultipleChoicesError as me:
        await matcher.send(reply_text(f'''找到多个匹配地名{place_name}对应的地点，请用更具体一点的名称问我。
匹配到的地点全称和别名如下：
{double_end_line.join([s.to_str() for s in me.choices])}''', event))
    except ClientError as ce:
        if ce.internal_message is not None:
            logger.error(ce.internal_message)
        await matcher.send(reply_text(ce.message, event))
    except ServerError as se:
        logger.error(se.internal_message)
        logger.error(f'url: {se.url}')
        logger.error(f'response: {se.response}')
        if se.exception is not None:
            logger.opt(exception=True).error(se.exception)
        await matcher.send(reply_text(se.message, event))
    except Exception as e:
        logger.opt(exception=True).error(e)
        await matcher.send(reply_text('发生未知错误，请联系维护者。', event))


