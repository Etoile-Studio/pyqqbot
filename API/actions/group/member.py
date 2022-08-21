import requests
from settings import HTTP_PORT, HTTP_HOST
from API.types import GroupMember, CurrentTalkative, GroupHonor


def kickGroupMember(groupId: int, kickUserId: int, noAddAgain: bool = False):
    data = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/set_group_kick",
        data={
            "group_id": groupId,
            "user_id": kickUserId,
            "reject_add_request": noAddAgain
        }
    ).json()
    if data["status"].lower() in ["ok", "async"]:
        return "ok"
    return -1


def silentGroupMember(groupId: int, noSpeakUserId: int, silentSecond: int):
    data = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/set_group_ban",
        data={
            "group_id": groupId,
            "user_id": noSpeakUserId,
            "duration": silentSecond
        }
    ).json()
    if data["status"].lower() in ["ok", "async"]:
        return "ok"
    return -1


def unSilentGroupMember(groupId: int, noSpeakUserId: int):
    return silentGroupMember(groupId, noSpeakUserId, 0)


def silentGroupAnonymousMember(groupId: int, anonymous, silentSecond: int):
    data = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/set_group_anonymous_ban",
        data={
            "group_id": groupId,
            "anonymous": anonymous,
            "duration": silentSecond
        }
    ).json()
    if data["status"].lower() in ["ok", "async"]:
        return "ok"
    return -1


def setGroupAdmin(groupId: int, userId: int):
    data = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/set_group_admin",
        data={
            "group_id": groupId,
            "user_id": userId,
            "enable": True
        }
    ).json()
    if data["status"].lower() in ["ok", "async"]:
        return "ok"
    return -1


def unsetGroupAdmin(groupId: int, userId: int):
    data = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/set_group_admin",
        data={
            "group_id": groupId,
            "user_id": userId,
            "enable": False
        }
    ).json()
    if data["status"].lower() in ["ok", "async"]:
        return "ok"
    return -1


def setGroupMemberNickName(groupId: int, userId: int, nickName: str):
    data = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/set_group_card",
        data={
            "group_id": groupId,
            "user_id": userId,
            "card": nickName
        }
    ).json()
    if data["status"].lower() in ["ok", "async"]:
        return "ok"
    return -1


def unsetGroupMemberNickName(groupId: int, userId: int):
    return setGroupMemberNickName(groupId, userId, "")


def setGroupMemberSpecialTitle(groupId: int, userId: int, title: str):
    data = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/set_group_special_title",
        data={
            "group_id": groupId,
            "user_id": userId,
            "special_title": title,
            "duration": -1
        }
    ).json()
    if data["status"].lower() in ["ok", "async"]:
        return "ok"
    return -1


def unsetGroupMemberSpecialTitle(groupId: int, userId: int):
    return setGroupMemberSpecialTitle(groupId, userId, "")


def getGroupMemberList(groupId: int):
    data = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/get_group_member_list",
        data={
            "group_id": groupId,
        }
    ).json()
    if data["status"].lower() in ["ok", "async"]:
        returnList = []
        for dat in data["data"]:
            returnList.append(GroupMember(dat))
        return returnList
    return -1


def getGroupMemberInfo(groupId: int, userId: int, noCache: bool = False):
    data = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/get_group_member_info",
        data={
            "group_id": groupId,
            "user_id": userId,
            "no_cache": noCache
        }
    ).json()
    if data["status"].lower() in ["ok", "async"]:
        return GroupMember(data["data"])
    return -1


def getGroupHonorInfo(groupId: int, honorType: str):
    data = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/get_group_honor_info",
        data={
            "group_id": groupId,
            "type": honorType
        }
    ).json()
    if data["status"].lower() in ["ok", "async"]:
        returns = {"current_talkative": None, "talkative_list": None, "performer_list": None, "legend_list": None, "strong_newbie_list": None, "emotion_list": None}
        match honorType:
            case "talkative":
                if data["data"]["current_talkative"] is not None:
                    returns["current_talkative"] = CurrentTalkative(data["data"]["current_talkative"])
            case "all":
                if data["data"]["current_talkative"] is not None:
                    returns["current_talkative"] = CurrentTalkative(data["data"]["current_talkative"])
        if data["data"]["talkative_list"] is not None:
            returns["talkative_list"] = []
            for dat in data["data"]["talkative_list"]:
                returns["talkative_list"].append(GroupHonor(dat))
        if data["data"]["performer_list"] is not None:
            returns["performer_list"] = []
            for dat in data["data"]["performer_list"]:
                returns["performer_list"].append(GroupHonor(dat))
        if data["data"]["legend_list"] is not None:
            returns["legend_list"] = []
            for dat in data["data"]["legend_list"]:
                returns["legend_list"].append(GroupHonor(dat))
        if data["data"]["strong_newbie_list"] is not None:
            returns["strong_newbie_list"] = []
            for dat in data["data"]["strong_newbie_list"]:
                returns["strong_newbie_list"].append(GroupHonor(dat))
        if data["data"]["emotion_list"] is not None:
            returns["emotion_list"] = []
            for dat in data["data"]["emotion_list"]:
                returns["emotion_list"].append(GroupHonor(dat))
    return -1


def getGroupHonorList(groupId: int):
    return getGroupHonorInfo(groupId, "all")
