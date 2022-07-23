import requests
from settings import HTTP_PORT, HTTP_HOST


def uploadGroupFile(groupId: int, filePath: str, fileName: str, folder: str = "/"):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/upload_group_file",
        data={
            "group_id": groupId,
            "file": filePath,
            "name": fileName,
            "folder": folder
        }
    ).json()


def getGroupFileSystemInfo(groupId: int):
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/upload_group_file",
        data={
            "group_id": groupId,
        }
    ).json()


class Explorer:
    def __init__(self, groupId):
        self.groupId = groupId

