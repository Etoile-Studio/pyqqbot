import requests
from settings import HTTP_PORT, HTTP_HOST

def findFileInFolder(groupId, fileId, folderId="/"):
    """别用，我觉得你用会出问题"""
    result = _listDir(groupId, folderId)
    if result["files"] is None:
        return -1
    for file in result["files"]:
        if file["file_id"] == fileId:
            return folderId
    if result["folders"] is None:
        return -1
    for folder in result["folders"]:
        res = findFileInFolder(groupId, fileId, folder["folder_id"])
        if res != -1:
            return res
    return -1


def _listDir(groupId, folderId="/"):
    if folderId == "/":
        return requests.post(
            f"http://{HTTP_HOST}:{HTTP_PORT}/get_group_root_files",
            data={
                "group_id": groupId,
            }
        ).json()["data"]
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/get_group_files_by_folder",
        data={
            "group_id": groupId,
            "folder_id": folderId
        }
    ).json()["data"]
