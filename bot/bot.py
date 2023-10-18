import asyncio
import os
import random
from datetime import datetime, timedelta

import config
import db
import message_templates.message as msg
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import (FSInputFile, KeyboardButton, Message,
                           ReplyKeyboardMarkup)
from aiogram.types.message import ContentType
from aiogram.utils.markdown import hbold
from config import MAX_TIME, MIN_TIME, logger, path_dict
from handlers import handlers

bot = Bot(token=config.TOKEN)
dp = Dispatcher()

# Create required directories
def create_content_dirs(path_dict):
    try:
        for dir_path in [path_dict["PIC_PATH"], path_dict["VIDEO_PATH"], path_dict["LOG_PATH"]]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                logger.info(f"Created directory: {dir_path}")
            else:
                logger.info(f"Directory already exists: {dir_path}")
    except Exception as e:
        logger.error(f"Error creating directories: {e}")
        raise e

# Get rendom file
async def get_random_file():
    try:
        picture_files = [os.path.join(path_dict["PIC_PATH"], filename) for filename in os.listdir(path_dict["PIC_PATH"])]
        video_files = [os.path.join(path_dict["VIDEO_PATH"], filename) for filename in os.listdir(path_dict["VIDEO_PATH"])]
        ruletka = random.randint(1, 30)
        if ruletka == 1:
            chosen_dir = path_dict["VIDEO_PATH"]
        else:
            chosen_dir = path_dict["PIC_PATH"]
        chosen_file = random.choice(os.listdir(chosen_dir))
        file_path = os.path.join(chosen_dir, chosen_file)
        return file_path
    except Exception as e:
        logger.error(f"Error get random file: {e}")

# notifier
async def send_messages(bot):
    try:
        while True:
            users = await db.get_all_user_ids()
            interval = timedelta(hours=(random.randint(MIN_TIME, MAX_TIME)))
            for user_id in users:
                try:
                    path = await get_random_file()
                    if "video" in path:
                        video = FSInputFile(path)
                        await bot.send_video(user_id, video=video)
                    elif "pic" in path:
                        pic = FSInputFile(path)
                        await bot.send_photo(user_id, photo=pic)
                except Exception as e:
                    logger.error(f"Error send_random_file: {e}")
                logger.info(f"Sent a message to {user_id}")
                await asyncio.sleep(10) # delay in seconds
            logger.info(f"Next iteration in: {interval} hours")
            await asyncio.sleep(interval.total_seconds())
    except Exception as e:
        await bot.reply("⚠️ Something went wrong. Try again or contact admin.")
        logger.error(f"Error send_messages: {e}")

# /bulk
@dp.message(Command("bulk"))
async def cmd_bulk(message: Message):
    try:
        user_id = message.from_user.id
        if user_id == int(config.ADMIN_ID):
            users = await db.bulk_user_ids()
            for user_id in users:
                logger.info(f"Sent a message to user_id {user_id}")
                await bot.send_message(user_id, msg.ADMIN_MESSAGE, parse_mode="MarkdownV2", reply_markup=main_kb())
                await asyncio.sleep(10)  # Delay in seconds
        else:
            await message.answer("What's wrong with u?")
    except Exception as e:
        logger.error(f"Error bulk users: {e}")

async def main():
    create_content_dirs(path_dict)
    await db.create_tables_if_exists()
    dp.include_routers(handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    send_messages_task = asyncio.create_task(send_messages(bot))
    await dp.start_polling(bot)
    await asyncio.gather(send_messages_task)

if __name__ == "__main__":
    asyncio.run(main())