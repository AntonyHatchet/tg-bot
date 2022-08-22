from enum import Enum
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flows.callbacks import Callbacks
from planfix.planfix import create_payment_consultation_task
from models.User import User

ask_name_message = "Как я могу к вам обращаться? (напишите имя)"
ask_phone_message = ", напишите ваш номер телефона"
yes_we_can_message = ", да, мы можем помочь в указанной категории правовых вопросов. В каком формате вы хотели бы получить консультацию?"
maybe_we_can_message = ", у каждого юриста есть своя специализация и мы не можем знать всех законов нашей страны. " \
    "Если мы будем не компетентны в какой-то категории вопросов, то мы переадресуем ваш вопрос на наших коллег, за которых мы можем поручиться. " \
    "Внесенная вами оплата будет переведена им, а вы не останетесь без поддержки в любом случае. " \
    "Если вы согласны на эти условия, то в каком формате вы хотели бы получить консультацию?"
letter_consultation_text = "Письменная консультация в формате «Правового мнения» или «Legal Opinion» - самый предпочтительный вид консультации, " \
    "потому что наша команда максимально понятно и широко в письменном виде отвечает на все ваши вопросы, которые вас мучают, " \
    "а также сразу предоставляет вам шаблоны необходимых документов. То есть после такой письменной консультации вы (с высокой долей вероятности) сможете самостоятельно решить свой вопрос. " \
    "Срок составления заключения – 3 рабочих дня. Продолжить оформление этой услуги?"
price_text = "Стоимость личной консультации зависит от уровня сотрудника, который данную консультацию оказывает. Выберете желаемый уровень сотрудника"
prepayment_message = "Благодарим вас за заявку. С вами свяжутся в ближайшее время."
# prepayment_message = "Благодарим вас за заявку. Для начала работы, необходимо внести предоплату:"

user_dict = {}
bot_dict = {}


class Consultation(Enum):
    personal = 0
    phone = 1
    letter = 2


class Price(Enum):
    personal_other = 15000
    personal_self = 30000
    phone_other = 5000
    phone_self = 10000
    mail = 25000


def consultation_category():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton(
            "Судебный спор", callback_data=Callbacks.consultation_litigation.name),
        InlineKeyboardButton("Деловые отношения и бизнес",
                             callback_data=Callbacks.consultation_business.name),
        InlineKeyboardButton("Жилье и недвижимость",
                             callback_data=Callbacks.consultation_property.name),
        InlineKeyboardButton("Интеллектуальные права (авторство и товарные знаки)",
                             callback_data=Callbacks.consultation_copyright.name),
        InlineKeyboardButton("Семейное и наследственное право",
                             callback_data=Callbacks.consultation_inheritance.name),
        InlineKeyboardButton("Долги и банкротство",
                             callback_data=Callbacks.consultation_bankrupt.name),
        InlineKeyboardButton("Социальная и пенсионная сфера",
                             callback_data=Callbacks.consultation_pension.name),
        InlineKeyboardButton("Другая тема",
                             callback_data=Callbacks.consultation_other.name),
    )
    return markup


def consultation_type():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Хочу приехать лично в ваш офис в Москве",
                             callback_data=Callbacks.consultation_type_personal.name),
        InlineKeyboardButton("Мне нужна устная консультация по телефону",
                             callback_data=Callbacks.consultation_type_phone.name),
        InlineKeyboardButton("Мне нужна письменная консультация",
                             callback_data=Callbacks.consultation_type_letter.name),
    )
    return markup


def letter_consultation():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Заказать письменное правовое заключение",
                             callback_data=Callbacks.consultation_type_letter_yes.name),
        InlineKeyboardButton("Назад",
                             callback_data=Callbacks.consultation_type_letter_no.name),
    )
    return markup


def personal_prices():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Юрист из команды Егора Редина",
                             callback_data=Callbacks.consultation_personal_price_other.name),
        InlineKeyboardButton("Егор Редин",
                             callback_data=Callbacks.consultation_personal_price_self.name),
    )
    return markup


def phone_prices():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Юрист из команды Егора Редина",
                             callback_data=Callbacks.consultation_phone_price_other.name),
        InlineKeyboardButton("Егор Редин",
                             callback_data=Callbacks.consultation_phone_price_self.name),
    )
    return markup


