import os
import threading
import time
from importlib import import_module

from API.actions import cqcode
from API.actions.group.message import sendGroupMessage
from API.permission import Permissions, setMemberPermissionCommand, havePermission, setMemberPermissionCommandHelper, \
    getMemberPermissionCommand, getMemberPermissionCommandHelper
from API.types import GroupMessage, UploadGroupFile, GroupMemberAdd, GroupMemberLeave, GroupAddRequest
from settings import PLUGIN_PATH, PLUGIN_PACKAGE, LOGGER, PLUGIN_LIST, QQ_ID
from API.plugin import Plugin, PluginHelpText
from API.misc import removeMiscPath, getClasses, getCommandListener
from command_spilter import splitCommand

plugins = PLUGIN_LIST
reloading = False
permissionName = ["member", "admin", "owner"]


def loadPlugins():
    global plugins
    global reloading
    reloading = True
    LOGGER.info("loading plugins")
    for plugin in plugins["on_remove"]:
        plugin()
    plugins = PLUGIN_LIST.copy()
    pluginDirs = removeMiscPath(os.listdir(PLUGIN_PATH))
    plugins["on_command"].append({"help": {"exec": helper, "helper": helperHelper, "permission": Permissions.member}})
    plugins["on_command"].append({"setMemberPermission": {"exec": setMemberPermissionCommand,
                                                          "helper": setMemberPermissionCommandHelper,
                                                          "permission": Permissions.owner}})
    plugins["on_command"].append({"getMemberPermission": {"exec": getMemberPermissionCommand,
                                                          "helper": getMemberPermissionCommandHelper,
                                                          "permission": Permissions.member}})
    plugins["on_command"].append({"reload": {"exec": reload, "helper": reloadHelper, "permission": Permissions.owner}})
    for pluginDir in pluginDirs:
        try:
            plugin = import_module(f"{PLUGIN_PACKAGE}.{pluginDir}.main")
            plugin_classes = getClasses(plugin)
            for plugin_class in plugin_classes:
                if Plugin in plugin_class.__bases__:
                    initedPluginClass = plugin_class()
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

                    if plugin_class.on_remove != Plugin.on_remove:
                        plugins["on_remove"].append(initedPluginClass.on_remove)

                    initedPluginClass.on_load()

                    onCommands = getCommandListener(initedPluginClass)
                    for command in onCommands["exec"]:
                        name = command[0]
                        # print(onCommands)
                        flag = True
                        for plug in plugins["on_command"]:
                            if name in plug.keys():
                                LOGGER.error(
                                    f"Plugin class {plugin_class.__name__} has the same name as a plugin. Please rename the command")
                                flag = False
                                break
                        if flag:
                            plugins["on_command"].append(
                                {name: {"exec": command[1], "helper": onCommands["helper"][name],
                                        "permission": onCommands["permission"][name]}})
        except ImportError:
            LOGGER.error(f"Plugin {pluginDir} doesn't have an entrance. Please add main.py to the plugin")
    LOGGER.info("finish loading")
    reloading = False


def executeCommand(rawCommand, fullEvent):
    while reloading:
        time.sleep(0.1)
    if rawCommand.strip() == "":
        menu(fullEvent["group_id"], fullEvent["user_id"])
        return None
    command = splitCommand(rawCommand)
    if type(command) == tuple:
        LOGGER.info("用户请求命令时参数出错")
        return command[1]
    for plugin in plugins["on_command"]:
        if command["exec"] in plugin.keys():
            if havePermission(fullEvent["group_id"], fullEvent["user_id"], plugin[command["exec"]]["permission"]):
                return plugin[command["exec"]]["exec"](command["args"], GroupMessage(fullEvent))
            return "没有权限"
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
    if "exec" not in command:
        return helperHelper()
    for plugin in plugins["on_command"]:
        if command["exec"] in plugin.keys():
            return plugin[command["exec"]]["helper"]()
    LOGGER.error("用户请求不存在的命令")
    return "您请求的命令不存在"


def helperHelper():
    text = PluginHelpText("help")
    text.addArg("exec", "指定您需要命令的帮助文档", "命令", ["string"], False)
    text.addExample("-exec:help", "打印help命令的文档")
    return text.generate()


def reload(command, event):
    loadPlugins()
    return "加载成功"


def reloadHelper():
    text = PluginHelpText("reload")
    text.addExample("", "重新加载插件")
    return text.generate()


def menu(groupId, userId):
    while reloading:
        time.sleep(0.1)
    text = f"{cqcode.at(userId)}\n=====主菜单=====\n"
    text += "命令:\n"
    for exe in plugins["on_command"]:
        commandName = list(exe.keys())[0]
        text += f"\t{commandName} 权限: {permissionName[exe[commandName]['permission']]}\n"
    text += f"使用{cqcode.at(QQ_ID)} help -exec:(命令名) 来查询指令用法"
    sendGroupMessage(groupId, text)
