import os

# Time range for message
MIN_TIME = 1 #2
MAX_TIME = 2 #24

# Welcome message
WELCOME_MESSAGE = """
🦊*Smotri Kakaja Lisi4ka*🦊

_Commands_\:
\/start _Enable the bot_
\/help _Get this message_
\/stop _Disable notifications_

You can also find us on\:
🌟 [TikTok](https\:\/\/tiktok\.com\/\@sashasup1312) 🌟
🌟 [Reddit](https\:\/\/www\.reddit\.com\/user\/sasha\_sup1312) 🌟

For any issues or feedback\, reach out\:
📬 [sasha\-sup](https\:\/\/sasha\-sup\.github\.io/)
"""

HELP_MESSAGE = """
_Commands_\:
\/start _Enable the bot_
\/help _Get this message_
\/stop _Disable notifications_
\/notifyon _Enable notifications_
"""


TOKEN = os.getenv('TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

# Path
BASE_DIR = os.path.dirname(__file__)
PIC_PATH = os.path.join(BASE_DIR, 'content', 'pic')
VIDEO_PATH = os.path.join(BASE_DIR, 'content', 'video')
