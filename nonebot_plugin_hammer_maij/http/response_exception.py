from typing import Optional

from httpx import URL, Response

from nonebot_plugin_hammer_maij.http.http_models import PlaceForAliases


class MultipleChoicesError(Exception):
    choices: list[PlaceForAliases] = []

    def __init__(self, choices: list[PlaceForAliases]):
        self.choices = choices


class NotFoundError(Exception):
    def __init__(self):
        pass


class ClientError(Exception):
    def __init__(self, message, internal_message=None):
        self.message = message
        self.internal_message = internal_message


class ServerError(Exception):
    def __init__(self, url, response, message, internal_message, e=None):
        self.url: URL = url
        self.response: Response = response
        self.message: str = message
        self.internal_message: str = internal_message
        self.exception: Optional[Exception] = e
