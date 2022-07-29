import requests
from settings import HTTP_PORT, HTTP_HOST
from API.types import GroupInformation


def setGroupName(groupId: int, name: str):
    data = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/set_group_name",
        data={
            "group_id": groupId,
            "group_name": name,
        }
    ).json()
    if data["status"].lower() in ["ok", "async"]:
        return "ok"
    return -1


def setGroupImage(groupId: int, filePathOrUrl: str, cache: bool = False):
    data = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/set_group_portrait",
        data={
            "group_id": groupId,
            "file": filePathOrUrl,
            "cache": int(cache)
        }
    ).json()
    if data["status"].lower() in ["ok", "async"]:
        return "ok"
    return -1


def getGroupInfo(groupId: int, noCache: bool = False):
    data = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/get_group_info",
        data={
            "group_id": groupId,
            "no_cache": noCache
        }
    ).json()
    if data["status"].lower() in ["ok", "async"]:
        return GroupInformation(data["data"])
    return -1


def getGroupImage(groupId: int):
    return requests.post(
        f"https://p.qlogo.cn/gh/{groupId}/{groupId}/100",
    ).content
