from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

y_or_n_kb = InlineKeyboardMarkup().add(InlineKeyboardButton('Так', callback_data='yes')).add(InlineKeyboardButton('Ні', callback_data='no'))