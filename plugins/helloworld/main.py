from API.permission import Permissions
from API.plugin import PluginHelpText, Plugin


class HelloWorld(Plugin):
    def __init__(self):
        super(HelloWorld, self).__init__()

    def helloworld_helper(self):
        helpText = PluginHelpText("helloworld")
        helpText.addExample("", "打印helloworld")
        helpText = helpText.generate()
        return helpText

    def on_command_helloworld(self, command, fullEvent):
        return "Hello World !!!"

    def get_permission_helloworld(self):
        return Permissions.member
