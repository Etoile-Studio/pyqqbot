# @aaaaa bbb -xxx -xxxa:ad -aa -yyy:`xx x`
"""
{"xxx":}
"""


def _spliter(command: str):
    if command.count("`") % 2 != 0:
        return None
    command = command.split("`")
    while command.count(""):
        command.remove("")
    new_command = []
    isString = False
    for word in command:
        if isString:
            isString = False
            new_command[-1] += word
            continue
        if word[-1] == ":":
            isString = True
        new_command += word.split(" ")
    while new_command.count(""):
        new_command.remove("")
    return new_command


def splitCommand(command: str):
    commandArguments = _spliter(command)
    if commandArguments is None:
        return None, f"命令处理出错：“`”不为偶数。"
    command = {
        "exec": commandArguments[0],
        "args": {}
    }
    commandArguments.pop(0)
    print(commandArguments)
    for commandArgument in commandArguments:
        if commandArgument[0] != '-':
            return None, f"命令处理出错：不正确的语法\"{commandArgument}\"，您是不是指\"-{commandArgument}\""
        commandArgument = commandArgument.lstrip("-")
        print(commandArgument)
        kw = commandArgument.find(":")
        if kw == -1:
            command["args"][commandArgument] = True
        else:
            key = commandArgument[0:kw]
            value = commandArgument[kw + 1:len(commandArgument)]
            print(key, value)
            if key in command["args"]:
                if type(command["args"][key]) == list:
                    command["args"][key].append(value)
                else:
                    command["args"][key] = [command["args"][key], value]
            else:
                command["args"][key] = value
    print(command)
    return command

