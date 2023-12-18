from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_kb():
    kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🐕 Pet Me")
        ],
        [
            KeyboardButton(text="🪪 Bio")
        ],
        [
            KeyboardButton(text="🍜 Feed Me")
        ],
        [
            KeyboardButton(text="🆘 Help")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Select action: "
    )
    return kb