import telebot
from telebot import types
import sqlite3
import json
from utils import (
    get_datas_from_hemis,
    get_info_message
)
from datetime import datetime
import titul
import os, cv2
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
import numpy as np
load_dotenv()


# Atrof-muhit o'zgaruvchilarini yuklash
BOT_TOKEN = os.getenv("UZMUGROUP_BOT_TOKEN")

# Admin Telegram ID
ADMIN_ID = int(os.getenv("UZMUGROUP_ADMIN_ID"))
# Ma'lumotlar bazasi fayli
DB_NAME = "students.db"

# Bot obyektini yaratish
bot = telebot.TeleBot(BOT_TOKEN)

# Ma'lumotlar bazasiga ulanish va jadvalni yaratish funksiyasi
def init_db():
    """Ma'lumotlar bazasiga ulanadi va agar mavjud bo'lmasa jadval yaratadi."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            telegram_id INTEGER PRIMARY KEY,
            telegram_username TEXT,
            phone_number TEXT,
            hemis_login TEXT UNIQUE,
            hemis_password TEXT,
            student_datas TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Foydalanuvchi ma'lumotlarini saqlash uchun lug'at
user_data = {}


@bot.message_handler(content_types=["photo"], func=lambda message: message.chat.id == ADMIN_ID)
def get_photo(message):
    # Download file
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    # Load PIL
    img = Image.open(BytesIO(downloaded_file))

    # RGB to BGR
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    result, img = titul.scan(img)

    _, buffer = cv2.imencode(".jpg", img)
    io_buf = BytesIO(buffer)

    # img in cv2.Mat
    count = sum(1 for a, b in zip(result, titul.questions_answers) if a == b)
    try:
        id_raqam = int(message.caption)
        # Databasedan qidirish
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE telegram_id = ?", (id_raqam,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            bot.send_message(
                message.chat.id,
                "Foydalanuvchi topilmadi"
            )
            return
        
    except:
        bot.send_message(
            message.chat.id,
            "Foydalanuvchi topilmadi"
        )
        return
    variatnlar = ''.join(result)
    t_javoblar = ''.join(titul.questions_answers)
    text_message = f"🎉 Tabriklaymiz siz muvvaffaqiyatli 2 - bosqichga o'tdingiz" if count >= 10 else f"Afsuski siz 2 - bosqichga o'ta olmadingiz"
    bot.send_photo(
        message.chat.id,
        io_buf,
        caption=f"✅ To'g'ri javoblar soni: **{count} ta**\n❌ Noto'g'ri javoblar soni: **{20 - count} ta**\n\nSizning javoblaringiz:\n{variatnlar}\nTo'g'ri javoblar:\n{t_javoblar}\n\n{text_message}\n\nYangiliklarni kuzatib boring.",
        parse_mode="Markdown",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("Natijani yuklash ✅", callback_data=f"natija_{id_raqam}")
        )
    )
# Callback handler
@bot.callback_query_handler(func=lambda call: call.data.startswith("natija_"))
def handle_callback(call):
    # ID raqamini olish
    id_raqam = call.data.split("_")[1]
    # Databasedan qidirish
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE telegram_id = ?", (id_raqam,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        bot.send_message(
            call.message.chat.id,
            "Foydalanuvchi topilmadi"
        )
        return
    # Natijani yuklash
    datas = json.loads(row[5])
    id_raqam = int(call.data.split("_")[1])
    bot.send_photo(
        id_raqam,
        call.message.photo[-1].file_id,
        caption=call.message.caption,
        parse_mode="Markdown",
        reply_markup=types.InlineKeyboardMarkup().add(
            # Yangiliklar kanali
            types.InlineKeyboardButton("Yangiliklar kanali 📢", url="https://t.me/uzmugroup"),
        )
    )
    bot.edit_message_caption(
        caption=call.message.caption+"\n\n✅ Natija muvaffaqiyatli yuklandi!",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )

# @username text kabi qidiruv qismi
@bot.inline_handler(func=lambda query: query.from_user.id == ADMIN_ID)
def inline_query(query):
    # Database dan o'qish
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    results = []
    for row in rows:
        datas = json.loads(row[5])
        if query.query.lower() in datas.get("first_name").lower()+" "+datas.get("last_name").lower():
            results.append(
                types.InlineQueryResultArticle(
                    id=str(row[0]),
                    title=str(row[0]),
                    description=datas.get("first_name")+" "+datas.get("last_name"),
                    input_message_content=types.InputTextMessageContent(
                        message_text=row[2],
                        parse_mode="Markdown"
                    )
                )
            )
    bot.answer_inline_query(query.id, results)
import requests
API_BASE_URL = "http://127.0.0.1:8000/api/v1"

# Start buyrug'i uchun handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    telegram_id = message.from_user.id
    
    # Backend orqali tizimda borligini tekshirish
    try:
        res = requests.get(f"{API_BASE_URL}/hemis/semesters/{telegram_id}")
        if res.status_code == 200:
            # Tizimga kirgan
            markup = types.InlineKeyboardMarkup(row_width=1)
            # Web app link (hozircha shunday)
            web_app_url = f"https://yourdomain.com/gpa?user_id={telegram_id}"
            markup.add(
                types.InlineKeyboardButton("🧮 GPA ni hisoblash", web_app=types.WebAppInfo(url=web_app_url)),
                types.InlineKeyboardButton("📚 Sessiyaga tayyorlanish fanlar", callback_data="sessiya")
            )
            bot.send_message(
                message.chat.id, 
                "O'zbekiston Milliy universiteti Talabalar yordamchi botiga xush kelibsiz!\n\n🎓 Asosiy bo'lim (Dashboard):", 
                reply_markup=markup
            )
        else:
            # Tizimga kirmagan (401 xatolik qaytadi)
            bot.send_message(
                message.chat.id, 
                "O'zbekiston Milliy universiteti Talabalar yordamchi botiga xush kelibsiz!\n\nTizimdan foydalanish uchun HEMIS loginingizni kiriting (Misol: 314241101530):"
            )
            bot.register_next_step_handler(message, get_bot_hemis_login)
    except Exception as e:
        bot.send_message(message.chat.id, "❌ Backend ishlamayapti. Kuting.")

def get_bot_hemis_login(message):
    user_id = message.from_user.id
    user_data[user_id] = {'hemis_login': message.text}
    bot.send_message(message.chat.id, "Ajoyib. Endi HEMIS parolingizni kiriting:")
    bot.register_next_step_handler(message, get_bot_hemis_password)

def get_bot_hemis_password(message):
    telegram_id = message.from_user.id
    login_str = user_data.get(telegram_id, {}).get('hemis_login')
    password_str = message.text
    
    if not login_str:
        bot.send_message(message.chat.id, "Xatolik! /start ni qayta bosing.")
        return
        
    msg = bot.send_message(message.chat.id, "⏳ Tizimga kirilmoqda, kuting...")
    
    payload = {
        "telegram_id": telegram_id,
        "hemis_login": login_str,
        "hemis_password": password_str,
        "full_name": message.from_user.first_name,
        "group_name": ""
    }
    
    try:
        res = requests.post(f"{API_BASE_URL}/auth/login", json=payload)
        if res.status_code == 200:
            bot.edit_message_text("✅ Muvaffaqiyatli tizimga kirdingiz!", message.chat.id, msg.message_id)
            # Dashboardni ochish
            send_welcome(message)
        else:
            bot.edit_message_text(f"❌ Login yoki parol xato: {res.json().get('detail')}\n\nQaytadan /start ni bosing.", message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text("❌ Backend server bilan aloqa yo'q.", message.chat.id, msg.message_id)



import time
# Botni doimiy ishlash holatiga o'tkazish
print("Bot ishga tushdi...")
while  __name__ == '__main__':
    try:
        bot.polling(non_stop=True)
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        time.sleep(5)
        print("Bot qayta ishga tushdi...")
        continue
