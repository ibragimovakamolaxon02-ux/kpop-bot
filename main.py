import os
import threading
from flask import Flask
import telebot
from google import genai

# 1. Kichik veb-server (Render o'chib qolmasligi uchun)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# Veb-serverni alohida oqimda ishga tushiramiz
threading.Thread(target=run_flask, daemon=True).start()

# 2. Telegram bot va Gemini sozlamalari
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=4)

# Gemini API mijozini sozlash (API kalit Render muhitidan olinadi)
client = genai.Client()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Men sizning K-pop AI do'stingizman! K-pop bo'yicha istalgan savolingizni berishingiz mumkin! 🖤💖")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    try:
        # Colab'dagi kabi foydalanuvchi yozgan matnni to'g'ridan-to'g'ri Gemini'ga yuboramiz
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=message.text,
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Xatolik yuz berdi: {e}")

if __name__ == "__main__":
    print("K-pop bot ishga tushdi!")
    bot.infinity_polling(skip_pending=True)
