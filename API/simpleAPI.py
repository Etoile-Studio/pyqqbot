import os.path
import requests
from settings import GROUP_ID, HTTP_PORT, HTTP_HOST

PATH = os.path.abspath(os.path.dirname(__file__))
STATIC_PATH = os.path.join(PATH, "statics")


def sendMSG(msg: str, rawContent: bool = False) -> None:
    requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/send_group_msg",
        data={
            "group_id": GROUP_ID,
            "auto_escape": rawContent,
            "message": msg
        }
    )
