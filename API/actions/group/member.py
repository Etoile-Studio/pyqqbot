import requests
from settings import HTTP_PORT, HTTP_HOST


def kickGroupMember(groupId: int, kickUserId: int, noAddAgain: bool = False):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/set_group_kick",
        data={
            "group_id": groupId,
            "user_id": kickUserId,
            "reject_add_request": noAddAgain
        }
    ).json()


def silentGroupMember(groupId: int, noSpeakUserId: int, silentSecond: int):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/set_group_ban",
        data={
            "group_id": groupId,
            "user_id": noSpeakUserId,
            "duration": silentSecond
        }
    ).json()


def unSilentGroupMember(groupId: int, noSpeakUserId: int):
    return silentGroupMember(groupId, noSpeakUserId, 0)


def silentGroupAnonymousMember(groupId: int, anonymous, silentSecond: int):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/set_group_anonymous_ban",
        data={
            "group_id": groupId,
            "anonymous": anonymous,
            "duration": silentSecond
        }
    ).json()


def setGroupAdmin(groupId: int, userId: int):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/set_group_admin",
        data={
            "group_id": groupId,
            "user_id": userId,
            "enable": True
        }
    ).json()


def unsetGroupAdmin(groupId: int, userId: int):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/set_group_admin",
        data={
            "group_id": groupId,
            "user_id": userId,
            "enable": False
        }
    ).json()


def setGroupMemberNickName(groupId: int, userId: int, nickName: str):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/set_group_card",
        data={
            "group_id": groupId,
            "user_id": userId,
            "card": nickName
        }
    ).json()


def unsetGroupMemberNickName(groupId: int, userId: int):
    return setGroupMemberNickName(groupId, userId, "")


def setGroupMemberSpecialTitle(groupId: int, userId: int, title: str):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/set_group_special_title",
        data={
            "group_id": groupId,
            "user_id": userId,
            "special_title": title,
            "duration": -1
        }
    ).json()


def unsetGroupMemberSpecialTitle(groupId: int, userId: int):
    return setGroupMemberSpecialTitle(groupId, userId, "")
