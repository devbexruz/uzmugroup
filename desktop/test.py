from requests import Session as b
b = b()
while True:
    res = b.post(
        "http://127.0.0.1:8000/api/chat-messages/send/1/a7708050-f439-481c-8d2c-c2dbe42af496/",
        json = {
            "content":[
                {
                    "type": "text",
                    "text": input("Text: ")
                }
            ]
        }
    )
print(res.json())






# from requests import Session
# b = Session()
# from tkinter import filedialog
# import json

# file_path = filedialog.askopenfilename()
# print(file_path)
# with open(file_path, "rb") as f:
#     res = b.post(
#         "http://127.0.0.1:8000/api/profile/upload-image/awdasnehdgfbajhefjwjhegjasvyef/",
#         files={"file": f}  # multipart/form-data orqali yuborish
#     )
# print(res.json())