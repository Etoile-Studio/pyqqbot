from API.plugin import PluginHelpText, Plugin
from API.actions import sendGroupMessage


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

    def on_group_message(self, raw_message, fullEvent):
        sendGroupMessage(fullEvent["group_id"], raw_message + "!")
