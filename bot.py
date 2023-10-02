import os
import db
import random
import config
import asyncio
import logging
from aiogram.utils import executor
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode

API_TOKEN = config.TOKEN

# Init bot
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(level=logging.INFO)

# /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    if not await db.user_exists(user_id):
        # Create functions for add and check if exists user id in db
        await db.add_user(user_id)
        logging.info(f"Added new user with user_id {user_id} and username {message.from_user.username}")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton("🐕 Pet Me")
    keyboard.add(button)
    # Check MD output in message 
    await message.answer(config.WELCOME_MESSAGE, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

# TO DO
# Delay Pet me - add timeout for user, if requests > 2 times in 10 sec - slow mode
# Counter for users who request pet me - why not? 
# bulk message sent 
# random content get send 
# help handler
# stop for unsubcribe
# local build - use env file

