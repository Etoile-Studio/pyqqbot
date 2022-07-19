import logging
import os

# path
PATH = os.path.abspath(os.path.dirname(__file__))
PLUGIN_PATH = os.path.join(PATH, "plugins")
PATH_WHITELIST = ["__init__.py", ""]

# qq config
QQ_ID = 1726237584
GROUP_ID = [678414652]
ALLOW_PRIVATE_MSG = True

# api location
WEBSOCKET_HOST = HTTP_HOST = "localhost"
WEBSOCKET_PORT = 6700
HTTP_PORT = 5700

# log config
LOG_LEVEL = logging.INFO
logging.basicConfig(format="[%(asctime)s](%(levelname)s): %(message)s", level=LOG_LEVEL)
LOGGER = logging.getLogger()
