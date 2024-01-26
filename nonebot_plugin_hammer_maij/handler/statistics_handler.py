from datetime import datetime
from pathlib import Path
from typing import Annotated, Any

from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from nonebot.internal.matcher import Matcher
from nonebot.params import RegexDict
from nonebot.plugin.on import on_regex
from nonebot_plugin_hammer_core.util.message_factory import reply
from playwright.async_api import async_playwright

from .handle_utils import do_request
from .. import group_mapping, plugin_cache_dir
from ..http.http_client import client
from ..http.http_utils import json_dict_from_response

__statistic_images_cache_dir = plugin_cache_dir / 'statisticImages'
__statistic_images_cache_dir.mkdir(parents=True, exist_ok=True)
place_weekly_statistic = on_regex(r'^(?P<place>[^\s]+?)的?[本这]?周的?出勤情况$')


@place_weekly_statistic.handle()
async def handle_place_weekly_statistic(
        matcher: Matcher,
        event: GroupMessageEvent,
        r: Annotated[dict[str, Any], RegexDict()]
):
    city_name = group_mapping[event.group_id]
    place_name = r['place'].strip()

    ##########
    async def do():
        place_data_resp = await client.get(url=f'/place/{city_name}/{place_name}', params={'queryType': 'forAliases'})
        place_data = json_dict_from_response(place_data_resp)
        real_place_name = place_data['name']

        current_time = datetime.now()
        await __clear_old_statistic_cache(current_time)
        cache_path, exist = await __get_statistic_image_cache(real_place_name, current_time)
        if exist:
            stats_image = cache_path
        else:
            response = await client.get(url=f'/stat/{city_name}/{place_name}/render')
            html = response.text
            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(headless=True)
                browser_page = await browser.new_page()
                await browser_page.set_content(html, wait_until='networkidle')
                await browser_page.wait_for_timeout(1000)
                stats_image = await browser_page.screenshot(
                    type="jpeg",
                    path=cache_path,
                    quality=80,
                    full_page=True
                )
                await browser.close()
        await matcher.send(reply(MessageSegment.image(stats_image), event))

    ##########

    await do_request(matcher, event, place_name, do)


async def __get_statistic_image_cache(place_name: str, current_time: datetime) -> (Path, bool):
    file_name = f'{place_name}_{current_time.year}_{current_time.month}_{current_time.day}_{current_time.hour}.jpeg'
    file_path = __statistic_images_cache_dir / file_name
    if not file_path.exists():
        return file_path, False
    return file_path, True


async def __clear_old_statistic_cache(current_time: datetime):
    files = __statistic_images_cache_dir.glob(
        f'.+?_{current_time.year}_{current_time.month}_{current_time.day}_{current_time.hour - 1}.jpeg'
    )
    for file in files:
        file.unlink()
