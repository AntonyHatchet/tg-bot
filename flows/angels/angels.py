from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flows.callbacks import Callbacks
from models.User import User

user_dict = {}
bot_dict = {}

message = "Мы можем предложить судебную защиту вашего бизнеса без каких-либо предоплат на следующих условиях:" \
    "\n\n1. Вы переходите на сайт проекта «Ангелы Права», прикладываете документы и текстом кратко описываете вашу ситуацию" \
    "\n\n2. Егор Редин в течение 3-5 дней принимает решение – готовы ли мы взяться за вашу защиту и на каких условиях." \
    "\n\n3. Если мы готовы взяться за ваше дело на условиях проекта «Ангелы Права», то далее:" \
    "\n\n4. Мы подписываем с вами соглашение, по которому вы нам ничего не платите в качестве предоплаты, но, в случае если мы выигрываем судебный процесс - мы возьмем оплату в виде % от суммы иска или дела." \
    "\n\n5. По окончанию судебного процесса (в случае положительного решения суда), вы в обязательном порядке даете нам видео отзыв." \
    "\n\nСогласны ли вы с обозначенным выше порядком?"

angels_site_message = "Для получения более детальной информации вы можете перейти на сайт проекта Ангелыправа.рф"


def pro_bono():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Да, согласен(а)",
                             callback_data=Callbacks.angels_yes.name),
        InlineKeyboardButton("Вернуться в главное меню",
                             callback_data=Callbacks.main_menu.name),
    )
    return markup


def pro_bono_site():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Да, согласен(а)",
                             url="https://ангелыправа.рф"),
        InlineKeyboardButton("Вернуться в главное меню",
                             callback_data=Callbacks.main_menu.name),
    )
    return markup


def pro_bono_handler(bot, call):
    if call.data == Callbacks.angels.name:
        bot.send_message(call.message.chat.id,
                         message, reply_markup=pro_bono())
    if call.data == Callbacks.angels_yes.name:
        chat_id = call.message.chat.id
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
    bot_dict[chat_id].register_next_step_handler(msg, set_phone)


def set_phone(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    phone = message.text
    user.phone = phone
    bot_dict[chat_id].send_message(
        chat_id, angels_site_message, reply_markup=pro_bono_site())
