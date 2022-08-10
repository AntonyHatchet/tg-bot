from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flows.callbacks import Callbacks
from flows.other.cooperation import other_cooperation_handler
from flows.other.other_club import other_club_handler
from flows.other.other_faq import other_faq_handler
from flows.other.other_media import other_media_handler

job_message = "Дорогой коллега!" \
    "\n\nЯ рад видеть тебя в этом разделе. Я с удовольствием рассмотрю твою анкету. Давай выясним, сможем ли мы, работая в команде, сделать этот мир немножко лучше, а отношения между людьми более доверительными? Переходи по ссылке и заполняй анкету." \
    "\n\nУже жду нашей встречи!"


def other():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Рассказать о своей проблеме в СМИ",
                             callback_data=Callbacks.other_media.name),
        InlineKeyboardButton("Подписаться на канал",
                             callback_data=Callbacks.other_subscribe.name),
        InlineKeyboardButton(
            "База знаний", callback_data=Callbacks.other_faq.name),
        InlineKeyboardButton(
            "Правовой клуб", callback_data=Callbacks.other_club.name),
        InlineKeyboardButton("Хочу у вас работать",
                             callback_data=Callbacks.other_jobs.name),
        InlineKeyboardButton("Предложить сотрудничество",
                             callback_data=Callbacks.other_cooperation.name),
    )
    return markup


def subscribe():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Канал «Инвестиции с Егором Рединым»",
                             url="https://t.me/redininvest"),
        InlineKeyboardButton("«Канал юриста ЕгораРедина»",
                             url="https://t.me/egorredin"),
        InlineKeyboardButton(
            "Группа Егора Редина в социальной сети ВК", url="https://vk.com/locuslegis"),
    )
    return markup


def other_handler(bot, call):
    if call.data == Callbacks.other.name:
        bot.send_message(call.message.chat.id,
                         "Выберете категорию", reply_markup=other())
    if call.data == Callbacks.other_subscribe.name:
        bot.send_message(call.message.chat.id,
                         "Выберете на какой канал вы хотите подписаться?", reply_markup=subscribe())
    if call.data == Callbacks.other_jobs.name:
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(
            InlineKeyboardButton(
                "Заполнить форму", url="https://forms.gle/jYxmTsQFeQiDxZap9"),
        )
        bot.send_message(call.message.chat.id,
                         job_message, reply_markup=markup)

    other_media_handler(bot, call)
    other_faq_handler(bot, call)
    other_club_handler(bot, call)
    other_cooperation_handler(bot, call)
