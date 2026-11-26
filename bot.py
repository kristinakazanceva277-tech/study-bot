from flask import Flask, request
import telegram
import os
import asyncio

app = Flask(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telegram.Bot(token=BOT_TOKEN)

@app.route('/')
def index():
    return "Бот работает!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Получаем данные от Telegram
        data = request.get_json(force=True)
        update = telegram.Update.de_json(data, bot)
        
        # Если пришло текстовое сообщение
        if update.message and update.message.text:
            chat_id = update.message.chat_id
            text = update.message.text
            
            # Создаем асинхронную функцию для отправки ответа
            async def send_reply():
                if text == '/start':
                    await bot.send_message(chat_id=chat_id, text="Привет! Я учебный помощник.")
                elif text == '/help':
                    await bot.send_message(chat_id=chat_id, text="Я пока умею только здороваться.")
                else:
                    await bot.send_message(chat_id=chat_id, text=f"Вы сказали: {text}")
            
            # Запускаем отправку
            asyncio.run(send_reply())
            
        return 'OK'
    except Exception as e:
        print(f"Ошибка: {e}")
        return 'Error', 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
