import asyncio
from datetime import datetime, timedelta

import config
import db
import message_templates.message as msg
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message, ReplyKeyboardRemove
from config import path_dict
from keyboard.keyboard import main_kb
from logger import logger

from bot import get_random_file

router = Router()


# /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    try:
        user_id = message.from_user.id
        username = message.from_user.username
        await db.ensure_user_exists(user_id, username)
        path = await get_random_file()
        message_text = msg.WELCOME_MESSAGE
        if "video" in path:
            video = FSInputFile(path)
            await message.answer_video(
                video=video,
                caption=message_text,
                parse_mode="MarkdownV2",
                disable_web_page_preview=True,
                reply_markup=main_kb(),
            )
            await message.delete()
        elif "pic" in path:
            pic = FSInputFile(path)
            await message.answer_photo(
                photo=pic,
                caption=message_text,
                parse_mode="MarkdownV2",
                disable_web_page_preview=True,
                reply_markup=main_kb(),
            )
            await message.delete()
        logger.info(
            f"User {username} started the bot.",
            extra={"tags": {"Aki-Bot-Core": "Core"}},
        )
    except Exception as e:
        await message.answer("⚠️ Something went wrong. Try again or contact admin.")
        await message.delete()
        logger.error(
            f"Error start: {e}",
            extra={"tags": {"Aki-Bot-Core": "Core"}},
        )


# /help
@router.message(Command("help"))
async def cmd_help(message: Message):
    try:
        await message.answer(
            msg.HELP_MESSAGE, parse_mode="MarkdownV2", reply_markup=main_kb()
        )
        await message.delete()
    except Exception as e:
        await message.answer("⚠️ Something went wrong. Try again or contact admin.")
        await message.delete()
        logger.error(
            f"Error help: {e}",
            extra={"tags": {"Aki-Bot-Core": "Core"}},
        )


# /stop
@router.message(Command("stop"))
async def cmd_stop(message: Message):
    try:
        user_id = message.from_user.id
        await db.update_notification_settings(user_id, send_notifications=False)
        logger.info(
            f"User {message.from_user.username} has opted out of automatic notifications.",
            extra={"tags": {"Aki-Bot-Core": "Core"}},
        )
        await message.answer(
            "You have cancelled notifications.\n Use /notifyon command to restart notifications."
        )
        await message.delete()
    except Exception as e:
        await message.answer("⚠️ Something went wrong. Try again or contact admin.")
        await message.delete()
        logger.error(
            f"Error stop: {e}",
            extra={"tags": {"Aki-Bot-Core": "Core"}},
        )


# /notifyon
@router.message(Command("notifyon"))
async def cmd_restart(message: Message):
    try:
        user_id = message.from_user.id
        await db.update_notification_settings(user_id, send_notifications=True)
        logger.info(
            f"User {message.from_user.username} has opted in for automatic notifications.",
            extra={"tags": {"Aki-Bot-Core": "Core"}},
        )
        await message.answer("You have opted in for automatic notifications.")
    except Exception as e:
        await message.answer("⚠️ Something went wrong. Try again or contact admin.")
        await message.delete()
        logger.error(
            f"Error notifyon: {e}",
            extra={"tags": {"Aki-Bot-Core": "Core"}},
        )


# 🐕 Pet Me
@router.message(F.text.endswith("Pet Me"))
async def pet_me(message: Message):
    try:
        user_id = message.from_user.id
        user = await db.get_user(user_id)
        if user:
            current_time = datetime.now()
            last_request_time = user.get("last_pet_time")
            if (
                last_request_time is None
                or current_time - last_request_time >= timedelta(seconds=69)
            ):
                await db.set_last_pet_time(user_id, current_time)
                await db.increment_click_count(user_id)
                logger.info(
                    f"User {message.from_user.username} requested content.",
                    extra={"tags": {"Aki-Bot-Core": "Core"}},
                )
                path = await get_random_file()
                try:
                    if "video" in path:
                        video = FSInputFile(path)
                        await message.answer_video(video=video)
                        await message.delete()
                    elif "pic" in path:
                        pic = FSInputFile(path)
                        await message.answer_photo(photo=pic)
                        await message.delete()
                except Exception as e:
                    await message.answer(
                        "⚠️ Something went wrong. Try again or contact admin."
                    )
                    await message.delete()
                    logger.error(
                        f"Error in send rendom file: {e}",
                        extra={"tags": {"Aki-Bot-Core": "Core"}},
                    )
            else:
                await message.answer("Please wait before requesting more content.")
                await message.delete()
        else:
            await message.answer("You are not registered. Use /start to begin.")
            await message.delete()
    except Exception as e:
        logger.error(
            f"Error petme button: {e}",
            extra={"tags": {"Aki-Bot-Core": "Core"}},
        )


