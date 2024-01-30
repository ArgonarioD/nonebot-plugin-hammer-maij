import json
import random
import certifi
import ssl

import httpx
from httpx import Response

from .response_exception import MultipleChoicesError, ClientError, NotFoundError, ServerError
from .. import config


async def response_raise_check(response: Response):
    await response.aread()
    if response.status_code >= 400:
        exception_id = random.Random().randint(0, 10000000)
        unexpected_exception_message = f'发生错误，错误ID为{exception_id}，请与维护者联系。'
        try:
            r_body = response.json()
            code = r_body['code']
        except Exception as e:
            raise ServerError(response.url, response, unexpected_exception_message,
                              f'错误 id {exception_id}: 服务器返回了无法解析的数据。', e)
        if code == 104:
            raise NotFoundError
        if code == 105:
            raise MultipleChoicesError(json.loads(r_body['message']))
        if code == 300:
            raise ClientError('MaiJ API Token 无效，请检查配置。')
        if code == 301:
            raise ClientError('该 MaiJ API Token 无权访问该资源，如需访问请与 API 维护者联系。')
        if response.status_code >= 500:
            raise ServerError(
                response.url,
                response,
                unexpected_exception_message,
                f"MaiJ API 错误 id {exception_id}: {r_body['message'] if 'message' in r_body else '服务器内部错误。'}"
            )
        raise ClientError(unexpected_exception_message, f"未知错误 id {exception_id}: {r_body['message']}")


client = httpx.AsyncClient(
    headers={
        'content-type': 'application/json;charset=utf-8',
        'x-maij-token': config.maij_api_token
    },
    event_hooks={
        'response': [response_raise_check]
    },
    base_url=config.maij_api_root_url,
    http1=False,
    http2=True
)
