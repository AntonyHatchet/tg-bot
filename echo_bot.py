import os
import telebot
from dotenv import load_dotenv

from telebot.storage import StateRedisStorage

from flows.callbacks import Callbacks
from flows.main_menu import main_menu
from flows.angels.angels import angels_handler
from flows.other.other import other_handler
from flows.about.about import about_handler
from flows.consultation.consultation import consultation_handler
from flows.pro_bono.pro_bono import pro_bono_handler

load_dotenv()

bot_token = os.getenv('bot_token')

state_storage = StateRedisStorage()  # you can init here another storage
bot = telebot.TeleBot(
    bot_token, state_storage=state_storage)


@bot.message_handler(commands=['s', 'start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Как я могу вам помочь?",
                     reply_markup=main_menu())


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == Callbacks.main_menu.name:
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id,
                         "Как я могу вам помочь?", reply_markup=main_menu())

    about_handler(bot, call)
    other_handler(bot, call)
    consultation_handler(bot, call)
    pro_bono_handler(bot, call)
    angels_handler(bot, call)


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.infinity_polling(skip_pending=True)
