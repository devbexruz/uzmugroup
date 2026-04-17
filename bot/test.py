from sqlite3 import connect
import json

db = connect('students.db')
cursor = db.cursor()


# SELECT so‘rovi
cursor.execute("SELECT telegram_id, student_datas FROM students")

# 1) Hammasini olish
rows = cursor.fetchall()

def strip(s):
    return s.strip() if isinstance(s, str) else s

key = input("Field name: ")
qidiruv = input("Qidiruv qiymati: ")
outs = list(map(strip, input("Chiquvchi fieldlar (__, __, ...): ").split(",")))


for row in rows:
    student_datas = json.loads(row[1])
    if qidiruv in student_datas.get(key):
        print(row[0], *[student_datas.get(k) for k in outs], sep=" | ")

