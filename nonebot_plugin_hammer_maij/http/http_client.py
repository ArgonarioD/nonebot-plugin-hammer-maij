import httpx
from httpx import Response

from .response_exception import MultipleChoicesError, ResponseError, NotFoundError


def response_raise_check(response: Response):
    response.read()
    if response.status_code >= 400:
        r_body = response.json()
        code = r_body['code']
        if code == 102:
            raise MultipleChoicesError(r_body['data'])
        if code == 104:
            raise NotFoundError
        if code == 300:
            raise ResponseError('系统繁忙，请稍后再试')
        if response.status_code >= 500:
            raise RuntimeError(r_body['msg'])
        raise ResponseError(r_body['msg'])


client = httpx.Client(headers={'content-type': 'application/json;charset=utf-8'},
                      event_hooks={'response': [response_raise_check]})
