# pyqqbot

python qqbot depends on go-cqhttp



## How to use?

1. clone this repository
2. 参照 requirement.txt 安装依赖
3. 点击[此处](https://github.com/Mrs4s/go-cqhttp/releases/tag/v1.0.0-rc3)下载go-cqhttp

4. 配置go-cqhttp，开启正向http和websocket，将它们的端口记下来，开启群临时会话

5. 进入settings.py，在BOT_PATH填入go-cqhttp的位置，在HTTP_PORT, WEBSOCKET_PORT 分别填入刚刚记下的端口，填写qq_id, 填写你要使用bot的群号，比如 [678414652]，[114514, 1919810]

6. 将你要的插件放入plugins文件夹下

7. win的用户需要改一下main.py中的 “./go-cqhttp”
   ```python
   proc = subprocess.Popen(args="./go-cqhttp -faststart", shell=True, cwd=BOT_PATH, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   ```
8. 运行main.py, then enjoy it

# <font color="red">项目仍在开发中，请等待正式版1.0</font>