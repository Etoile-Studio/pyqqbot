import os
import threading
import time
from importlib import import_module

from API.types import PrivateMessage, GroupMessage, UploadGroupFile, GroupMemberAdd, GroupMemberLeave, GroupAddRequest
from settings import PLUGIN_PATH, PLUGIN_PACKAGE, LOGGER, PLUGIN_LIST
from API.plugin import Plugin, PluginHelpText
from API.misc import removeMiscPath, getClasses
from command_spilter import splitCommand

plugins = PLUGIN_LIST
reloading = False


def loadPlugins():
    global plugins
    global reloading
    reloading = True
    LOGGER.info("loading plugins")
    plugins = PLUGIN_LIST
    pluginDirs = removeMiscPath(os.listdir(PLUGIN_PATH))
    plugins["on_command"].append({"help": {"exec": helper, "helper": helperHelper}})
    for pluginDir in pluginDirs:
        try:
            plugin = import_module(f"{PLUGIN_PACKAGE}.{pluginDir}.main")
            plugin_classes = getClasses(plugin)
            for plugin_class in plugin_classes:
                if Plugin in plugin_class.__bases__:
                    initedPluginClass = plugin_class()
                    name = initedPluginClass.getName()
                    if plugin_class.on_group_add_request != Plugin.on_group_add_request:
                        plugins["on_group_add_request"].append(initedPluginClass.on_group_add_request)

                    if plugin_class.on_group_member_add != Plugin.on_group_member_add:
                        plugins["on_group_member_add"].append(initedPluginClass.on_group_member_add)

                    if plugin_class.on_group_member_leave != Plugin.on_group_member_leave:
                        plugins["on_group_member_leave"].append(initedPluginClass.on_group_member_leave)

                    if plugin_class.on_group_file != Plugin.on_group_file:
                        plugins["on_group_file"].append(initedPluginClass.on_group_file)

                    if plugin_class.on_group_message != Plugin.on_group_message:
                        plugins["on_group_message"].append(initedPluginClass.on_group_message)

                    if plugin_class.on_group_anonymous_message != Plugin.on_group_anonymous_message:
                        plugins["on_group_anonymous_message"].append(initedPluginClass.on_group_anonymous_message)

                    if plugin_class.on_command != Plugin.on_command:
                        flag = True
                        for plug in plugins["on_command"]:
                            if name in plug.keys():
                                LOGGER.error(
                                    f"Plugin class {plugin_class.__name__} has the same name as a plugin. Please rename the command")
                                flag = False
                                break
                        if flag:
                            plugins["on_command"].append(
                                {name: {"exec": initedPluginClass.on_command, "helper": initedPluginClass.helper, "permission": initedPluginClass.permissionLevel}})
        except ImportError:
            LOGGER.error(f"Plugin {pluginDir} doesn't have an entrance. Please add main.py to the plugin")
    LOGGER.info("finish loading")
    reloading = False


def executeCommand(rawCommand, fullEvent):
    while reloading:
        time.sleep(0.1)
    command = splitCommand(rawCommand)
    if type(command) == tuple:
        LOGGER.info("用户请求命令时参数出错")
        return command[1]
    for plugin in plugins["on_command"]:
        if command["exec"] in plugin.keys():
            return plugin[command["exec"]]["exec"](command["args"], GroupMessage(fullEvent) if fullEvent[
                                                                                                   "message_type"] == "group" else PrivateMessage(
                fullEvent))
    LOGGER.error("用户请求不存在的命令")
    return "您请求的命令不存在"


def executeEvent(eventType, fullEvent):
    while reloading:
        time.sleep(0.1)
    args = False
    match eventType:
        case "on_group_message":
            args = (GroupMessage(fullEvent),)
        case "on_group_file":
            args = (UploadGroupFile(fullEvent))
        case "on_group_member_add":
            args = (GroupMemberAdd(fullEvent),)
        case "on_group_member_leave":
            args = (GroupMemberLeave(fullEvent),)
        case "on_group_add_request":
            args = (GroupAddRequest(fullEvent),)
        case "on_group_anonymous_message":
            args = (GroupMessage(fullEvent),)
    if not args:
        LOGGER.info("暂不支持此event")
        return
    for plugin in plugins[f"{eventType}"]:
        threading.Thread(target=plugin, args=args).start()


def helper(command, event):
    LOGGER.info(command)
    if "exec" not in command:
        return helperHelper()
    for plugin in plugins["on_command"]:
        if command["exec"] in plugin.keys():
            return plugin[command["exec"]]["helper"]()
    LOGGER.error("用户请求不存在的命令")
    return "您请求的命令不存在"


def helperHelper():
    text = PluginHelpText("help")
    text.addArg("exec", "指定您需要命令的帮助文档", "命令", "string")
    text.addExample("-exec:help", "打印help命令的文档")
    return text.generate()

