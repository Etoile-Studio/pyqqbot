import requests
from settings import HTTP_PORT, HTTP_HOST
from API.types import ForwardMessage


class ForwardMessageGenerator:
    """目前api有点问题，不建议用"""

    def __init__(self):
        self.messages = []

    def addPreviousMessage(self, messageId: int):
        self.messages.append({
            "type": "node",
            "data": {
                "id": str(messageId)
            }
        })

    def addCustomMessage(self, customDisplayName: str, customUserId: int, rawMessage: str):
        self.messages.append({
            "type": "node",
            "data": {
                "name": customDisplayName,
                "uin": str(customUserId),
                "content": rawMessage
            }
        })

    def getData(self):
        return self.messages


def sendGroupMessage(groupId: int, msg: str, rawContent: bool = False) -> int:
    data = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/send_group_msg",
        data={
            "group_id": groupId,
            "auto_escape": rawContent,
            "message": msg
        }
    ).json()
    if data["status"].lower() in ["ok", "async"]:
        return data["data"]["message_id"]
    return -1


def sendGroupTogetherForwardMessage(groupId: int, msgNodes: ForwardMessageGenerator):
    """目前api有点问题，不建议用"""
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/send_group_forward_msg",
        data={
            "group_id": groupId,
            "messages": msgNodes.getData()
        }
    ).json()


def getForwardMessage(messageId: str) -> list[ForwardMessage] | None | int:
    data = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/get_forward_msg",
        data={
            "message_id": messageId
        }
    ).json()
    if data["status"].lower() in ["ok", "async"]:
        returnList = []
        for dat in data["data"]:
            returnList.append(ForwardMessage(dat))
        return returnList
    return -1
