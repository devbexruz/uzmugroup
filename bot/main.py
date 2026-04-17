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
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Admin Telegram ID
ADMIN_ID = int(os.getenv("ADMIN_ID"))
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
# Start buyrug'i uchun handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """/start buyrug'iga javob beradi va ro'yxatdan o'tishni boshlaydi."""
    init_db()  # Ma'lumotlar bazasini ishga tushirish
    
    # Avval database da yaratilgan bo'lsa shunchaki oddiy salom berish kerak

    # Database dan o'qish
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE telegram_id = ?", (message.from_user.id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        # Avvalroq ro'yxatdan o'tgan bo'lsa
        datas = json.loads(row[5])

        bot.send_message(
            message.chat.id,
            f"Assalomu alaykum, {datas['first_name']} {datas['second_name']}!\nYangiliklarni telegram kanalda kuzatib boring",
            parse_mode="Markdown",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("📢 Yangiliklar kanali", url="https://t.me/uzmugroup")
            )
        )
        return
    

    # Vaqt   28 - sentabr 🗓 23:59 🕛 gacha
    # Agar bu vaqtdan o'tib ketgan bo'lsa Ro'yxatga olish yakunlangan deb chiqarsin
    now = datetime.now()
    if now > datetime(2025, 10, 5, 23, 59):
        bot.send_message(message.chat.id, "Ro'yxatdan o'tish yakunlangan")
        return

    user_id = message.from_user.id
    user_data[user_id] = {}  # Yangi foydalanuvchi uchun ma'lumotlar saqlash
    
    # Maxfiylik siyosati uchun tugmalar yaratamiz
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    agree_button = types.KeyboardButton("✅ Roziman")
    disagree_button = types.KeyboardButton("❌ Rozimasman")
    markup.add(agree_button, disagree_button)
    
    bot.send_message(
        message.chat.id,
        "Botdan foydalanishdan oldin, **Maxfiylik siyosati** bilan tanishib chiqing.\n\n"
        "Sizdan olingan shaxsiy ma'lumotlar (telefon raqami, HEMIS logini, paroli, HEMIS tizimidagi talaba profile hamda shaxsiy ma'lumotlari) faqatgina ta'lim jarayonini avtomatlashtirish maqsadida ishlatiladi. Ma'lumotlar himoyalangan holda saqlanadi.\n\n"
        "Ushbu shartlarga rozimisiz?",
        parse_mode="Markdown",
        reply_markup=markup
    )
    # Keyingi qadamga o'tish uchun handler belgilash
    bot.register_next_step_handler(message, privacy_policy_check)

# Maxfiylik siyosatiga rozilikni tekshirish
def privacy_policy_check(message):
    """Foydalanuvchining Maxfiylik siyosatiga roziligini tekshiradi."""
    if message.text == "✅ Roziman":
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        contact_button = types.KeyboardButton('📲 Telefon raqamni yuborish', request_contact=True)
        markup.add(contact_button)
        
        msg = bot.send_message(
            message.chat.id,
            "Ajoyib! Endi ro'yxatdan o'tish uchun telefon raqamingizni yuboring. Quyidagi tugmadan foydalanishingiz mumkin.",
            reply_markup=markup
        )
        bot.register_next_step_handler(msg, get_contact)
    elif message.text == "❌ Rozimasman":
        markup = types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id,
            "Tushunarli. Afsuski, maxfiylik siyosatiga roziliksiz tizimdan foydalana olmaysiz. Agar fikringiz o'zgarsa, qayta /start buyrug'ini yuboring.",
            reply_markup=markup
        )
        user_id = message.from_user.id
        if user_id in user_data:
            del user_data[user_id]
    else:
        # Agar foydalanuvchi tugmalardan boshqa narsa kiritsa
        bot.send_message(message.chat.id, "Iltimos, faqat tugmalardan birini bosing.")
        bot.register_next_step_handler(message, privacy_policy_check)


