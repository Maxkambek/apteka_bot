import re
import requests
from aiogram import types
from aiogram.bot import bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.dispatcher.filters import Command
from keyboards.default.menu_default import menu, type_keyboard, hospital_keyboard, back, for_order
from keyboards.inline.cart import product_markup, product_cb, total_cost
from loader import dp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.chat import ChatActions
from .my_tools import ShoppingCart
from .start import bot_start, type_user
from .text import bot_text, drug_msg
from geopy.geocoders import Nominatim

storage = MemoryStorage()

cart = ShoppingCart()


class MyStates(StatesGroup):
    state1 = State()
    state2 = State()


@dp.message_handler(text="Shifoxonalar")
async def user_1(message: types.Message):
    await message.answer(bot_text['text_3'], reply_markup=hospital_keyboard)


@dp.message_handler(lambda message: 'tumani' in message.text)
async def user_2(message: types.Message):
    button = message.text.split(' ')[0]
    rp = requests.get(url=f'http://185.196.213.44/main/clinic?name={button}')
    print(button)
    res = rp.json()
    print(res)
    keyboard = InlineKeyboardMarkup(row_width=1)
    for i in res:
        index = i['id']
        keyboard.add(InlineKeyboardButton(text=i['name'], callback_data=f'clinic {index}'))
    keyboard.add(InlineKeyboardButton("Orqaga qaytish", callback_data="orqaga qaytish"))
    await message.answer("Iltimos Shifoxonalar ro'yhatidan tanlang!", reply_markup=keyboard)
    await message.answer(
        "Agar shifoxonangizni topa olmasangiz bosh menu dagi aloqa raqamlari orqali bizga murojaat qilishingizni so'raymiz",
        reply_markup=back)


@dp.callback_query_handler(lambda c: c.data.startswith('clinic'))
async def for_drug_search(c: types.CallbackQuery):
    await MyStates.state1.set()
    await dp.bot.send_message(chat_id=c.message.chat.id, text=bot_text['text_4'], reply_markup=back)


@dp.message_handler(state=MyStates.state1)
async def process_input_handler(message: types.Message, state: FSMContext):
    user_text = message.text
    if user_text == "⬅Orqaga":
        await state.finish()
        return await type_user(message)
    if user_text == "⬆Bosh Menyu":
        await state.finish()
        return await bot_start(message)
    rp = requests.get(url=f'http://185.196.213.44/main/list?text={user_text}')
    res = rp.json()
    print(len(res))
    if len(res) == 0:
        await MyStates.state1.set()
        await recursive_function(message)
    if len(res) > 0:
        if len(res) > 20:
            res = res[:20]
        markup = ReplyKeyboardMarkup()
        for i in res:
            text = str(i['id']) + ". " + i['name']
            markup.add(KeyboardButton(text))
        markup.add(KeyboardButton("⬅Orqaga"))
        markup.add(KeyboardButton("⬆Bosh Menyu"))
        await state.finish()
        await message.answer(bot_text['text_5'], reply_markup=markup)


async def recursive_function(message: types.Message):
    await message.answer(bot_text['text_6'], reply_markup=back)


@dp.message_handler(regexp=r'^(\d+)\.')
async def button_handler(message: types.Message):
    button_index = int(re.match(r'^(\d+)\.', message.text).group(1))
    rp = requests.get(url=f'http://185.196.213.44/main/drug/{button_index}/')
    res = rp.json()
    msg = drug_msg(res['name'], res['owner'], res['price'], res['expire'])
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("➕ Savatchaga qo'shish", callback_data=f'add_product {button_index}'),
    )
    await dp.bot.send_message(message.chat.id, msg, reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data.startswith('add_product'))
async def add_product_callback(callback_query: types.CallbackQuery):
    product_id = callback_query.data.split(' ')[1]
    keyboard = InlineKeyboardMarkup(row_width=1)
    rp = requests.get(url=f'http://185.196.213.44/main/drug/{product_id}/')
    res = rp.json()

    cart.add_product(res['id'], res['name'], res['price'])
    keyboard.add(
        InlineKeyboardButton("➕ Xaridni davom ettirish", callback_data="continue"),
    )
    keyboard.add(
        InlineKeyboardButton("⬆ Savatchaga o'tish", callback_data="cart_list")
    )
    await dp.bot.send_message(callback_query.from_user.id, bot_text['text_7'],
                              reply_markup=keyboard)


total_for = None


