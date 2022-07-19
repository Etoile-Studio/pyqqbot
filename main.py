import asyncio
import json
import os
import signal
import subprocess
import time
import websockets
from settings import PATH, WEBSOCKET_HOST, WEBSOCKET_PORT, QQ_ID, GROUP_ID, LOGGER

proc = subprocess.Popen(args="go-cqhttp.exe -faststart", shell=True, cwd=os.path.join(PATH, "bot"),
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# 从服务器接收数据
async def manage():
    while 1:
        try:
            # websocket 连接
            async with websockets.connect(f'ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}') as websocket:
                LOGGER.info("连接成功")
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
                        continueProcess = True
                        # 生成log
                        log = "收到一条消息:\n"
                        log += "来源:"
                        match event["sub_type"]:
                            case "friend":
                                log += "朋友(当群临时会话处理)\n"
                            case "group":
                                log += "群临时会话\n"
                            case "normal":
                                log += "群消息\n"
                            case "anonymous":
                                log += "匿名消息（这是不允许的）\n"
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
                            match event["message_type"]:
                                # 来自群的消息
                                case "group":
                                    if event["group_id"] in GROUP_ID:
                                        if event["raw_message"].find(f"[CQ:at,qq={QQ_ID}]") == 0:
                                            continue
                                        ...
                                # 来自私聊或群临时会话，此处命令无需@
                                case "private":
                                    ...
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
    signal.signal(signal.SIGINT, exit1)
    asyncio.run(manage())
