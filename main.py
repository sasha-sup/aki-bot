import os
import db
import random
import config
import asyncio
import logging
from bot import dp
from aiogram import executor

# Logger
log_dir = os.path.join(os.path.dirname(__file__), 'log')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO,
    filename = os.path.join(config.BASE_DIR, "log", "main.log"))
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# LoggingMiddleware
logging_middleware = LoggingMiddleware(
    logger_name='aiogram',
    log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    log_level=logging.INFO)

# Create required directories
async def create_content_dirs():
    try:
        for dir_path in [config.PIC_PATH, config.VIDEO_PATH]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                logging.info(f"Created directory: {dir_path}")
            else:
                logging.info(f"Directory already exists: {dir_path}")
    except Exception as e:
        logging.error(f"Error creating directories: {e}")
        raise e

async def main():
    await create_content_dirs()
    await db.create_tables_if_exists()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
