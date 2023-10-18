from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="🐕 Pet Me")
    kb.button(text="🪪 Bio")
    kb.button(text="🍜 Feed Me")
    kb.button(text="🆘 Help")
    return kb.as_markup(resize_keyboard=True)