# 🍜 Feed me
@router.message(F.text.endswith("Feed Me"))
async def pet_me(message: Message):
    try:
        user_id = message.from_user.id
        user = await db.get_user(user_id)
        if user:
            current_time = datetime.now()
            last_request_time = user.get("last_pet_time")
            logger.info(
                f"{last_request_time}",
                extra={"tags": {"Aki-Bot-Core": "Core"}},
            )
            if (
                last_request_time is None
                or current_time - last_request_time >= timedelta(seconds=69)
            ):
                logger.info(
                    f"User {message.from_user.username} requested donate.",
                    extra={"tags": {"Aki-Bot-Core": "Core"}},
                )
                await message.answer(
                    msg.DONAT, parse_mode="MarkdownV2", reply_markup=main_kb()
                )
                await message.delete()
                await asyncio.sleep(10)  # delay in seconds
            else:
                await message.answer("Please wait before requesting more content.")
                await message.delete()
        else:
            await message.answer("You are not registered. Use /start to begin.")
            await message.delete()
    except Exception as e:
        await message.answer("⚠️ Something went wrong. Try again or contact admin.")
        await message.delete()
        logger.error(
            f"Error petme button: {e}",
            extra={"tags": {"Aki-Bot-Core": "Core"}},
        )


# 🪪 Bio
@router.message(F.text.endswith("Bio"))
async def bio(message: Message):
    try:
        user_id = message.from_user.id
        user = await db.get_user(user_id)
        if user:
            current_time = datetime.now()
            last_request_time = user.get("last_pet_time")
            if (
                last_request_time is None
                or current_time - last_request_time >= timedelta(seconds=69)
            ):
                await db.set_last_pet_time(user_id, current_time)
                await db.increment_click_count1(user_id)
                logger.info(
                    f"User {message.from_user.username} requested bio.",
                    extra={"tags": {"Aki-Bot-Core": "Core"}},
                )
                await asyncio.sleep(5)
                file_path = "/app/content/bio/aki-bio.png"
                photo = FSInputFile(file_path)
                message_text = msg.BIO_MESSAGE
                await message.answer_photo(
                    photo=photo, caption=message_text, parse_mode="MarkdownV2"
                )
                await message.delete()
            else:
                await message.answer("Please wait before requesting more content.")
                await message.delete()
        else:
            await message.answer("You are not registered. Use /start to begin.")
            await message.delete()
    except Exception as e:
        await message.answer("⚠️ Something went wrong. Try again or contact admin.")
        await message.delete()
        logger.error(
            f"Error bio button: {e}",
            extra={"tags": {"Aki-Bot-Core": "Core"}},
        )


# 🆘 Help
@router.message(F.text.endswith("Help"))
async def help(message: Message):
    try:
        user_id = message.from_user.id
        user = await db.get_user(user_id)
        if not user:
            logger.info(
                f"User {message.from_user.username} not registered. ",
                extra={"tags": {"Aki-Bot-Core": "Core"}},
            )
            await message.answer("You are not registered. Use /start to begin.")
            await message.delete()
            return
        await cmd_help(message)
    except Exception as e:
        await message.answer("⚠️ Something went wrong. Try again or contact admin.")
        await message.delete()
        logger.error(
            f"Error help message button: {e}",
            extra={"tags": {"Aki-Bot-Core": "Core"}},
        )


# 🦊 My sticker pack
@router.message(F.text.endswith("Aki sticker pack"))
async def bio(message: Message):
    try:
        user_id = message.from_user.id
        user = await db.get_user(user_id)
        if user:
            current_time = datetime.now()
            last_request_time = user.get("last_pet_time")
            if (
                last_request_time is None
                or current_time - last_request_time >= timedelta(seconds=69)
            ):
                await db.set_last_pet_time(user_id, current_time)
                await db.increment_click_count1(user_id)
                logger.info(
                    f"User {message.from_user.username} requested stickers.",
                    extra={"tags": {"Aki-Bot-Core": "Core"}},
                )
                await asyncio.sleep(5)
                file_path = "/app/content/pic/w-logo_226.jpg"
                photo = FSInputFile(file_path)
                message_text = msg.STICKER_MESSAGE
                await message.answer_photo(
                    photo=photo, caption=message_text, parse_mode="MarkdownV2"
                )
                await message.delete()
            else:
                await message.answer("Please wait before requesting more content.")
                await message.delete()
        else:
            await message.answer("You are not registered. Use /start to begin.")
            await message.delete()
    except Exception as e:
        await message.answer("⚠️ Something went wrong. Try again or contact admin.")
        await message.delete()
        logger.error(
            f"Error bio button: {e}",
            extra={"tags": {"Aki-Bot-Core": "Core"}},
        )
