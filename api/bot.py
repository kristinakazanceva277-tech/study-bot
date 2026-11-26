import os
import telebot
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@app.route('/', methods=['GET'])
def index():
    return "Бот работает! Я живой."

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Forbidden', 403

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Я учебный помощник. Я работаю!")

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "Я пока умею только здороваться.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, f"Вы сказали: {message.text}")
