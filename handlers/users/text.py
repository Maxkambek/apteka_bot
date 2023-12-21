bot_text = {
    "text_1": "Assalom-u alaykum, \nTezkor Apteka botiga xush kelibsiz!",
    "text_2": "Dorilarni qayerga yetkazib berish kerak\nIltimos tanlang:",
    "text_3": "Iltimos tummanni tanlang:⬇",
    "text_4": "Dori nomini kiriting:\nMasalan: <i>analgin</i>",
    "text_5": "Dorilar ro'yhatidan o'zingizga kerak dorini tanlang",
    "text_6": "Bunday nomdagi dori topilmadi.\nIltimos boshqa dori nomini kiriting:",
    "text_7": "Savatchaga muvaffaqqiyatli qo'shildi.",
    "text_8": "Savatchangiz bo'sh!",
    "text_9": "Buyurtmani rasmiylashtirish!⏩",
    "text_10": "Iltimos yetkazib berish lokatsiyasini jo'nating!",
}


def drug_msg(name, owner, price, expire):
    msg = ""
    msg += "⏩⏩⏩⏩⏩⏩⏩⏩⏩⏩⏩⏩⏩\n\n"
    msg += f"<b>Dori Nomi:</b> {name}\n\n<b>Ishlab chiqaruvchi:</b> {owner}\n"
    msg += f"<b>Yaroqlilik muddati:</b> {expire}\n\n"
    msg += f'<b>Narxi:</b> {price} sum'
    return msg
