from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flows.callbacks import Callbacks
from flows.main_menu import main_menu
from models.User import User
from planfix.planfix import create_payment_media_task

user_dict = {}
bot_dict = {}

first_message = "Готовы ли оплатить правовую консультацию? (оплата консультации не гарантирует освещение вашей ситуации в СМИ)"
explain_message = "Бесплатное освещение кейсов доверителей на канале Егора Редина осуществляется только в рамках проекта «PRO BONO»." \
    "\n\nХотите узнать условия бесплатной правовой поддержки в рамках этого проекта?"
thanks_message = "Благодарим вас за заявку. В течение рабочего дня с вами свяжутся специалисты"


def other_media():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Да, я готов(а)",
                             callback_data=Callbacks.other_media_yes.name),
        InlineKeyboardButton("Нет, не готов(а)",
                             callback_data=Callbacks.other_media_no.name),
    )
    return markup


def other_media_handler(bot, call):
    chat_id = call.message.chat.id
    if call.data == Callbacks.other_media.name:
        bot.send_message(call.message.chat.id,
                         first_message, reply_markup=other_media())
    if call.data == Callbacks.other_media_yes.name:
        user_dict[chat_id] = User(call.message.text)
        bot_dict[chat_id] = bot

        msg = bot.send_message(
            chat_id, "Как я могу к вам обращаться? (напишите имя)")
        bot.register_next_step_handler(msg, set_name)
    if call.data == Callbacks.other_media_no.name:
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(
            InlineKeyboardButton("Да, хочу",
                                 callback_data=Callbacks.pro_bono.name),
            InlineKeyboardButton("В главное меню",
                                 callback_data=Callbacks.main_menu.name),
        )
        bot.send_message(
            chat_id, explain_message, reply_markup=markup)


def set_name(message):
    chat_id = message.chat.id
    name = message.text
    user = User(name)
    user_dict[chat_id] = user
    msg = bot_dict[chat_id].send_message(
        chat_id, "Напишите ваш сотовый номер телефона. Если вы даете согласие на обработку персональных данных, то нажмите «Отправить»")
    bot_dict[chat_id].register_next_step_handler(msg, set_phone)


def set_phone(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    phone = message.text
    user.phone = phone
    create_payment_media_task(user.phone, user.name)
    bot_dict[chat_id].send_message(
        chat_id, thanks_message, reply_markup=main_menu())
