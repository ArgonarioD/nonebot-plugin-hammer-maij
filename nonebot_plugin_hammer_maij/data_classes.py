from typing import Union

from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot_plugin_hammer_core.util.onebot_utils import get_qq_nickname_with_group

from .utils import format_local_date_time


class Place:
    def __init__(
            self,
            placeId: int,
            placeName: Union[str, None] = None,
            updateTime: Union[list[int, ...], None] = None,
            cardCount: Union[int, None] = None,
            updated: Union[bool, None] = None,
            announcements: Union[list[dict, ...], None] = None
    ):
        self.placeId: int = placeId
        self.placeName: Union[str, None] = placeName
        self.updateTime: Union[str, None] = format_local_date_time(updateTime) if updateTime else None
        self.cardCount: Union[int, None] = cardCount
        self.updated: Union[bool, None] = updated
        if announcements is None:
            self.announcements: Union[list[Announcement, ...], None] = None
            return
        self.announcements: Union[list[Announcement, ...], None] = []
        for announcement in announcements:
            self.announcements.append(Announcement(**announcement))


class Announcement:
    def __init__(
            self,
            announcementId: int,
            uploaderId: Union[int, None] = None,
            uploaderGroupId: Union[int, None] = None,
            announcementContent: Union[str, None] = None,
            createTime: Union[list[int, ...], None] = None,
            expireTime: Union[list[int, ...], None] = None,
            place: Union[dict, None] = None
    ):
        self.announcementId: int = announcementId
        self.uploaderId: Union[int, None] = uploaderId
        self.uploaderGroupId: Union[int, None] = uploaderGroupId
        self.announcementContent: Union[str, None] = announcementContent
        self.createTime: Union[str, None] = format_local_date_time(createTime, True) if createTime else None
        self.expireTime: Union[str, None] = format_local_date_time(expireTime, True) if expireTime else None
        self.place: Union[Place, None] = Place(**place) if place else None

    async def display_str(self, bot: Bot, event: GroupMessageEvent) -> str:
        return f'''公告ID：{self.announcementId}
{self.announcementContent}
By {await get_qq_nickname_with_group(bot, self.uploaderId, event.group_id, self.uploaderGroupId)} {self.createTime} 将于{self.expireTime}过期'''.strip()


class Log:
    def __init__(
            self,
            logId: int,
            createTime: Union[list[int, ...], None] = None,
            qqId: Union[int, None] = None,
            qqGroupId: Union[int, None] = None,
            operateCount: Union[int, None] = None,
            afterCount: Union[int, None] = None,
    ):
        self.logId: int = logId
        self.createTime: Union[str, None] = format_local_date_time(createTime) if createTime else None
        self.qqId: Union[int, None] = qqId
        self.qqGroupId: Union[int, None] = qqGroupId
        self.operateCount: Union[int, None] = operateCount
        self.afterCount: Union[int, None] = afterCount


class LogListResult:
    def __init__(
            self,
            placeName: str,
            announcements: list[dict, ...],
            total: int,
            records: list[dict, ...]
    ):
        self.placeName: str = placeName
        self.announcements: list[Announcement, ...] = []
        for announcement in announcements:
            self.announcements.append(Announcement(**announcement))
        self.total: int = total
        self.records: list[Log, ...] = []
        for record in records:
            self.records.append(Log(**record))
