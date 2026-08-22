from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мужчина"), KeyboardButton(text="Женщина")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_inline():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="НОВАЯ ИСТОРИЯ", callback_data="new_history")],
            [InlineKeyboardButton(text="ОТПРАВИТЬ ИСТОРИЮ✅", callback_data="cmd_otpravit")],
        ]
    )

    return keyboard

def get_new_inline():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="НОВАЯ ИСТОРИЯ", callback_data="new_history")],
        ]
    )

    return keyboard