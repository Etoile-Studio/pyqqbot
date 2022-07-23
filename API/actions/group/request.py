import requests
from settings import HTTP_PORT, HTTP_HOST


def agreeGroupAddRequest(flag: str, subType: str):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/set_group_add_request",
        data={
            "flag": flag,
            "sub_type": subType,
            "approve": True,
            "reason": ""
        }
    ).json()


def disagreeGroupAddRequest(flag: str, subType: str, reason: str):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/set_group_add_request",
        data={
            "flag": flag,
            "sub_type": subType,
            "approve": False,
            "reason": reason
        }
    ).json()