def consultation_handler(bot, call):
    print("Top")
    print(call.data)
    chat_id = call.message.chat.id
    if call.data == Callbacks.consultation.name:
        msg = bot.send_message(chat_id, ask_name_message)
        bot.register_next_step_handler(msg, set_name)
        bot_dict[chat_id] = bot
        return
    if call.data == Callbacks.consultation_litigation.name:
        user = user_dict[chat_id]
        user.category = Callbacks.consultation_litigation.name
        bot.send_message(chat_id, user.name +
                         yes_we_can_message, reply_markup=consultation_type())
        return
    if call.data == Callbacks.consultation_business.name:
        user = user_dict[chat_id]
        user.category = Callbacks.consultation_business.name
        bot.send_message(chat_id, user.name +
                         yes_we_can_message, reply_markup=consultation_type())
        return
    if call.data == Callbacks.consultation_property.name:
        user = user_dict[chat_id]
        user.category = Callbacks.consultation_property.name
        bot.send_message(chat_id, user.name +
                         yes_we_can_message, reply_markup=consultation_type())
        return
    if call.data == Callbacks.consultation_copyright.name:
        user = user_dict[chat_id]
        user.category = Callbacks.consultation_copyright.name
        bot.send_message(chat_id, user.name +
                         yes_we_can_message, reply_markup=consultation_type())
        return
    if call.data == Callbacks.consultation_inheritance.name:
        user = user_dict[chat_id]
        user.category = Callbacks.consultation_inheritance.name
        bot.send_message(chat_id, user.name +
                         yes_we_can_message, reply_markup=consultation_type())
        return
    if call.data == Callbacks.consultation_bankrupt.name:
        user = user_dict[chat_id]
        user.category = Callbacks.consultation_bankrupt.name
        bot.send_message(chat_id, user.name +
                         yes_we_can_message, reply_markup=consultation_type())
        return
    if call.data == Callbacks.consultation_pension.name:
        user = user_dict[chat_id]
        user.category = Callbacks.consultation_property.name
        bot.send_message(chat_id, user.name +
                         yes_we_can_message, reply_markup=consultation_type())
        return
    if call.data == Callbacks.consultation_other.name:
        user = user_dict[chat_id]
        user.category = Callbacks.consultation_other.name
        bot.send_message(chat_id, user.name +
                         maybe_we_can_message, reply_markup=consultation_type())
        return
    if call.data == Callbacks.consultation_type_personal.name:
        user = user_dict[chat_id]
        user.type = Callbacks.consultation_type_personal.name
        bot.send_message(chat_id, price_text,
                         reply_markup=personal_prices())
        return
    if call.data == Callbacks.consultation_type_phone.name:
        print("Inside")
        user = user_dict[chat_id]
        user.type = Callbacks.consultation_type_phone.name
        bot.send_message(chat_id, price_text,
                         reply_markup=phone_prices())
        return
    if call.data == Callbacks.consultation_type_letter.name:
        user = user_dict[chat_id]
        user.type = Callbacks.consultation_type_letter.name
        bot.send_message(
            chat_id, letter_consultation_text, reply_markup=letter_consultation())
        return
    if call.data == Callbacks.consultation_personal_price_other.name:
        user = user_dict[chat_id]
        user.price = Price.personal_other.value
        create_payment_consultation_task(name=user.name, phone=user.phone,
                                         category=user.category, type=user.type, price=user.price)
        bot.send_message(
            chat_id, prepayment_message)
        return
    if call.data == Callbacks.consultation_personal_price_self.name:
        user = user_dict[chat_id]
        user.price = Price.personal_self.value
        create_payment_consultation_task(name=user.name, phone=user.phone,
                                         category=user.category, type=user.type, price=user.price)
        bot.send_message(
            chat_id, prepayment_message)
        return
    if call.data == Callbacks.consultation_phone_price_other.name:
        user = user_dict[chat_id]
        user.price = Price.phone_other.value
        create_payment_consultation_task(name=user.name, phone=user.phone,
                                         category=user.category, type=user.type, price=user.price)
        bot.send_message(
            chat_id, prepayment_message)
        return
    if call.data == Callbacks.consultation_phone_price_self.name:
        user = user_dict[chat_id]
        user.price = Price.phone_self.value
        create_payment_consultation_task(name=user.name, phone=user.phone,
                                         category=user.category, type=user.type, price=user.price)
        bot.send_message(
            chat_id, prepayment_message)
        return
    if call.data == Callbacks.consultation_type_letter_yes.name:
        user = user_dict[chat_id]
        user.price = Price.phone_self.value
        create_payment_consultation_task(name=user.name, phone=user.phone,
                                         category=user.category, type=user.type, price=Price.mail.value)
        bot.send_message(
            chat_id, prepayment_message)
        return
    if call.data == Callbacks.consultation_type_letter_no.name:
        bot.send_message(
            chat_id, "Выберете подходящий способ", reply_markup=consultation_type())
        return


def set_name(message):
    chat_id = message.chat.id
    name = message.text
    user = User(name)
    user_dict[chat_id] = user
    msg = bot_dict[chat_id].send_message(
        chat_id, message.text + ask_phone_message)
    bot_dict[chat_id].register_next_step_handler(msg, set_phone)


def set_phone(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    phone = message.text
    user.phone = phone
    bot_dict[chat_id].send_message(chat_id, user.name +
                                   ", выберете категорию вашего запроса", reply_markup=consultation_category())
