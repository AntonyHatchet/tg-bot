from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flows.callbacks import Callbacks
from flows.main_menu import main_menu
from models.User import User

user_dict = {}
bot_dict = {}

first_message = "Правовой клуб – это сообщество профессиональных юристов и адвокатов, которые готовы обмениваться опытом друг с другом." \
    "\n\nПреимущества клуба:" \
    "\n\n• Егор Редин делится запросами из СМИ для юристов и адвокатов" \
    "\n\n• Егор рассказывает о своем опыте управления юридической фирмой" \
    "\n\n• Егор передает клиентов, которых не успевает обработать самостоятельно" \
    "\n\n• Мы организуем образовательные онлайн и крутые досуговые оффлайн встречи для членов клуба" \
    "\n\n• Все образовательные продукты Егора Редина предоставляются членам клуба с 25% скидкой" \
    "\n\nИ все это цене 3х чашек кофе в месяц!"


def other_club():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Я с вами!",
                             callback_data=Callbacks.other_club_yes.name),
        InlineKeyboardButton("Главное меню",
                             callback_data=Callbacks.main_menu.name),
    )
    return markup


def other_club_handler(bot, call):
    chat_id = call.message.chat.id
    if call.data == Callbacks.other_club.name:
        bot.send_message(call.message.chat.id,
                         first_message, reply_markup=other_club())
    if call.data == Callbacks.other_club_yes.name:
        user_dict[chat_id] = User(call.message.text)
        bot_dict[chat_id] = bot

        msg = bot.send_message(
            chat_id, "Как я могу к вам обращаться? (напишите имя)")
        bot.register_next_step_handler(msg, set_name)


def set_name(message):
    chat_id = message.chat.id
    name = message.text
    user = User(name)
    user_dict[chat_id] = user
    msg = bot_dict[chat_id].send_message(
        chat_id, "Напишите ваш сотовый номер телефона. Если вы даете согласие на обработку персональных данных, то нажмите «Отправить»")
    bot_dict[chat_id].register_next_step_handler(msg, send_request)


def send_request(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    phone = message.text
    user.phone = phone
    bot_dict[chat_id].send_message(
        chat_id, "Оплатить подписку 990 рублей в месяц")
