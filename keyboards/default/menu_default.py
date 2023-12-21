from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔍 Dori Izlash"), ],
        [KeyboardButton(text="Qanday Foydalanaman"), ],
        [
            KeyboardButton(text="Izoh qoldirish"),
            KeyboardButton(text="Aloqa"),
        ],
        [KeyboardButton(text="Biz haqimizda"), ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

type_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Shifoxonalar")],
        [KeyboardButton(text="Uyimga")],
        [KeyboardButton(text="⬆Bosh Menyu")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
back = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⬅Orqaga")],
        [KeyboardButton(text="⬆Bosh Menyu")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

hospital_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Olmazor tumani")],
        [KeyboardButton(text="Yunusobod tumani")],
        [KeyboardButton(text="Chilonzor tumani")],
        [KeyboardButton(text="Shayxontohur tumani")],
        [KeyboardButton(text="Uchtepa tumani")],
        [KeyboardButton(text="Mirzo Ulug'bek tumani")],
        [KeyboardButton(text="Yashnobod tumani")],
        [KeyboardButton(text="Sergeli tumani")],
        [KeyboardButton(text="Mirobod tumani")],
        [KeyboardButton(text="Yakkasaroy tumani")],
        [KeyboardButton(text="Bektemir tumani")],
        [KeyboardButton(text="Yangihayot tumani")],
        [
            KeyboardButton(text="⬅Orqaga"),
            KeyboardButton(text="⬆Bosh Menyu")

        ]
    ]
)
for_order = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⬅Orqaga"),
            KeyboardButton(text="Buyurtmani Rasmiylashtirish")

        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
