import asyncio
import json
import signal
import subprocess
import threading
import time
import websockets
from settings import WEBSOCKET_HOST, WEBSOCKET_PORT, QQ_ID, GROUP_ID, LOGGER, BOT_PATH
from API.actions.group.message import sendGroupMessage

"""from API.actions.private.message import sendPrivateMessage"""
from API.actions import cqcode
import manager

proc = subprocess.Popen(args="go-cqhttp.exe -faststart", shell=True, cwd=BOT_PATH,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
initFlag = True


def initPlugin():
    while initFlag: time.sleep(1)
    manager.loadPlugins()


def returnCommandResultGroup(rawMessage, event):
    result = manager.executeCommand(rawMessage, event)
    if result is not None:
        sendGroupMessage(event["group_id"], cqcode.at(
            event["user_id"]) + " " + result)


"""def returnCommandResultPrivate(rawMessage, event):
    result = manager.executeCommand(rawMessage, event)
    if result is not None:
        sendPrivateMessage(event["group_id"], event["user_id"], cqcode.at(
            event["user_id"]) + " " + result)"""


# 从服务器接收数据
async def manage():
    global initFlag
    while 1:
        try:
            # websocket 连接
            async with websockets.connect(f'ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}') as websocket:
                LOGGER.info("连接成功")
                initFlag = False
                while 1:
                    # 处理原始数据
                    recv_event = await websocket.recv()
                    event = json.loads(recv_event)
                    # 元数据上报
                    if event["post_type"] == "meta_event":
                        LOGGER.debug(f"收到一个meta_event: {event['meta_event_type']}")
                        continue
                    # 消息上报
                    if event["post_type"] == "message":
                        if event["sub_type"] == "group_self":
                            continue
                        LOGGER.info(json.dumps(event, indent=4))
                        continueProcess = True
                        # 生成log
                        log = "收到一条消息:\n"
                        log += "来源:"
                        match event["sub_type"]:
                            case "friend":
                                log += "朋友(不做处理)\n"
                            case "group":
                                log += "群临时会话(不做处理)\n"
                            case "normal":
                                log += "群消息\n"
                            case "anonymous":
                                log += "匿名消息\n"
                                continueProcess = False
                            case "notice":
                                log += "群通知(不做处理)\n"
                                continueProcess = False
                        log += f"发送者: {event['user_id']}\n"
                        log += f"id: {event['message_id']}\n"
                        log += f"消息: {event['raw_message']}"
                        LOGGER.info(log)
                        # 判断是否继续处理（匿名消息和群通知不做处理）
                        if continueProcess:
                            # 消息分流
                            rawMessage: str = event["raw_message"]
                            match event["message_type"]:
                                # 来自群的消息
                                case "group":
                                    if event["group_id"] in GROUP_ID:
                                        if event["anonymous"] is not None:
                                            threading.Thread(target=manager.executeEvent,
                                                             args=("on_group_anonymous_message", event)).start()
                                            continue
                                        if rawMessage.find(cqcode.at(QQ_ID)) == 0:
                                            rawMessage = rawMessage.lstrip(cqcode.at(QQ_ID))
                                            threading.Thread(target=returnCommandResultGroup,
                                                             args=(rawMessage, event)).start()
                                            continue
                                        threading.Thread(target=manager.executeEvent,
                                                         args=("on_group_message", event)).start()
                                # 来自私聊或群临时会话，此处命令无需@, 我不想写了
                    if event["post_type"] == "notice":
                        match event["notice_type"]:
                            case "group_upload":
                                LOGGER.info("收到一个群文件...")
                                threading.Thread(target=manager.executeEvent, args=("on_group_file", event)).start()
                            case "group_increase":
                                LOGGER.info("群里来了新成员")
                                threading.Thread(target=manager.executeEvent,
                                                 args=("on_group_member_add", event)).start()
                            case "group_decrease":
                                LOGGER.info("群里有人走了")
                                threading.Thread(target=manager.executeEvent,
                                                 args=("on_group_member_leave", event)).start()
                    if event["post_type"] == "request":
                        match event["request_type"]:
                            case "group":
                                match event["sub_type"]:
                                    case "add":
                                        LOGGER.info("有人要加群！！！")
                                        threading.Thread(target=manager.executeEvent,
                                                         args=("on_group_add_request", event)).start()
        except websockets.ConnectionClosedError:
            LOGGER.error("连接失败，1秒后重试")
            time.sleep(1)
            continue
        except ConnectionRefusedError:
            LOGGER.error("连接失败，1秒后重试")
            time.sleep(1)
            continue
        except Exception as e:
            LOGGER.critical(e)


def exit1(signum, frame):
    proc.terminate()
    exit()


if __name__ == "__main__":
    threading.Thread(target=initPlugin).start()
    signal.signal(signal.SIGINT, exit1)
    asyncio.run(manage())
