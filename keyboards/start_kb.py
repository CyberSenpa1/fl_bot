from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_choose() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Фрилансер")
    kb.button(text="Заказчик")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


