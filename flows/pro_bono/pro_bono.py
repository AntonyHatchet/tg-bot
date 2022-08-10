from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flows.callbacks import Callbacks
from models.User import User

user_dict = {}
bot_dict = {}


message = "Бесплатная поддержка граждан осуществляется в следующем порядке:" \
    "\n\n1. Вы от руки или на компьютере пишите на бумаге письмо о вашей правовой проблеме и прикладываете все документы, которые считаете нужным." \
    "\n\n2. В вашем письме вы пишите «Я, ФИО, даю согласие Редину Егору Анатольевичу на обработку моих персональных данных, а также обнародование и разглашение моей истории любым способом» (публикация будет осуществлена без указания личных данных, за исключением вашего имени и города проживания)." \
    "\n\n3. Вы отправляете данное письмо Почтой России в офис Егора Редина по адресу 123557, город Москва, Средний Тишинский переулок, дом 8, офис 8 (Егору Редину)." \
    "\n\n4. Егор Редин в течение 30 календарных дней изучает ваш вопрос и дает такой же письменный ответ, который отправляет почтой на ваш адрес." \
    "\n\n5. После этого, Егор Редин может снять выпуск передачи «PRO BONO», где расскажет о вашей истории и отвечает на ваши вопросы (без разглашения личной информации кроме Имени и города) и выкладывает ее на свой канал на ютубе."

pro_bono_site_message = "Для получения более детальной информации вы можете перейти на сайт проекта PRO BONO"


def pro_bono():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Да, согласен(а)",
                             callback_data=Callbacks.pro_bono_yes.name),
        InlineKeyboardButton("Вернуться в главное меню",
                             callback_data=Callbacks.main_menu.name),
    )
    return markup


def pro_bono_site():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Да, согласен(а)",
                             url="https://пробоно.рус/"),
        InlineKeyboardButton("Вернуться в главное меню",
                             callback_data=Callbacks.main_menu.name),
    )
    return markup


def pro_bono_handler(bot, call):
    if call.data == Callbacks.pro_bono.name:
        bot.send_message(call.message.chat.id,
                         message, reply_markup=pro_bono())
    if call.data == Callbacks.pro_bono_yes.name:
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
        chat_id, pro_bono_site_message, reply_markup=pro_bono_site())
