import asyncio
import os
import random
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types
from aiogram.types import (KeyboardButton, Message, ParseMode,
                           ReplyKeyboardMarkup)
from aiogram.types.message import ContentType
from aiogram.utils.markdown import hbold

import config
import db
from config import logger

API_TOKEN = config.TOKEN

# Init bot
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# button
button = KeyboardButton("🐕 Pet Me")
keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button)

# Get content
async def send_random_file(user_id):
    try:
        picture_files = [os.path.join(config.PIC_PATH, filename) for filename in os.listdir(config.PIC_PATH)]
        video_files = [os.path.join(config.VIDEO_PATH, filename) for filename in os.listdir(config.VIDEO_PATH)]
        chosen_dir = random.choice([config.PIC_PATH, config.VIDEO_PATH])
        chosen_file = random.choice(os.listdir(chosen_dir))
        file_path = os.path.join(chosen_dir, chosen_file)

        if file_path in picture_files:
            await bot.send_photo(user_id, types.InputFile(file_path))
        elif file_path in video_files:
            await bot.send_video(user_id, types.InputFile(file_path))
    except Exception as e:
        logger.error(f"Error send_random_file: {e}")

# /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    try:
        user_id = message.from_user.id
        await db.ensure_user_exists(user_id)
        await message.answer(config.WELCOME_MESSAGE, parse_mode="MarkdownV2", disable_web_page_preview=True, reply_markup=keyboard)
        logger.info(f"User {message.from_user.username} started the bot.")
        await send_random_file(user_id)
    except Exception as e:
        logger.error(f"Error start: {e}")

# /help
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    try:
        await message.reply(config.HELP_MESSAGE, parse_mode="MarkdownV2", reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Error help: {e}")

# /stop
@dp.message_handler(commands=['stop'])
async def stop_command(message: types.Message):
    try:
        user_id = message.from_user.id
        await db.update_notification_settings(user_id, send_notifications=False)
        logger.info(f"User {user_id} has opted out of automatic notifications.")
        await message.reply("You have cancelled notifications.\n Use the /notifyon command to restart notifications.")
    except Exception as e:
        logger.error(f"Error stop: {e}")

# /notifyon
@dp.message_handler(commands=['notifyon'])
async def notify_on_command(message: types.Message):
    try:
        user_id = message.from_user.id
        await db.update_notification_settings(user_id, send_notifications=True)
        logger.info(f"User {user_id} has opted in for automatic notifications.")
        await message.reply("You have opted in for automatic notifications.")
    except Exception as e:
        logger.error(f"Error notifyon: {e}")

# notifier
async def send_messages():
    try:
        while True:
            users = await db.get_all_user_ids()
            interval = timedelta(hours=(random.randint(config.MIN_TIME, config.MAX_TIME)))
            for user_id in users:
                await send_random_file(user_id)
                logger.info(f"Sent a message to user {user_id}")
                await asyncio.sleep(10) # delay in seconds
            await asyncio.sleep(interval.total_seconds())
    except Exception as e:
        logger.error(f"Error send_messages: {e}")

# 🐕 Pet Me
@dp.message_handler(lambda message: message.text == "🐕 Pet Me")
async def handle_pet_me(message: types.Message):
    try:
        user_id = message.from_user.id
        user = await db.get_user(user_id)
        if user:
            current_time = datetime.now()
            last_request_time = user.get('last_pet_time')
            if last_request_time is None or current_time - last_request_time >= timedelta(seconds=60):
                await db.set_last_pet_time(user_id, current_time)
                await db.increment_click_count(user_id)
                logger.info(f"User {user_id} requested content.")
                await send_random_file(user_id)
            else:
                await message.answer("Please wait before requesting more content.")
        else:
            await message.answer("You are not registered. Use /start to begin.")
    except Exception as e:
        logger.error(f"Error petme: {e}")

async def start_bot():
    await asyncio.gather(
        dp.start_polling(skip_updates=True),
        send_messages())

if __name__ == '__main__':
    asyncio.run(start_bot())
    from aiogram import executor
