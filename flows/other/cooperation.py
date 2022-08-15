from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flows.callbacks import Callbacks
from flows.main_menu import main_menu
from models.User import User
from planfix.planfix import create_cooperation_task

user_dict = {}
bot_dict = {}

first_message = "Добрый день." \
    "\n\nРад, что у вас есть для меня деловое предложение. Давайте попробуем совместными усилиями сделать этот мир лучше." \
    "\n\nНажмите пожалуйста на подходящую вам категорию."


def other_cooperation():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Я – представитель СМИ",
                             callback_data=Callbacks.other_cooperation_media.name),
        InlineKeyboardButton("Я – представитель государственных органов",
                             callback_data=Callbacks.other_cooperation_gov.name),
        InlineKeyboardButton("Я – представитель институтов развития или ВУЗа",
                             callback_data=Callbacks.other_cooperation_isntitute.name),
        InlineKeyboardButton("Я – представитель иной категории",
                             callback_data=Callbacks.other_cooperation_other.name),

    )
    return markup


def other_cooperation_handler(bot, call):
    chat_id = call.message.chat.id
    user = User('')
    user_dict[chat_id] = user
    bot_dict[chat_id] = bot
    if call.data == Callbacks.other_cooperation.name:
        bot.send_message(call.message.chat.id,
                         first_message, reply_markup=other_cooperation())
    if call.data == Callbacks.other_cooperation_media.name:
        user.cooperation = 'СМИ'
        msg = bot.send_message(
            chat_id, "Как я могу к вам обращаться? (напишите имя)")
        bot.register_next_step_handler(msg, set_name)
    if call.data == Callbacks.other_cooperation_gov.name:
        user.cooperation = 'Государственные органы'
        msg = bot.send_message(
            chat_id, "Как я могу к вам обращаться? (напишите имя)")
        bot.register_next_step_handler(msg, set_name)
    if call.data == Callbacks.other_cooperation_isntitute.name:
        user.cooperation = 'ВУЗ'
        msg = bot.send_message(
            chat_id, "Как я могу к вам обращаться? (напишите имя)")
        bot.register_next_step_handler(msg, set_name)
    if call.data == Callbacks.other_cooperation_other.name:
        user.cooperation = 'Другое'
        msg = bot.send_message(
            chat_id, "Как я могу к вам обращаться? (напишите имя)")
        bot.register_next_step_handler(msg, set_name)


def set_name(message):
    chat_id = message.chat.id
    name = message.text
    user = user_dict[chat_id]
    user.name = name
    msg = bot_dict[chat_id].send_message(
        chat_id, "Напишите ваш сотовый номер телефона. Если вы даете согласие на обработку персональных данных, то нажмите «Отправить»")
    bot_dict[chat_id].register_next_step_handler(msg, send_request)


def send_request(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    phone = message.text
    user.phone = phone
    create_cooperation_task(user.name, user.phone, user.cooperation)
    bot_dict[chat_id].send_message(
        chat_id, "Благодарим вас за заявку. Егор Редин свяжется с вами в ближайшее время.", reply_markup=main_menu())
