import logging
import os

# Time range for message
MIN_TIME = 1#2
MAX_TIME = 2#24


# TOKEN = os.getenv('TOKEN')
# ADMIN_ID = os.getenv('ADMIN_ID')
# DB_HOST = os.getenv('DB_HOST')
# DB_PORT = os.getenv('DB_PORT')
# DB_NAME = os.getenv('DB_NAME')
# DB_USER = os.getenv('DB_USER')
# DB_PASS = os.getenv('DB_PASS')

TOKEN="5413670593:AAG4Upm1B6HJyuRM_1TjoSMLIOcZa-_Q3IM"
ADMIN_CHAT="-1001943705246"
ADMIN_ID="746885613"
DB_HOST="production-db.chllvs6uk5zy.ap-southeast-2.rds.amazonaws.com"
DB_PORT="5432"
DB_NAME="skeduler_master"
DB_USER="skeduler"
DB_PASS="igetyourdbpass228andpnwdyou1312"



# Path
# path_dict = {
#     "LOG_PATH": "/app/log",
#     "BIO_PATH": "/app/content/pic/bio",
#     "PIC_PATH": "/app/content/pic",
#     "VIDEO_PATH": "/app/content/video"
# }

path_dict = {
     "LOG_PATH": "/home/sasha/Code/my-projects/aki-bot/log",
     "PIC_PATH": "/home/sasha/Pictures/akibot/pic",
     "VIDEO_PATH": "/home/sasha/Pictures/akibot/video"
 }



# log
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(
    format=log_format,
    level=logging.DEBUG,
    filename="/home/sasha/Code/my-projects/aki-bot/log/main.log")
    #filename="/app/log/main.log")
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
