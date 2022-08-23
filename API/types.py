from API.actions.group.misc import findFileInFolder


class Sender:
    def __init__(self, sender):
        self.userId = sender["user_id"]
        self.name = sender["nickname"]
        self.sex = sender["sex"]
        self.age = sender["age"]


class GroupSender(Sender):
    def __init__(self, sender):
        super(GroupSender, self).__init__(sender)
        self.nickName = sender["card"]
        self.area = sender["area"]
        self.level = sender["level"]
        self.role = sender["role"]
        self.title = sender["title"]


class Anonymous:
    def __init__(self, anonymous):
        self.id = anonymous["id"]
        self.name = anonymous["name"]
        self.flag = anonymous["flag"]


class Message:
    def __init__(self, event):
        self.time = event["time"]
        self.subType = event["sub_type"]
        self.messageId = event["message_id"]
        self.message = event["message"]
        self.rawMessage = event["raw_message"]
        self.font = event["raw_message"]
        self.rawMessage = event["raw_message"]


"""class PrivateMessage(Message):
    def __init__(self, event):
        super(PrivateMessage, self).__init__(event)
        self.type = "_private"
        self.sender = Sender(event["sender"])
        self.tempSource = event["temp_source"]"""


class GroupMessage(Message):
    def __init__(self, event):
        super(GroupMessage, self).__init__(event)
        self.type = "group"
        self.sender = GroupSender(event["sender"])
        self.groupId = event["group_id"]
        self.anonymous = None if event["anonymous"] is None else Anonymous(event["anonymous"])


class GroupMemberChange:
    def __init__(self, event):
        self.time = event["time"]
        self.subType = event["sub_type"]
        self.groupId = event["group_id"]
        self.operatorId = event["operator_id"]
        self.userId = event["user_id"]


class GroupMemberAdd(GroupMemberChange):
    def __init__(self, event):
        super(GroupMemberAdd, self).__init__(event)


class GroupMemberLeave(GroupMemberChange):
    def __init__(self, event):
        super(GroupMemberLeave, self).__init__(event)
        self.leaveByHimself = self.userId == self.operatorId


class GroupAddRequest:
    def __init__(self, event):
        self.time = event["time"]
        self.subType = event["sub_type"]
        self.groupId = event["group_id"]
        self.userId = event["user_id"]
        self.comment = event["comment"]
        self.flag = event["flag"]


class ForwardMessage:
    def __init__(self, message):
        self.message = message["content"]
        self.groupId = message["group_id"]
        self.userId = message["user_id"]
        self.userName = message["nickname"]
        self.time = message["time"]


class GroupInformation:
    def __init__(self, info):
        self.groupId = info["group_id"]
        self.groupName = info["group_name"]
        self.groupCreateTime = info["group_create_time"]
        self.groupLevel = info["group_level"]
        self.memberCount = info["member_count"]
        self.maxMemberCount = info["max_member_count"]
        self.isInGroup = True
        if self.groupLevel == self.groupCreateTime == self.memberCount == self.maxMemberCount == 0:
            self.isInGroup = False


"""
| `user_id`    |
| `nickname`   |
| `sex`        |
| `age`        |
| `level`      |
| `login_days` |
"""
"""
| `join_time`         |
| `last_sent_time`    |
| `unfriendly`        |
| `title_expire_time` |
| `card_changeable`   |
| `shut_up_timestamp` |
"""


class User(Sender):
    def __init__(self, user):
        super(User, self).__init__(user)
        self.level = user["level"]
        self.loginDays = user["login_days"]


class GroupMember(GroupSender):
    def __init__(self, user):
        super(GroupMember, self).__init__(user)
        self.joinTime = user["join_time"]
        self.lastSentTime = user['last_sent_time']
        self.haveBreakRoleRecord = user['unfriendly']
        self.titleExpireTime = user['title_expire_time']
        self.canChangeNickName = user['card_changeable']
        self.shutUpTimeStamp = user['shut_up_timestamp']


"""
| `file_count`  |
| ------------- |
| `limit_count` |
| `used_space`  |
| `total_space` |
"""


class FileSystemInfo:
    def __init__(self, info):
        self.fileCount = info["file_count"]
        self.maxCount = info["limit_count"]
        self.usedSpace = info["used_space"]
        self.maxSpace = info["total_space"]


class UploadFile:
    def __init__(self, file):
        self.id = file["id"]
        self.name = file["name"]
        self.size = file["size"]
        self.url = file["url"]


class UploadGroupFile:
    def __init__(self, event):
        self.time = event["time"]
        self.groupId = event["group_id"]
        self.userId = event["user_id"]
        self.file = UploadFile(event["file"])


class File:
    def __init__(self, file):
        self.groupId = file["group_id"]
        self.id = file["file_id"]
        self.name = file["file_name"]
        self.busid = file["busid"]
        self.size = file["file_size"]
        self.parentFolderId = findFileInFolder(self.groupId, self.id)
        self.uploadTime = file["upload_time"]
        self.expireTime = file["dead_time"]
        self.lastModifyTime = file["modify_time"]
        self.downloadTimes = file["download_times"]
        self.uploaderId = file["uploader"]
        self.uploaderName = file["uploader_name"]


class Folder:
    def __init__(self, folder):
        self.groupId = folder["group_id"]
        self.id = folder["folder_id"]
        self.name = folder["folder_name"]
        self.createTime = folder["create_time"]
        self.creatorId = folder["creator"]
        self.creatorName = folder["creator_name"]
        self.totalFileCount = folder["total_file_count"]


class GroupAtAllRemain:
    def __init__(self, remain):
        self.canAtAll = remain["can_at_all"]
        self.remainAtAllCountForGroup = remain["remain_at_all_count_for_group"]
        self.remainAtAllCountForYou = remain["remain_at_all_count_for_uin"]


class EssenceMessage:
    def __init__(self, message):
        self.senderId = message["sender_id"]
        self.senderNick = message["sender_nick"]
        self.sendTime = message["sender_time"]
        self.operatorId = message["operator_id"]
        self.operatorNick = message["operator_nick"]
        self.operatorTime = message["operator_time"]
        self.id = message["message_id"]


class CurrentTalkative:
    def __init__(self, talkative):
        self.userId = talkative["user_id"]
        self.nickName = talkative["nickname"]
        self.avatar = talkative["avatar"]
        self.dayCount = talkative["day_count"]


class GroupHonor:
    def __init__(self, honor):
        self.userId = honor["user_id"]
        self.nickName = honor["nickname"]
        self.avatar = honor["avatar"]
        self.description = honor["description"]
