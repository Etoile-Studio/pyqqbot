from API.actions.cqcode import at
from settings import QQ_ID
from API.types import PrivateMessage, GroupMessage, UploadGroupFile, GroupMemberAdd, GroupMemberLeave, GroupAddRequest


class PluginHelpText:
    def __init__(self, name):
        self.name = name
        self.arguments = []
        self.examples = []

    def addArg(self, name, descriptions, valueName, types, isBoolArg=True):
        if isBoolArg:
            self.arguments.append(f"\t-{name} {descriptions}")
            return
        self.arguments.append(f"\t-{name}:<{valueName}[{', '.join(types)}]> {descriptions}")

    def addExample(self, command, descriptions):
        self.examples.append(f"\t{at(QQ_ID)} {self.name} {command} {descriptions}")

    def generate(self):
        helpText = f"====={self.name}的用法=====\n"
        if len(self.arguments):
            helpText += "参数:\n"
            helpText += "\n".join(self.arguments)
        else:
            helpText += "\t无参数"
        helpText += '\n'
        if len(self.examples):
            helpText += "示例:\n"
            helpText += "\n".join(self.examples)
        return helpText


class Plugin:
    """
    所有plugin的父类，必须extend才会被识别
    """

    def __init__(self, name, permissionLevel):
        """
        :param name: plugin的命名（只有在此插件有command时才重要，但必须填）
        :param permissionLevel: 命令总体权限，可为all, admin
        """
        self.name = name
        self.permissionLevel = permissionLevel

    def helper(self):
        """
        这玩意儿是给自带插件helper用的\n
        比如：\n
        helpText = PluginHelpText(self.name)\n
        helpText.addExample("", "打印helloworld")\n
        helpText = helpText.generate()\n
        return helpText\n
        :return: str格式的格式化后的帮助文本
        """
        ...

    def on_group_message(self, event: GroupMessage):
        """
        当收到群消息时执行（命令除外）\n
        :param event: 完整的事件参数，见官方文档 https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%B6%88%E6%81%AF
        :return: str格式的返回文本或None（如果你不想用默认的消息返回或没有返回消息）
        """
        ...

    def on_group_anonymous_message(self, event: GroupMessage):
        """
        当收到群匿名消息时执行（命令除外）\n
        :param event: 完整的事件参数，见官方文档 https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%B6%88%E6%81%AF
        :return: str格式的返回文本或None（如果你不想用默认的消息返回或没有返回消息）
        """
        ...

    def on_command(self, command: dict, event: GroupMessage | PrivateMessage):
        """
        当收到命令时执行\n
        此时收到的命令有可能是来自群聊或临时会话的，如果不想用默认返回消息方式，请做好判断\n
        :param command: 处理过后的command参数
        :param event: 完整的事件参数，见官方文档 https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%B6%88%E6%81%AF
        :return: str格式的返回文本或None（如果你不想用默认的消息返回或没有返回消息）
        """
        ...

    def on_group_file(self, event: UploadGroupFile):
        """
        当收到文件上传时执行\n
        不会返回任何数据，请自行返回\n
        :param event: 完整的事件参数，见官方文档 https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0
        :return: None(如有消息请自行返回)
        """
        ...

    def on_group_member_add(self, event: GroupMemberAdd):
        """
        当有人进群时执行\n
        不会返回任何数据，请自行返回\n
        :param event: 完整的事件参数，见官方文档 https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E5%A2%9E%E5%8A%A0
        :return: None(如有消息请自行返回)
        """
        ...

    def on_group_member_leave(self, event: GroupMemberLeave):
        """
        当有人退群时执行\n
        不会返回任何数据，请自行返回\n
        :param event: 完整的事件参数，见官方文档 https://docs.go-cqhttp.org/event/#%E7%BE%A4%E6%88%90%E5%91%98%E5%87%8F%E5%B0%91
        :return: None(如有消息请自行返回)
        """
        ...

    def on_group_add_request(self, event: GroupAddRequest):
        """
        当有人提交加群申请时执行\n
        不会返回任何数据，请自行返回\n
        建议配合on_group_member_add食用\n
        :param event: 完整的事件参数，见官方文档 https://docs.go-cqhttp.org/event/#%E5%8A%A0%E7%BE%A4%E8%AF%B7%E6%B1%82-%E9%82%80%E8%AF%B7
        :return: None(如有消息请自行返回)
        """
        ...

    def getName(self):
        """
        请勿更改
        """
        return self.name
