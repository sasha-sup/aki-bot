import logging
import os

# Time range for message
MIN_TIME = 2
MAX_TIME = 24

BIO_MESSAGE = """

\#\# Basic Information
\- *Name\:* Akihiro
\- *Breed\:* Shiba
\- *Gender\:* Female
\- *Date of Birth\:* 29\.08\.2021

\#\# Physical Characteristics
\- *Color\:* Red
\- *Size\:* Small
\- *Weight\:*  7 kg

\#\# Health
\- *Vaccination\:* Yes
\- *Microchipping\:* Yes

\#\# Owner
 📬 [sasha\-sup](https\:\/\/sasha\-sup\.github\.io/)
"""

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
LOG_PATH = "/app/log"
BIO_PATH = "/app/content/pic/bio."
PIC_PATH = "/app/content/pic"
VIDEO_PATH = "/app/content/video"

# log
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(
    format=log_format,
    level=logging.INFO,
    filename="/app/log/main.log")
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
