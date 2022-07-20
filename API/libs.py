import inspect
from settings import PATH_BLACKLIST, LOGGER


def getClasses(arg):
    classes = []
    classMembers = inspect.getmembers(arg, inspect.isclass)
    for (_, cls) in classMembers:
        classes.append(cls)
    return classes


def removeMiscPath(paths: list):
    for blockedPath in PATH_BLACKLIST:
        while paths.count(blockedPath):
            paths.remove(blockedPath)
    # LOGGER.info(paths)
    return paths
