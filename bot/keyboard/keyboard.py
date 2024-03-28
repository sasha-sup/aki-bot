from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def main_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🐕 Pet Me")],
            [KeyboardButton(text="🪪 Bio")],
            [KeyboardButton(text="🍜 Feed Me")],
            [KeyboardButton(text="🦊 Aki sticker pack")],
            [KeyboardButton(text="🆘 Help")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Select action: ",
    )
    return kb
