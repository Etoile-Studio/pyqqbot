import requests
from settings import HTTP_PORT, HTTP_HOST


def setGroupName(groupId: int, name: str):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/set_group_name",
        data={
            "group_id": groupId,
            "group_name": name,
        }
    ).json()


def setGroupImage(groupId: int, filePathOrUrl: str, cache: bool = False):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/set_group_portrait",
        data={
            "group_id": groupId,
            "file": filePathOrUrl,
            "cache": int(cache)
        }
    ).json()


def getGroupInfo(groupId: int, noCache: bool = False):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/get_group_info",
        data={
            "group_id": groupId,
            "no_cache": noCache
        }
    ).json()


def getGroupImage(groupId: int):
    return requests.post(
        f"https://p.qlogo.cn/gh/{groupId}/{groupId}/100",
    ).content


def getGroupMemberList(groupId: int):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/get_group_member_list",
        data={
            "group_id": groupId,
        }
    ).json()


def getGroupHonorInfo(groupId: int, honorType: str):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/get_group_honor_info",
        data={
            "group_id": groupId,
            "type": honorType
        }
    ).json()


def getGroupHonorList(groupId: int):
    return getGroupHonorInfo(groupId, "all")
