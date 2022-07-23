import requests
from settings import HTTP_PORT, HTTP_HOST


class ForwardMessage:
    def __init__(self):
        self.messages = []

    def addPreviousMessage(self, messageId: int):
        self.messages.append({
            "type": "node",
            "data": {
                "id": messageId
            }
        })

    def addCustomMessage(self, customDisplayName: str, customUserId: int, rawMessage: str):
        self.messages.append({
            "type": "node",
            "data": {
                "name": customDisplayName,
                "uin": customUserId,
                "content": rawMessage
            }
        })

    def getData(self):
        return self.messages


def sendGroupMessage(groupId: int, msg: str, rawContent: bool = False):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/send_group_msg",
        data={
            "group_id": groupId,
            "auto_escape": rawContent,
            "message": msg
        }
    ).json()


def sendGroupTogetherForwardMessage(groupId: int, msgNodes: ForwardMessage):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/send_group_forward_msg",
        data={
            "group_id": groupId,
            "messages": msgNodes.getData()
        }
    ).json()


def getForwardMessage(messageId: int):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/get_forward_msg",
        data={
            "message_id": messageId
        }
    ).json()
