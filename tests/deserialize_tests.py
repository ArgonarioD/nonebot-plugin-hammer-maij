import json
import pytest
from nonebug import App


@pytest.mark.asyncio
async def test_deserialize(app: App):
    async with app.test_matcher() as ctx:
        ctx.create_bot()
        from nonebot_plugin_hammer_maij.data_classes import Place, LogListResult, Announcement

        # place test
        place = Place(**json.loads('''
            {
            "placeId": 1,
            "placeName": "风云再起淮河路店",
            "updateTime": [
                2023,
                4,
                4,
                14,
                2,
                12
            ],
            "cardCount": 6,
            "updated": true,
            "announcements": [
                {
                    "announcementId": 1,
                    "uploaderId": 123456,
                    "uploaderGroupId": 12345678,
                    "announcementContent": "测试公告1",
                    "createTime": [
                        2023,
                        4,
                        4,
                        14,
                        2,
                        12
                    ],
                    "expireTime": [
                        2023,
                        4,
                        11,
                        14,
                        2,
                        12
                    ]
                },
                {
                    "announcementId": 2,
                    "uploaderId": 654321,
                    "uploaderGroupId": 123654321,
                    "announcementContent": "测试公告2",
                    "createTime": [
                        2023,
                        4,
                        4,
                        14,
                        5,
                        12
                    ],
                    "expireTime": [
                        2023,
                        4,
                        11,
                        14,
                        2,
                        12
                    ]
                }
            ]
        }
            '''))
        assert place.placeName == "风云再起淮河路店"
        assert place.updateTime == "14:02:12"
        assert len(place.announcements) == 2
        assert place.announcements[0].announcementContent == '测试公告1'

        # place incomplete test
        place = Place(**json.loads('''
        {
                "placeId": 2,
                "placeName": "super101合肥店",
                "updateTime": [
                    2023,
                    4,
                    4,
                    13,
                    55,
                    14
                ],
                "cardCount": 3,
                "updated": true,
                "announcements": [
                    {
                        "announcementId": 2
                    }
                ]
            }
            '''))
        assert place.placeId == 2
        assert place.placeName == 'super101合肥店'
        assert len(place.announcements) == 1
        assert place.announcements[0].announcementId == 2
        assert place.announcements[0].announcementContent is None

        # log test
        log_result = LogListResult(**json.loads('''
        {
        "placeName": "风云再起淮河路店",
        "announcements": [
            {
                "announcementId": 1,
                "uploaderId": 739062975,
                "uploaderGroupId": 12345678,
                "announcementContent": "测试公告阿巴巴爸爸吧不",
                "createTime": [
                    2023,
                    4,
                    4,
                    14,
                    2,
                    12
                ],
                "expireTime": [
                    2023,
                    4,
                    11,
                    14,
                    2,
                    12
                ]
            }
        ],
        "total": 2,
        "records": [
            {
                "logId": 10,
                "createTime": [
                    2022,
                    7,
                    24,
                    19,
                    30
                ],
                "qqId": 153123153,
                "qqGroupId": 156123123,
                "operateCount": 5,
                "afterCount": 5
            },
            {
                "logId": 11,
                "createTime": [
                    2022,
                    7,
                    24,
                    19,
                    30,
                    13
                ],
                "qqId": 153888853,
                "qqGroupId": 56161233,
                "operateCount": -3,
                "afterCount": 2
            }
        ]
    }
        '''))
        assert log_result.placeName == "风云再起淮河路店"
        assert len(log_result.announcements) == 1
        assert log_result.announcements[0].announcementContent == "测试公告阿巴巴爸爸吧不"
        assert len(log_result.records) == 2
        assert log_result.records[0].createTime == '19:30:00'

        # announcement test
        announcement = Announcement(**json.loads('''
        {
        "announcementId": 3,
        "uploaderId": 123456,
        "uploaderGroupId": 123456789,
        "announcementContent": "测试公告",
        "createTime": [
            2023,
            4,
            4,
            14,
            2,
            12
        ],
        "expireTime": [
            2023,
            4,
            11,
            14,
            2,
            12
        ],
        "place": {
            "placeId": 1,
            "placeName": "风云再起淮河路店"
        }
    }
        '''))
        assert announcement.announcementId == 3
        assert announcement.announcementContent == '测试公告'
        assert announcement.createTime == '14:02:12'
        assert announcement.place.placeId == 1
        assert announcement.place.placeName == '风云再起淮河路店'
