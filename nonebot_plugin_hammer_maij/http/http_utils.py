from httpx import Response


def json_dict_from_response(response: Response) -> dict:
    return response.json()
