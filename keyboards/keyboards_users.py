from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

def index_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Принять правила", callback_data="accept_rules")]
    ]
    inline_kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_kb