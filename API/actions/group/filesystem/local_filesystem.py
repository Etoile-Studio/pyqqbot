import os
import sqlite3
import threading
import time
from settings import PATH, SYNC_TIME
from API.types import File, Folder
from API.actions.group.__file import findFileInFolder, _listDir


def LFSFolderToFolder(data):
    folder = {}
    folder["group_id"] = data["groupId"]
    folder["folder_id"] = data["folderId"]
    folder["folder_name"] = data["name"]
    folder["create_time"] = data["createTime"]
    folder["creator"] = data["creator"]
    folder["creator_name"] = data["creatorName"]
    folder["total_file_count"] = data["totalFileCount"]
    return Folder(folder)


def LFSFileToFile(data):
    file = {}
    file["group_id"] = data["groupId"]
    file["file_id"] = data["fileId"]
    file["file_name"] = data["name"]
    file["busid"] = data["busid"]
    file["file_size"] = data["fileSize"]
    file["upload_time"] = data["uploadTime"]
    file["dead_time"] = data["deadTime"]
    file["modify_time"] = data["modifyTime"]
    file["download_times"] = data["downloadTimes"]
    file["uploader"] = data["uploader"]
    file["uploader_name"] = data["uploaderName"]
    return File(file)


class LocalFileSystem:
    def __init__(self):
        self.connect = sqlite3.connect(os.path.join(PATH, "API/actions/group/filesystem/filesystem.db"))
        self.cursor = self.connect.cursor()
        self._init()
        self.syncLock = {}
        self.syncTask = {}

    def _init(self):
        sql = "create table IF NOT EXISTS folder(ID INTEGER PRIMARY KEY  ,groupId INTEGER, name TEXT,folderId TEXT,createTime INTEGER,creator INTEGER,creatorName TEXT,totalFileCount INTEGER);"
        self.cursor.execute(sql)
        sql = "create table IF NOT EXISTS groupFileSystem(ID INTEGER PRIMARY KEY AUTOINCREMENT ,groupId INTEGER,fileCount INTEGER,maxCount INTEGER,usedSpace INTEGER,totalSpace INTEGER);"
        self.cursor.execute(sql)
        sql = "create table IF NOT EXISTS file(ID INTEGER PRIMARY KEY AUTOINCREMENT ,groupId INTEGER,name TEXT,fileId TEXT,busid INTEGER,fileSize INTEGER,uploadTime INTEGER,deadTime INTEGER,modifyTime INTEGER,downloadTimes INTEGER,uploader INTEGER,uploaderName TEXT, parentFolderId TEXT);"
        self.cursor.execute(sql)
        self.connect.commit()

    def getFileIdByName(self, groupId, fileName):
        sql = f"select * from file where groupId = {groupId} and name = '{fileName}';"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if len(result) != 0:
            return result[0][4]
        return 0

    def unlockSync(self, groupId, isInit=False):
        if not isInit:
            if self.syncTask[groupId]:
                return
        self.syncLock[groupId] = False

    def startSync(self, groupId):
        if groupId not in self.syncLock:
            self.unlockSync(groupId, True)
            threading.Thread(target=self.syncFileSystem, args=(groupId,)).start()
            threading.Thread(target=self.syncTimer, args=(groupId, )).start()

    def syncTimer(self, groupId):
        while 1:
            time.sleep(SYNC_TIME)
            self.unlockSync(groupId)

    def syncFileSystem(self, groupId):
        while True:
            while self.syncLock[groupId]:
                time.sleep(1)
            self.syncTask[groupId] = True
            root = _listDir(groupId)
            files = root["files"] if root["files"] is not None else []
            folders = root["folders"] if root["folders"] is not None else []
            for file in files:
                self.setFile(File(file))
            for folder in folders:
                self.recordFolder(groupId, folder)
            self.syncLock[groupId] = True
            self.syncTask[groupId] = True

    def isSyncing(self, groupId):
        return self.syncTask[groupId]

    def recordFolder(self, groupId, folder):
        self.setFolder(Folder(folder))
        fileList = _listDir(groupId, folder.id)
        files = fileList["files"] if fileList["files"] is not None else []
        folders = fileList["folders"] if fileList["folders"] is not None else []
        for file in files:
            self.setFile(File(file))
        for folder in folders:
            self.recordFolder(groupId, folder)

    def getFolderByFolderId(self, groupId, folderId):
        sql = f"select * from folder where groupId = {groupId} and folderId = '{folderId}';"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if len(result) == 0:
            self.unlockSync(groupId)
            return -1
        return LFSFolderToFolder(result[0])

    def getFolderByFolderName(self, groupId, folderName):
        sql = f"select * from folder where groupId = {groupId} and folderName = '{folderName}';"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if len(result) == 0:
            self.unlockSync(groupId)
            return -1
        return LFSFolderToFolder(result[0])

    def getFileByFileName(self, groupId, fileName):
        sql = f"select * from file where groupId = {groupId} and fileName = '{fileName}';"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if len(result) == 0:
            self.unlockSync(groupId)
            return -1
        returns = []
        for res in result:
            returns = LFSFileToFile(res)
        return returns

    def getFileByFileId(self, groupId, fileId):
        sql = f"select * from file where groupId = {groupId} and fileId = '{fileId}';"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if len(result) == 0:
            self.unlockSync(groupId)
            return -1
        return LFSFileToFile(result[0])

    def removeFile(self, groupId, fileId):
        sql = f"delete from file where groupId = {groupId} and fileId = {fileId}"
        self.cursor.execute(sql)
        self.connect.commit()

    def removeFolder(self, groupId, folderId):
        sql = f"delete from folder where groupId = {groupId} and folderId = {folderId}"
        self.cursor.execute(sql)
        self.connect.commit()

    def setFile(self, data: File):
        sql = f"select * from file where groupId = {data.groupId} and fileId = '{data.id}';"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if len(result) == 0:
            sql = f"select fileCount, maxCount, usedSpace, totalSpace from groupFileSystem where groupId = {data.groupId}"
            self.cursor.execute(sql)
            fileCount, maxCount, usedSpace, totalSpace = self.cursor.fetchone()
            if fileCount + 1 > maxCount or usedSpace + data.size > totalSpace:
                return -1
            folderId = findFileInFolder(data.groupId, data.id, "/")
            sql = f"update folder set totalFileCount = totalFileCount+1 where groupId = {data.groupId}, folderId = {folderId}"
            self.cursor.execute(sql)
            sql = f"update groupFileSystem set fileCount = fileCount+1 and totalSpace = totalSpace + {data.size} where groupId = {data.groupId}"
            self.cursor.execute(sql)
            sql = f"insert into file (groupId, name, fileId, busid, fileSize, uploadTime, deadTime, modifyTime, downloadTimes, uploader, uploaderName, parentFolderId) " \
                  f"VALUES ({data.groupId}, '{data.name}', '{data.id}', {data.busid}, {data.size}, {data.uploadTime}, {data.expireTime}, {data.lastModifyTime}, {data.downloadTimes}, {data.uploaderId}, '{data.uploaderName}', '{folderId}')"
            self.cursor.execute(sql)
            self.connect.commit()
            return 1
        if data.lastModifyTime != result[0][8]:
            self.removeFile(data.groupId, data.id)
            return self.setFile(data)
        return 0

    def setFolder(self, data: Folder):
        sql = f"select * from folder where groupId = {data.groupId} and folderId = '{data.id}';"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if len(result) == 0:
            sql = f"insert into folder (groupId, name, folderId, createTime, creator, creatorName, totalFileCount) " \
                  f"VALUES ({data.groupId}, '{data.name}', '{data.id}', {data.createTime}, {data.creatorId}, '{data.creatorName}', {data.totalFileCount})"
            self.cursor.execute(sql)
            self.connect.commit()
            return 1
        return 0

