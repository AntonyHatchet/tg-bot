from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flows.callbacks import Callbacks


def main_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Узнать про Егора Редина",
                             callback_data=Callbacks.about.name),
        InlineKeyboardButton("Записаться на платную консультацию",
                             callback_data=Callbacks.consultation.name),
        InlineKeyboardButton("PRO BONO (бесплатная поддержка граждан)",
                             callback_data=Callbacks.pro_bono.name),
        InlineKeyboardButton("Ангелы Права (защита бизнеса)",
                             callback_data=Callbacks.about.name),
        InlineKeyboardButton(
            "Другие вопросы", callback_data=Callbacks.other.name),
    )
    return markup
