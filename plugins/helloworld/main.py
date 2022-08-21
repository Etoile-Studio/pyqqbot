from API.plugin import PluginHelpText, Plugin
from API.actions.group.message import sendGroupMessage


class HelloWorld(Plugin):
    def __init__(self):
        super(HelloWorld, self).__init__("helloworld")

    def helper(self):
        helpText = PluginHelpText(self.name)
        helpText.addExample("", "打印helloworld")
        helpText = helpText.generate()
        return helpText

    def on_command(self, command, fullEvent):
        return "Hello World !!!"

    def on_group_message(self, event):
        sendGroupMessage(event.groupId, event.rawMessage + "!")
