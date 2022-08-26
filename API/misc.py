import inspect
import os.path
import ctypes
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
        # print(mem[0].removesuffix("_helper"))
        if mem[0].removesuffix("_helper") in names:
            # print(mem[0].removesuffix("_helper"))
            onCommand["helper"][mem[0].removesuffix("_helper")] = mem[1]
        if mem[0].removeprefix("get_permission_") in names:
            onCommand["permission"][mem[0].removeprefix("get_permission_")] = mem[1]()
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





def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stopThread(thread):
    _async_raise(thread.ident, SystemExit)