# Kontakt ma'lumotini qabul qilish handleri
def get_contact(message):
    """Foydalanuvchi yuborgan kontakt ma'lumotini qabul qiladi."""
    if not message.contact:
        bot.send_message(message.chat.id, "Iltimos, pastdagi tugmadan foydalanib telefon raqamingizni yuboring.")
        bot.register_next_step_handler(message, get_contact)
        return

    if message.contact.user_id != message.from_user.id:
        bot.send_message(message.chat.id, "Iltimos, o'zingizning telefon raqamingizni yuboring.")
        bot.register_next_step_handler(message, get_contact)
        return
        
    user_id = message.from_user.id
    user_data[user_id]['phone_number'] = message.contact.phone_number
    
    markup = types.ReplyKeyboardRemove()
    msg = bot.send_message(message.chat.id, "Ajoyib! Endi HEMIS loginingizni kiriting:", reply_markup=markup)
    bot.register_next_step_handler(msg, get_hemis_login)


# HEMIS loginini qabul qilish handleri
def get_hemis_login(message):
    """Foydalanuvchi yuborgan HEMIS loginini qabul qiladi."""
    user_id = message.from_user.id
    user_data[user_id]['hemis_login'] = message.text
    
    msg = bot.send_message(message.chat.id, "Rahmat. Endi HEMIS parolingizni kiriting:")
    bot.register_next_step_handler(msg, get_hemis_password)


# HEMIS parolini qabul qilish va ma'lumotlarni saqlash handleri
def get_hemis_password(message):
    """Foydalanuvchi yuborgan HEMIS parolini qabul qiladi va barcha ma'lumotlarni saqlaydi."""
    user_id = message.from_user.id
    if user_id not in user_data:
        bot.send_message(message.chat.id, "Xatolik yuz berdi. Iltimos, /start buyrug'idan boshlang.")
        return
        
    user_data[user_id]['hemis_password'] = message.text

    telegram_username = message.from_user.username if message.from_user.username else "Mavjud emas"
    phone_number = user_data[user_id]['phone_number']
    hemis_login = user_data[user_id]['hemis_login']
    hemis_password = user_data[user_id]['hemis_password']
    # Malumotlarni HEMIS tizimidan olish
    data = get_datas_from_hemis(hemis_login, hemis_password, bot)
    if not data["status"]:
        bot.send_message(message.chat.id, data["detail"])
        bot.register_next_step_handler(message, get_hemis_login)
        return
    user_data[user_id]['datas'] = data["datas"]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(types.KeyboardButton("✅ Ha"),types.KeyboardButton("❌ Yo'q"))
    bot.send_message(
        message.chat.id,
        get_info_message(data["datas"]),
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=markup
    )
    bot.register_next_step_handler(message, save_data)

def save_data(message):
    user_id = message.from_user.id
    telegram_username = message.from_user.username if message.from_user.username else "Mavjud emas"
    phone_number = user_data[user_id]['phone_number']
    hemis_login = user_data[user_id]['hemis_login']
    hemis_password = user_data[user_id]['hemis_password']
    datas = user_data[user_id]['datas']
    if message.text == "❌ Yo'q":
        bot.send_message(message.chat.id, "Ma'lumotlar saqlanmadi.\nQayta urinib ko'rish uchun /start buyrug'ini yuboring.")
        return
    elif message.text != "✅ Ha":
        return
    # Ma'lumotlar bazasiga ma'lumotlarni qo'shish
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO students (telegram_id, telegram_username, phone_number, hemis_login, hemis_password, student_datas)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, telegram_username, phone_number, hemis_login, hemis_password, json.dumps(datas, indent=4, ensure_ascii=False)))
        conn.commit()
        
        # Muvaffaqiyatli saqlangandan keyin yangi xabar
        bot.send_message(message.chat.id, 
            "Ma'lumotlaringiz muvaffaqiyatli saqlandi! Tez orada **keyingi bosqichlar haqida xabar beriladi**.",
            parse_mode="Markdown",
            # kanalni inline tugma qilib qo'shish
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("📢 Yangiliklar kanali", url="https://t.me/uzmugroup")
            )
        )
    except Exception as e:
        bot.send_message(message.chat.id, f"Ma'lumotlarni saqlashda xatolik yuz berdi: {e}")
    finally:
        conn.close()
        # Ma'lumotni lug'atdan o'chirish
        del user_data[user_id]


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
