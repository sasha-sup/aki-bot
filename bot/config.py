import logging
import os

# Time range for message
MIN_TIME = 1#2
MAX_TIME = 2#24


TOKEN = os.getenv('TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')


Path
path_dict = {
    "LOG_PATH": "/app/log",
    "PIC_PATH": "/app/content/pic",
    "VIDEO_PATH": "/app/content/video"
}

# log
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(
    format=log_format,
    level=logging.DEBUG,
    filename="/app/log/main.log")
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
