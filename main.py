import asyncio
import os
import random

from aiogram import Dispatcher, executor

import config
import db
from bot import dp, send_messages
from config import logger


# Create required directories
async def create_content_dirs():
    try:
        for dir_path in [config.PIC_PATH, config.VIDEO_PATH, config.LOG_PATH]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                logger.info(f"Created directory: {dir_path}")
            else:
                logger.info(f"Directory already exists: {dir_path}")
    except Exception as e:
        logger.error(f"Error creating directories: {e}")
        raise e

async def main():
    await create_content_dirs()
    await db.create_tables_if_exists()
#    await send_messages()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    executor.start_polling(dp, skip_updates=True)
