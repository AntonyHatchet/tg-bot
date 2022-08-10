from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flows.callbacks import Callbacks

about_message = "Егор Редин – профессиональный юрист и управляющий партнер юридической компании «Позиция Права»." \
    "\n\nЛичная правовая практика с 2007 года." \
    "Более 95 % выигранных судебных споров." \
    "Самый цитируемый юрист России в печатных СМИ - более 4000 публикаций, комментариев и эфиров в СМИ с 2019 года. Хотите записаться на консультацию?"


def about():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Записаться на платную консультацию",
                             callback_data=Callbacks.consultation.name),
        InlineKeyboardButton("Посмотреть свежие публикации в СМИ",
                             url="https://newssearch.yandex.ru/news/search?text=%D0%B5%D0%B3%D0%BE%D1%80+%D1%80%D0%B5%D0%B4%D0%B8%D0%BD&rpt=nnews2&grhow=clutop&source=tabbar&flat=1&sortby=date"),
        InlineKeyboardButton("Вернуться в главное меню",
                             callback_data=Callbacks.main_menu.name),
    )
    return markup


def about_handler(bot, call):
    if call.data == Callbacks.about.name:
        bot.send_message(call.message.chat.id,
                         about_message, reply_markup=about())
