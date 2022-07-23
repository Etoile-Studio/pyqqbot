import requests
from settings import HTTP_PORT, HTTP_HOST


def sendPrivateMessage(groupId: int, toUser: int, msg: str, rawContent: bool = False):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/send_private_msg",
        data={
            "group_id": groupId,
            "user_id": toUser,
            "auto_escape": rawContent,
            "message": msg
        }
    ).json()
