import requests
from settings import HTTP_PORT, HTTP_HOST
from API.types import GroupAddRequest


def agreeGroupAddRequest(request: GroupAddRequest):
    data = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/set_group_add_request",
        data={
            "flag": request.flag,
            "sub_type": request.subType,
            "approve": True,
            "reason": ""
        }
    ).json()
    if data["status"].lower() in ["ok", "async"]:
        return "ok"
    return -1


def disagreeGroupAddRequest(request: GroupAddRequest, reason: str):
    data = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/set_group_add_request",
        data={
            "flag": request.flag,
            "sub_type": request.subType,
            "approve": False,
            "reason": reason
        }
    ).json()
    if data["status"].lower() in ["ok", "async"]:
        return "ok"
    return -1
