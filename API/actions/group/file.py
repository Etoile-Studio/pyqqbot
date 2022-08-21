import requests

from API.actions.group.misc import _listDir
from settings import HTTP_PORT, HTTP_HOST
from API.types import FileSystemInfo, Folder, File


def getFileById(groupId, fileId, folderId="/"):
    """别用，我觉得你用会出问题"""
    result = _listDir(groupId, folderId)
    if result["files"] is None:
        return -1
    for file in result["files"]:
        if file["file_id"] == fileId:
            return File(file)
    if result["folders"] is None:
        return -1
    for folder in result["folders"]:
        res = getFileById(groupId, fileId, folder["folder_id"])
        if res != -1:
            return res
    return -1


def getFileByName(groupId, fileName, folderId="/"):
    """别用，我觉得你用会出问题"""
    result = _listDir(groupId, folderId)
    if result["files"] is None:
        return -1
    for file in result["files"]:
        if file["file_name"] == fileName:
            return File(file)
    if result["folders"] is None:
        return -1
    for folder in result["folders"]:
        res = getFileByName(groupId, fileName, folder["folder_id"])
        if res != -1:
            return res
    return -1


def getFolderByName(groupId, folderName, folderId="/"):
    """别用，我觉得你用会出问题"""
    result = _listDir(groupId, folderId)
    if result["folders"] is None:
        return -1
    for folder in result["folders"]:
        if folder["folder_name"] == folderName:
            return Folder(folder)
        res = getFolderByName(groupId, folderName, folder["folder_id"])
        if res != -1:
            return res
    return -1


def getFolderById(groupId, folderId, searchFolderId="/"):
    """别用，我觉得你用会出问题"""
    result = _listDir(groupId, searchFolderId)
    if result["folders"] is None:
        return -1
    for folder in result["folders"]:
        if folder["folder_id"] == folderId:
            return Folder(folder)
        res = getFolderById(groupId, folderId, folder["folder_id"])
        if res != -1:
            return res
    return -1


def getFileSystemInfo(groupId):
    data = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/upload_group_file",
        data={
            "group_id": groupId,
        }
    ).json()
    if data["status"].lower() in ["ok", "async"]:
        return FileSystemInfo(data["data"])
    return -1, data["msg"]


def uploadToFolderByFolderName(groupId, filePath: str, fileName: str, folderName: str = "/"):
    """谨慎用啊，可能会导致风控，因为每次都会使用api遍历一遍云端的文件系统"""
    folderId = getFolderByName(groupId, folderName)
    if folderId == -1:
        return -1, "FOLDER_NOT_EXISTS"
    return uploadToFolderByFolderId(filePath, fileName, folderId.id)


def uploadToFolderByFolderId(groupId, filePath: str, fileName: str, folderId: str = "/"):
    data = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/upload_group_file",
        data={
            "group_id": groupId,
            "file": filePath,
            "name": fileName,
            "folder": folderId
        }
    ).json()
    if data["status"].lower() in ["ok", "async"]:
        return "ok"
    return -1, data["msg"]


def listDir(groupId, folderId="/"):
    result = _listDir(groupId, folderId)
    returns = {"folders": [], "files": []}
    result["files"] = result["files"] if result["files"] is not None else []
    result["folders"] = result["folders"] if result["folders"] is not None else []
    for folder in result["folders"]:
        returns["folders"].append(Folder(folder))
    for file in result["files"]:
        returns["files"].append(File(file))
    return returns


def makeDir(groupId, folderName):
    """此函数有点问题，请先别用"""
    return requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/create_group_file_folder",
        data={
            "group_id": groupId,
            "name": folderName,
            "parent_id": "/"
        }
    ).json()


def downloadFile(groupId, fileId, busid):
    data = requests.post(
        f"http://{HTTP_HOST}:{HTTP_PORT}/get_group_file_url",
        data={
            "group_id": groupId,
            "file_id": fileId,
            "busid": busid
        }
    ).json()
    if data["status"].lower() in ["ok", "async"]:
        returns = requests.get(
            data["data"]["url"]
        ).content
        return returns
    return -1, data["msg"]


def removeById(groupId, Id, busid=None, isFolder=False):
    if not isFolder:
        data = requests.post(
            f"http://{HTTP_HOST}:{HTTP_PORT}/delete_group_file",
            data={
                "group_id": groupId,
                "file_id": Id,
                "busid": busid
            }
        ).json()
    else:
        data = requests.post(
            f"http://{HTTP_HOST}:{HTTP_PORT}/delete_group_folder",
            data={
                "group_id": groupId,
                "folder_id": Id,
            }
        ).json()
    if data["status"].lower() in ["ok", "async"]:
        return "ok"
    return -1, data["msg"]


def removeByName(groupId, name, busid=None, isFolder=False):
    """谨慎用啊，可能会导致风控，因为每次都会使用api遍历一遍云端的文件系统"""
    if isFolder:
        Id = getFolderByName(groupId, name)
    else:
        Id = getFileByName(groupId, name)
    if Id == -1:
        return -1, "NOT_EXISTS"
    return removeById(groupId, Id.id, busid, isFolder)


def isFileExistsByName(groupId, fileName, folderId="/"):
    if getFileByName(groupId, fileName, folderId) == -1:
        return False
    return True


def isFileExistsById(groupId, fileId, folderId="/"):
    if getFileById(groupId, fileId, folderId) == -1:
        return False
    return True


def isFolderExistsByName(groupId, folderName, folderId="/"):
    if getFolderByName(groupId, folderName, folderId) == -1:
        return False
    return True


def isFolderExistsById(groupId, folderId, searchFolderId="/"):
    if getFolderById(groupId, folderId, searchFolderId) == -1:
        return False
    return True

