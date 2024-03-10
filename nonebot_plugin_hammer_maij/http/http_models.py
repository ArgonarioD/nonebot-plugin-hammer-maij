from datetime import datetime
from typing import Optional

from nonebot.adapters.onebot.v11 import Bot
from nonebot_plugin_hammer_core.util.onebot_utils import get_qq_nickname_with_group

from ..time_utils import format_time

end_line = '\n'


class Log:
    def __init__(
            self,
            id: int,
            createTime: str,
            uploaderId: int,
            uploaderGroupId: int,
            operateCount: int,
            afterCount: int,
    ):
        self.id: int = id
        self.createTime: datetime = datetime.fromisoformat(createTime)
        self.uploaderId: int = uploaderId
        self.uploaderGroupId: int = uploaderGroupId
        self.operateCount: int = operateCount
        self.afterCount: int = afterCount

    async def to_str(self, bot: Bot, current_group_id: int) -> str:
        operate_count = f"+{self.operateCount}" if self.operateCount >= 0 else str(self.operateCount)
        return f" - {await get_qq_nickname_with_group(bot, self.uploaderId, current_group_id, self.uploaderGroupId)} {operate_count}卡 至 {self.afterCount}卡 （{format_time(self.createTime)}）"


class PlaceBrief:
    def __init__(
            self,
            id: int,
            name: str,
    ):
        self.id: int = id
        self.name: str = name


class PlaceForLogs(PlaceBrief):
    def __init__(
            self,
            id: int,
            name: str,
            announcements: list[dict],
            logs: list[dict],
    ):
        super().__init__(id, name)
        self.announcements: list[Announcement] = []
        for announcement in announcements:
            self.announcements.append(Announcement(**announcement))
        self.logs: list[Log] = []
        for log in logs:
            self.logs.append(Log(**log))


class Announcement:
    def __init__(
            self,
            id: int,
            uploaderId: int,
            uploaderGroupId: int,
            content: str,
            createTime: str,
            expireTime: str,
            place: Optional[dict] = None
    ):
        self.id: int = id
        self.uploaderId: int = uploaderId
        self.uploaderGroupId: int = uploaderGroupId
        self.content: str = content
        self.createTime: datetime = datetime.fromisoformat(createTime)
        self.expireTime: datetime = datetime.fromisoformat(expireTime)
        self.place: Optional[PlaceBrief] = PlaceBrief(**place) if place is not None else None

    async def to_str(self, bot: Bot, current_group_id: int) -> str:
        return f"""ID {self.id}：
{self.content}
By {await get_qq_nickname_with_group(
            bot,
            self.uploaderId,
            current_group_id,
            self.uploaderGroupId
        )}"""


class PlaceCommon(PlaceBrief):
    def __init__(
            self,
            id: int,
            name: str,
            updateTime: str,
            cardCount: int,
            isUpdated: bool,
            announcements: list[dict]
    ):
        super().__init__(id, name)
        self.updateTime: datetime = datetime.fromisoformat(updateTime)
        self.cardCount: int = cardCount
        self.isUpdated: bool = isUpdated
        self.announcements: list[Announcement] = []
        for announcement in announcements:
            self.announcements.append(Announcement(**announcement))


class PlaceListed(PlaceBrief):
    def __init__(
            self,
            id: int,
            name: str,
            updateTime: str,
            cardCount: int,
            announcements: list,
    ):
        super().__init__(id, name)
        self.updateTime: datetime = datetime.fromisoformat(updateTime)
        self.cardCount: int = cardCount
        self.announcements: list = []
        for announcement in announcements:
            self.announcements.append(announcement)

    def to_str(self) -> str:
        result = f"{self.name}：{self.cardCount}（{format_time(self.updateTime)}）"
        if len(self.announcements) > 0:
            result += f"（{len(self.announcements)}条公告）"
        return result


class CityCardStatus:
    def __init__(
            self,
            updatedPlaces: list[dict],
            nonUpdatedPlacesWithAnnouncements: list[dict],
    ):
        self.updatedPlaces: list[PlaceListed] = []
        for place in updatedPlaces:
            self.updatedPlaces.append(PlaceListed(**place))
        self.nonUpdatedPlacesWithAnnouncements: list[PlaceListed] = []
        for place in nonUpdatedPlacesWithAnnouncements:
            self.nonUpdatedPlacesWithAnnouncements.append(PlaceListed(**place))


class Alias:
    def __init__(
            self,
            id: int,
            name: str
    ):
        self.id: int = id
        self.name: str = name


class PlaceForAliases:
    def __init__(
            self,
            id: int,
            name: str,
            aliases: list[dict]
    ):
        self.id: int = id
        self.name: str = name
        self.aliases: list[Alias] = []
        for alias in aliases:
            self.aliases.append(Alias(**alias))

    def to_str(self) -> str:
        return f'''{self.name}的别名有：
{end_line.join([f" - {alias.name}" for alias in self.aliases])}'''
