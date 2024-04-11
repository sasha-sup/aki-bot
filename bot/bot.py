import asyncio
import os
import random
from datetime import datetime, timedelta

import config
import db
import message_templates.message as msg
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import FSInputFile, KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.types.message import ContentType
from aiogram.utils.markdown import hbold
from config import MAX_TIME, MIN_TIME, path_dict
from handlers import handlers
from logger import logger

bot = Bot(token=config.TOKEN)
dp = Dispatcher()


# Create required directories
def create_content_dirs(path_dict):
    try:
        for dir_path in [
            path_dict["PIC_PATH"],
            path_dict["VIDEO_PATH"]
        ]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                logger.info(
                    f"Created directory: {dir_path}",
                    extra={"tags": {"Aki-Bot-Core": "Content-Dirs"}},
                )
            else:
                logger.info(
                    f"Directory already exists: {dir_path}",
                    extra={"tags": {"Aki-Bot-Core": "Content-Dirs"}},
                )
    except Exception as e:
        logger.error(
            f"Error creating directories: {e}",
            extra={"tags": {"Aki-Bot-Core": "Content-Dirs"}},
        )
        raise e


# Get rendom file
async def get_random_file():
    try:
        picture_files = [
            os.path.join(path_dict["PIC_PATH"], filename)
            for filename in os.listdir(path_dict["PIC_PATH"])
        ]
        video_files = [
            os.path.join(path_dict["VIDEO_PATH"], filename)
            for filename in os.listdir(path_dict["VIDEO_PATH"])
        ]
        ruletka = random.randint(1, 3)
        if ruletka == 1:
            chosen_dir = path_dict["VIDEO_PATH"]
        else:
            chosen_dir = path_dict["PIC_PATH"]
        chosen_file = random.choice(os.listdir(chosen_dir))
        file_path = os.path.join(chosen_dir, chosen_file)
        return file_path
    except Exception as e:
        logger.error(
            f"Error get random file: {e}",
            extra={"tags": {"Aki-Bot-Core": "Get-Random-File"}},
        )


# notifier
async def send_messages(bot):
    try:
        while True:
            users = await db.get_all_user_ids()
            interval = timedelta(hours=(random.randint(MIN_TIME, MAX_TIME)))
            logger.info(
                f"Next iteration in: {interval} hours",
                extra={"tags": {"Aki-Bot-Core": "Notifier"}},
            )
            await asyncio.sleep(interval.total_seconds())
            for user_id in users:
                try:
                    path = await get_random_file()
                    if "video" in path:
                        video = FSInputFile(path)
                        await bot.send_video(user_id, video=video)
                    elif "pic" in path:
                        pic = FSInputFile(path)
                        await bot.send_photo(user_id, photo=pic)
                    logger.info(
                        f"Sent file {path} to {user_id}",
                        extra={"tags": {"Aki-Bot-Core": "Notifier"}},
                    )
                except Exception as e:
                    logger.error(
                        f"Error with {path}: {e}",
                        extra={"tags": {"Aki-Bot-Core": "Notifier"}},
                    )
                    logger.warning(
                        f"User {user_id} blocked the bot? Skipping.",
                        extra={"tags": {"Aki-Bot-Core": "Notifier"}},
                    )
                await asyncio.sleep(10)  # delay in seconds
    except Exception as e:
        await bot.reply("⚠️ Something went wrong. Try again or contact admin.")
        logger.error(
            f"Error send_messages: {e}",
            extra={"tags": {"Aki-Bot-Core": "Notifier"}},
        )


async def send_donat(bot):
    try:
        while True:
            users = await db.get_all_user_ids()
            interval = timedelta(days=(random.randint(MIN_TIME, MAX_TIME)))
            logger.info(
                f"Next donat notify in: {interval}",
                extra={"tags": {"Aki-Bot-Core": "Donat-Notifier"}},
            )
            await asyncio.sleep(interval.total_seconds())
            for user_id in users:
                try:
                    logger.info(
                        f"Sent a donat to user_id {user_id}",
                        extra={"tags": {"Aki-Bot-Core": "Donat-Notifier"}},
                    )
                    path = "/app/content/pic/w-logo_546.jpg"
                    pic = FSInputFile(path)
                    await bot.send_photo(
                        user_id, photo=pic, caption=msg.DONAT, parse_mode="MarkdownV2"
                    )
                    logger.info(
                        f"Sent donat msg to {user_id}",
                        extra={"tags": {"Aki-Bot-Core": "Donat-Notifier"}},
                    )
                    await asyncio.sleep(10)  # Delay in second
                except Exception as e:
                    logger.error(
                        f"Error send_donat: {e}",
                        extra={"tags": {"Aki-Bot-Core": "Donat-Notifier"}},
                    )
                    logger.warning(
                        f"User {user_id} blocked the bot? Skipping.",
                        extra={"tags": {"Aki-Bot-Core": "Donat-Notifier"}},
                    )
    except Exception as e:
        await bot.reply("⚠️ Something went wrong. Try again or contact admin.")
        logger.error(
            f"Error send_donat: {e}",
            extra={"tags": {"Aki-Bot-Core": "Donat-Notifier"}},
        )


# /bulk
@dp.message(Command("bulk"))
async def cmd_bulk(message: Message):
    try:
        user_id = message.from_user.id
        if user_id == int(config.ADMIN_ID):
            users = await db.bulk_user_ids()
            for user_id in users:
                try:
                    path = "/app/content/pic/w-logo_230.jpg"
                    pic = FSInputFile(path)
                    await bot.send_photo(
                        user_id,
                        photo=pic,
                        caption=msg.ADMIN_MESSAGE,
                        parse_mode="MarkdownV2",
                    )
                    logger.info(
                        f"Sent bulk msg to {user_id}",
                        extra={"tags": {"Aki-Bot-Core": "Bulk"}},
                    )
                    await asyncio.sleep(10)  # Delay in seconds
                except Exception as e:
                    logger.error(
                        f"Error bulk msg: {e}",
                        extra={"tags": {"Aki-Bot-Core": "Bulk"}},
                    )
                    logger.warning(
                        f"User {user_id} blocked the bot? Skipping.",
                        extra={"tags": {"Aki-Bot-Core": "Bulk"}},
                    )
                    continue
        else:
            await message.answer("What's wrong with u?")
    except Exception as e:
        logger.error(
            f"Error bulk users: {e}",
            extra={"tags": {"Aki-Bot-Core": "Bulk"}},
        )


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await db.create_tables_if_exists()
    create_content_dirs(path_dict)
    dp.include_routers(handlers.router)
    send_messages_task = asyncio.create_task(send_messages(bot))
    send_donat_task = asyncio.create_task(send_donat(bot))
    await dp.start_polling(bot)
    await asyncio.gather(send_messages_task, send_donat_task)


if __name__ == "__main__":
    asyncio.run(main())
