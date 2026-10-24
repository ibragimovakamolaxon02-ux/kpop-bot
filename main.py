import os
import time
import telebot
from google import genai

# Tokenlarni xavfsiz o'zgaruvchilardan yoki to'g'ridan-to'g'ri olamiz
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8703749064:AAFKgjLG8qikIqnEsEgM07kKCtljl7idGc")
GEMINI_KEY = os.environ.get("GEMINI_KEY", "AQ.Ab8RN6KY6kx38KRU-jr892ARgjd7nsMK4q1n43xY9kFVPqcy-A")

ai_client = genai.Client(api_key=GEMINI_KEY)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

SYSTEM_INSTRUCTION = """
Siz K-pop bo'yicha mutaxassis va do'stona AI yordamchisiz. 
Foydalanuvchilar K-pop guruhlari (BLACKPINK, BTS, Stray Kids va barcha boshqa guruhlar), 
ularning a'zolari va qo'shiqlari haqida so'rashadi.
Har doim xushfe'l, samimiy va chiroyli emojilar ishlatib o'zbek tilida javob bering.
"""

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Salom! 🖤🩷 Men sening K-pop AI do'stingman! K-pop bo'yicha xohlagan savolingni berishing mumkin!")

@bot.message_handler(content_types=['text'])
def send_ai_response(message):
    for attempt in range(3):
        try:
            response = ai_client.models.generate_content(
                model='gemini-2.0-flash',
                contents=message.text,
                config={'system_instruction': SYSTEM_INSTRUCTION}
            )
            bot.send_message(message.chat.id, response.text)
            break
        except Exception as e:
            if "503" in str(e) and attempt < 2:
                time.sleep(2)
                continue
            else:
                bot.send_message(message.chat.id, "Google serveri hozircha biroz band. Iltimos, bir ozdan so'ng qayta yozib ko'ring! 🖤🩷")
                break

if __name__ == "__main__":
    try:
        bot.remove_webhook()
    except:
        pass
    
    print("K-pop bot ishga tushdi!")
    
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            time.sleep(3)
