from flask import Flask, request
import telegram
import os

app = Flask(__name__)

# Берем токен из переменных окружения (безопасно)
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telegram.Bot(token=BOT_TOKEN)

@app.route('/')
def index():
    return "Бот работает!"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    if update.effective_message:
        chat_id = update.effective_chat.id
        text = update.effective_message.text
        
        if text == '/start':
            bot.send_message(chat_id=chat_id, text="Привет! Я учебный помощник.")
        elif text == '/help':
            bot.send_message(chat_id=chat_id, text="Я пока умею только здороваться и повторять за тобой.")
        else:
            bot.send_message(chat_id=chat_id, text=f"Вы сказали: {text}")
    return 'OK'

# Этот блок нужен для запуска на Render
if __name__ == '__main__':
    # Render сам подставит нужный порт в переменную PORT
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)