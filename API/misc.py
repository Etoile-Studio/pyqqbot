import inspect
import os.path

from settings import PATH_BLACKLIST, LOGGER


def getClasses(arg):
    classes = []
    classMembers = inspect.getmembers(arg, inspect.isclass)
    for (_, cls) in classMembers:
        classes.append(cls)
    return classes


def getCommandListener(_class):
    funcMember = inspect.getmembers(_class, inspect.ismethod)
    onCommand = {"exec": [], "helper": {}, "permission": {}}
    names = []
    for mem in funcMember:
        if mem[0].startswith("on_command_"):
            name = mem[0].lstrip("on_command_")
            onCommand["exec"].append((name, mem[1]))
            names.append(name)
    for mem in funcMember:
        if mem[0].rstrip("_helper") in names:
            onCommand["helper"][mem[0].rstrip("_helper")] = mem[1]
        if mem[0].lstrip("get_permission_") in names:
            onCommand["permission"][mem[0].lstrip("get_permission_")] = mem[1]()
    return onCommand


def removeMiscPath(paths: list):
    for blockedPath in PATH_BLACKLIST:
        while paths.count(blockedPath):
            paths.remove(blockedPath)
    # LOGGER.info(paths)
    return paths


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)
