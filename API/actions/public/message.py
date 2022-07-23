import requests
from settings import HTTP_PORT, HTTP_HOST


def deleteMessage(messageId: int):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/delete_msg",
        data={
            "message_id": messageId
        }
    ).json()


def getMessage(messageId: int):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/get_msg",
        data={
            "message_id": messageId
        }
    ).json()


def getImage(cachedFileName: str):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/get_image",
        data={
            "file": cachedFileName
        }
    ).json()
