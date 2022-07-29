import logging
import os

# path
PATH = os.path.abspath(os.path.dirname(__file__))
PLUGIN_PATH = os.path.join(PATH, "plugins")
BOT_PATH = os.path.join(PATH, "bot")
PLUGIN_PACKAGE = "plugins"
PATH_BLACKLIST = ["__init__.py", "__pycache__"]

# qq config
QQ_ID = 1726237584
GROUP_ID = [678414652]

# api location
WEBSOCKET_HOST = HTTP_HOST = "localhost"
WEBSOCKET_PORT = 6700
HTTP_PORT = 5700

# log config
LOG_LEVEL = logging.DEBUG
logging.basicConfig(format="[%(asctime)s](%(levelname)s): %(message)s", level=LOG_LEVEL)
LOGGER = logging.getLogger()

# 此处不要改！！！Do not modify!!!
PLUGIN_LIST = {
    "on_group_message": [],
    "on_command": [],
    "on_group_file": [],
    "on_group_member_add": [],
    "on_group_add_request": [],
    "on_group_member_leave": [],
    "on_group_anonymous_message": []
}