@dp.callback_query_handler(lambda c: c.data == "cart_list")
async def cart_list_callback(callback_query: types.CallbackQuery, state: FSMContext):
    global total_for
    if len(cart.products) == 0:
        await dp.bot.send_message(callback_query.from_user.id, bot_text['text_8'])
    else:
        await dp.bot.send_chat_action(callback_query.from_user.id, ChatActions.TYPING)
        async with state.proxy() as data:
            data['products'] = {}
        order_cost = 0
        for i in cart.products:
            async with state.proxy() as data:
                data['products'][i['id']] = [i['name'], i['price'], i['quantity']]
            markup = product_markup(i['id'], i['quantity'], i['price'])
            name = i['name']
            total = i['price'] * i['quantity']
            order_cost += total
            text = f'<b>{name}</b>\n\n\nЦена: {total} sum.'
            await dp.bot.send_message(callback_query.from_user.id, text, reply_markup=markup)
        message_id = await dp.bot.send_message(callback_query.from_user.id, f'Umumiy narxi: {cart.get_total_price()}')
        total_for = message_id.message_id
        if order_cost != 0:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('📦 Buyurtma berish')
            await dp.bot.send_message(callback_query.from_user.id, bot_text['text_9'],
                                      reply_markup=markup)


@dp.message_handler(text="📦 Buyurtma berish")
async def button_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        level = 1
        text = ''
        total_cart = 0
        for key, value in data['products'].items():
            total_cart += value[1] * value[2]
            text += str(level) + '.' + value[0] + "\n<b>Soni:</b> " + str(value[2]) + '\n'
        text += f'\n\n<b>Umumiy narxi:</b> {total_cart} sum'
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            InlineKeyboardButton('Davom etish', callback_data=f'toPayment')
        )
        await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(lambda query: query.data == 'toOrder')
async def callback_handler(call_back: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Joylashuvni yuborish", request_location=True))

    await dp.bot.send_message(call_back.message.chat.id, bot_text['text_10'],
                              reply_markup=keyboard)


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def handle_location(message: types.Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    geolocator = Nominatim(user_agent="myMahkamApp")
    location = geolocator.reverse(f"{latitude}, {longitude}")
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        KeyboardButton(text="❌ Yo'q", callback_data=f"qayta lokatsiya"),
        KeyboardButton(text="✅ Ha", callback_data=f"toPayment"),
    )
    await message.answer(f"Shu manzilni  tasdiqlaysizmi?\n{location.address}", reply_markup=keyboard)


@dp.callback_query_handler(lambda query: query.data == 'qayta lokatsiya')
async def callback_handler(call_back: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Joylashuvni yuborish", request_location=True))

    await dp.bot.send_message(call_back.message.chat.id, bot_text['text_10'],
                              reply_markup=keyboard)


@dp.callback_query_handler(lambda call_back: call_back.data == "toPayment")
async def get_phone_number(call_back: CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Telefon raqam ulashish", request_contact=True))

    await dp.bot.send_message(call_back.message.chat.id, "Iltimos telefon raqamingizni jo'nating",
                              reply_markup=keyboard)


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def handle_contact(message: types.Message):
    phone_number = message.contact.phone_number
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(KeyboardButton('Payme'))
    markup.add(KeyboardButton('Click'))
    await message.answer(f"Iltimos to'lov turini tanlang! ", reply_markup=markup)


@dp.callback_query_handler(product_cb.filter(action='count'))
@dp.callback_query_handler(product_cb.filter(action='increase'))
@dp.callback_query_handler(product_cb.filter(action='decrease'))
async def product_callback_handler(query: CallbackQuery, callback_data: dict, state: FSMContext):
    idx = int(callback_data['id'])
    action = callback_data['action']
    if 'count' == action:
        async with state.proxy() as data:

            if 'products' not in data.keys():

                await cart_list_callback(query, state)

            else:

                await query.answer('Количество - ' + str(data['products'][idx][2]))

    else:

        async with state.proxy() as data:
            if 'products' not in data.keys():
                await cart_list_callback(query, state)
            else:
                print(data['products'])
                data['products'][idx][2] += 1 if 'increase' == action else -1
                count_in_cart = data['products'][idx][2]
                price = data['products'][idx][1]
                await query.message.edit_reply_markup(product_markup(idx, count_in_cart, price))
                total = 0
                for key, value in data['products'].items():
                    total += value[1] * value[2]
                print(total)
                await dp.bot.edit_message_text(chat_id=query.message.chat.id, message_id=total_for,
                                               text=f'Umumiy narxi: {total}')


@dp.callback_query_handler(lambda c: c.data == 'continue')
async def continue_callback(callback_query: types.CallbackQuery):
    await MyStates.state1.set()
    await dp.bot.send_message(callback_query.from_user.id, bot_text['text_4'],
                              reply_markup=back)
