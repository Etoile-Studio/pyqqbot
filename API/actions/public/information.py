import requests
from settings import HTTP_PORT, HTTP_HOST


def getUserInfo(userId: int, noCache: bool = False):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/get_stranger_info",
        data={
            "user_id": userId,
            "no_cache": noCache
        }
    ).json()
