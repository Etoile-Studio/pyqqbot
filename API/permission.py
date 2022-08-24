import json
import os.path

from API.plugin import PluginHelpText
from settings import PATH


class Permissions:
    member = 0
    admin = 1
    owner = 2


def setMemberPermission(groupId, userId, permissionType):
    data = json.load(open(os.path.join(PATH, 'permission.json'), 'r', encoding="utf8"))
    if permissionType == "admin":
        if userId not in data[f"{groupId}"]["admin"]:
            data[f"{groupId}"]["admin"].append(userId)
    elif permissionType == "member":
        if userId in data[f"{groupId}"]["admin"]:
            data[f"{groupId}"]["admin"].remove(userId)
    else:
        return -1
    json.dump(data, open(os.path.join(PATH, 'permission.json'), 'w', encoding="utf8"), indent=4)
    return 0


def setMemberPermissionCommand(command, event):
    """if event.type == "_private":
        return "请在群中操作"""
    if "userid" not in command or "type" not in command:
        return setMemberPermissionCommandHelper()
    try:
        userId = int(command["userid"])
        permissionType = command["type"]
        if setMemberPermission(event.groupId, userId, permissionType) == -1:
            return "您设置的权限不为admin或member之一"
        return "设置成功"
    except:
        return setMemberPermissionCommandHelper()


def setMemberPermissionCommandHelper():
    text = PluginHelpText("setMemberPermission")
    text.addArg("userid", "用户的QQ号", "QQ号", ["int"], False)
    text.addArg("type", "权限类型", "member或者admin", ["string"], False)
    text.addExample("-userid:114514 -type:member", "将QQ号为114514的成员设为普通用户")
    text.addExample("-userid:56339627 -type:admin", "将QQ号为56339627的成员设为命令管理员")
    return text.generate()


def havePermission(groupId, userId, permissionLevel):
    data = json.load(open(os.path.join(PATH, 'permission.json'), 'r', encoding="utf8"))
    userLevel = 0
    if userId in data[f"{groupId}"]["admin"]:
        userLevel = 1
    if userId == data[f"{groupId}"]["owner"]:
        userLevel = 2
    return userLevel >= permissionLevel


def getMemberPermission(groupId):
    data = json.load(open(os.path.join(PATH, 'permission.json'), 'r', encoding="utf8"))
    return data[f"{groupId}"]


def getMemberPermissionCommand(command, event):
    """if event.type == "_private":
        return "请在群中操作"""
    data = getMemberPermission(event.groupId)
    text = f"群主：{data['owner']}\n命令管理员：{' '.join([str(i) for i in data['admin']])}"
    return text


def getMemberPermissionCommandHelper():
    text = PluginHelpText("getMemberPermission")
    text.addExample("", "获取群主以及命令管理员的QQ号")
    return text.generate()
