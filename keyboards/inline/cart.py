from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

product_cb = CallbackData('product', 'id', 'action')


def product_markup(idx, count, price):
    global product_cb
    pr = price * count
    markup = InlineKeyboardMarkup()
    if count != 1:
        back_btn = InlineKeyboardButton('➖', callback_data=product_cb.new(id=idx, action='decrease'))
    else:
        back_btn = InlineKeyboardButton('❌', callback_data=product_cb.new(id=idx, action='decrease'))
    count_btn = InlineKeyboardButton(count, callback_data=product_cb.new(id=idx, action='count'))
    next_btn = InlineKeyboardButton('➕', callback_data=product_cb.new(id=idx, action='increase'))
    markup.add(InlineKeyboardButton(f'Narx: {pr}', callback_data="dd"))
    markup.add(back_btn, count_btn, next_btn)

    return markup


def total_cost(total):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(f'Umumiy narxi: {total}', callback_data=""))
    return markup
