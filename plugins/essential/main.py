import datetime
import os.path
import threading
import time as timer

from API.misc import stopThread
from API.permission import Permissions
from API.plugin import Plugin, PluginHelpText
import json
from API.actions.group.message import sendGroupMessage
from API.types import GroupMessage, GroupMemberAdd
from settings import PATH


def sendNotice(groupId, content):
    sendGroupMessage(groupId, msg=content)


class Essential(Plugin):
    def __init__(self):
        self.notices = {}
        self.threads = {}

    def on_command_setNotice(self, command: dict, event: GroupMessage):
        # 内容: content， 时间: time， 是否提醒新成员: sendToNewMember
        if "content" not in command or "time" not in command:
            return self.setNotice_helper()
        content = command["content"]
        time = command["time"]
        groupId = event.groupId
        if time.find(":") == -1:
            return self.setNotice_helper()
        sendToNewMember = False
        if "sendToNewMember" in command:
            sendToNewMember = True
        data = json.load(open(os.path.join(PATH, "plugins/essential/notice.json"), "r", encoding="utf8"))
        if f"{groupId}" not in data:
            data[f"{groupId}"] = {"notices": {}, "_id": 0}
        data[f"{groupId}"]["_id"] += 1
        _id = data[f"{groupId}"]["_id"]
        data[f"{groupId}"]["notices"][str(_id)] = {"content": content, "time": time, "sendToNewMember": sendToNewMember, "creator": event.sender.name + f"({event.sender.userId})"}
        json.dump(data, open(os.path.join(PATH, "plugins/essential/notice.json"), "w", encoding="utf8"), indent=4)
        self.notices = data.copy()
        if groupId not in self.threads:
            self.threads[groupId] = {}
        self.threads[groupId][_id] = threading.Thread(target=self.sendNoticeByTime, args=(str(groupId), str(_id)))
        self.threads[groupId][_id].start()
        return "设置成功"

    def setNotice_helper(self):
        text = PluginHelpText("setNotice")
        text.addArg("content", "设置公告的内容", "公告的内容", ["string"], isBoolArg=False)
        text.addArg("time", "设置公告发送的时间", "小时:分(英文冒号)", ["string"], isBoolArg=False)
        text.addArg("sendToNewMember", "是否提醒新成员", "", [], isBoolArg=True, isNeeded=False)
        text.addExample("-content:114514,1919810 -time:1:0", "每天凌晨1发公告")
        text.addExample("-content:114514,1919810 -time:1:0 -sendToNewMember", "每天凌晨1发公告, 但是新成员也提醒")
        text.addExample("-content:`aaaaaaaaaa bbbbbbbbbbb cccccccc \n cccccccccc` -time:1:0 -sendToNewMember",
                        "每天凌晨1发公告, 但是新成员也提醒")
        return text.generate()

    def get_permission_setNotice(self):
        return Permissions.admin

    def on_load(self):
        data = json.load(open(os.path.join(PATH, "plugins/essential/notice.json"), "r", encoding="utf8"))
        self.notices = data.copy()
        for group in self.notices:
            for i in self.notices[group]["notices"]:
                if int(group) not in self.threads:
                    self.threads[int(group)] = {}
                self.threads[int(group)][i] = threading.Thread(target=self.sendNoticeByTime, args=(group, i))
                self.threads[int(group)][i].start()

    def on_remove(self):
        for group in self.threads:
            for thread in self.threads[group]:
                stopThread(self.threads[group][thread])

    def on_group_member_add(self, event: GroupMemberAdd):
        for notice in self.notices[str(event.groupId)]:
            if notice["sendToNewMember"]:
                sendNotice(event.groupId, notice["content"])

    def sendNoticeByTime(self, groupId, i):
        # print(self.notices)
        time = self.notices[groupId]["notices"][i]["time"].split(":")
        hour = int(time[0])
        minute = int(time[1])
        while 1:
            # print(datetime.datetime.now().hour, datetime.datetime.now().minute)
            while not (datetime.datetime.now().minute == minute and datetime.datetime.now().hour == hour): timer.sleep(
                5)
            sendNotice(int(groupId), self.notices[groupId]["notices"][i]["content"])
            while not (datetime.datetime.now().minute != minute and datetime.datetime.now().hour != hour): timer.sleep(
                5)
