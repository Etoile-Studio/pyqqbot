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
        self.groupId = sender["group_id"]


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


class PrivateMessage(Message):
    def __init__(self, event):
        super(PrivateMessage, self).__init__(event)
        self.type = "private"
        self.sender = Sender(event["sender"])
        self.tempSource = event["temp_source"]


class GroupMessage(Message):
    def __init__(self, event):
        super(GroupMessage, self).__init__(event)
        self.type = "group"
        self.sender = GroupSender(event["sender"])
        self.groupId = event["group_id"]
        self.anonymous = None if event["anonymous"] is None else Anonymous(event["anonymous"])


class File:
    def __init__(self, file):
        self.id = file["id"]
        self.name = file["name"]
        self.size = file["size"]
        self.url = file["url"]


class GroupFile:
    def __init__(self, event):
        self.time = event["time"]
        self.groupId = event["group_id"]
        self.userId = event["user_id"]
        self.file = File(event["file"])


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
