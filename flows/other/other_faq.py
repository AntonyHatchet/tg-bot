from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flows.callbacks import Callbacks
from flows.main_menu import main_menu
from models.User import User
from planfix.planfix import create_faq_task

user_dict = {}
bot_dict = {}

first_message = "Давайте с вами познакомимся. Как вас зовут?"
explain_message = "Бесплатное освещение кейсов доверителей на канале Егора Редина осуществляется только в рамках проекта «PRO BONO»." \
    "\n\nХотите узнать условия бесплатной правовой поддержки в рамках этого проекта?"
thanks_message = "Благодарим вас за заявку. В течение рабочего дня с вами свяжутся специалисты"


def other_faq():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Юрист",
                             callback_data=Callbacks.other_faq_jurist.name),
        InlineKeyboardButton("Адвокат",
                             callback_data=Callbacks.other_faq_lawyer.name),
        InlineKeyboardButton("Предприниматель",
                             callback_data=Callbacks.other_faq_entrepreneur.name),
        InlineKeyboardButton("Обычный гражданин",
                             callback_data=Callbacks.other_faq_regular.name),
        InlineKeyboardButton("Госслужащий",
                             callback_data=Callbacks.other_faq_servant.name),
    )
    return markup


def other_faq_handler(bot, call):
    chat_id = call.message.chat.id
    if call.data == Callbacks.other_faq.name:
        user_dict[chat_id] = User(call.message.text)
        bot_dict[chat_id] = bot
        msg = bot.send_message(
            chat_id, "Как я могу к вам обращаться? (напишите имя)")
        bot.register_next_step_handler(msg, set_name)
    if call.data == Callbacks.other_faq_jurist.name:
        user = user_dict[chat_id]
        user.job = 'Юрист'
        send_request(chat_id)
    if call.data == Callbacks.other_faq_lawyer.name:
        user = user_dict[chat_id]
        user.job = 'Адвокат'
        send_request(chat_id)
    if call.data == Callbacks.other_faq_entrepreneur.name:
        user = user_dict[chat_id]
        user.job = 'Предприниматель'
        send_request(chat_id)
    if call.data == Callbacks.other_faq_regular.name:
        user = user_dict[chat_id]
        user.job = 'Обычный гражданин'
        send_request(chat_id)
    if call.data == Callbacks.other_faq_servant.name:
        user = user_dict[chat_id]
        user.job = 'Госслужащий'
        send_request(chat_id)


def set_name(message):
    chat_id = message.chat.id
    name = message.text
    user = User(name)
    user_dict[chat_id] = user
    msg = bot_dict[chat_id].send_message(
        chat_id, "Напишите ваш сотовый номер телефона.")
    bot_dict[chat_id].register_next_step_handler(msg, set_phone)


def set_phone(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    phone = message.text
    user.phone = phone
    bot_dict[chat_id].send_message(
        chat_id, "К какой категории вас можно отнести?", reply_markup=other_faq())


def send_request(chat_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("На сайт правовых знаний от Егора Редина",
                             url="www.znanie.egorredin.ru"),
    )
    bot_dict[chat_id].send_message(
        chat_id, "На странице,вы сможете найти бесплатные и платные гайды, подкасты, видео и курсы Егора Редина", reply_markup=markup)
    user = user_dict[chat_id]
    create_faq_task(user.name, user.phone, user.job)
