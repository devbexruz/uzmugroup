import requests
class ServerConnection:
    def __init__(self):
        self.load_auth_token()
        self.base_url = "http://45.138.158.199:8002"
    def post_request(self, endpoint, data):
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=data)
        print(url)
        return response.json()
    def get_request(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url)
        print(url)
        return response.json()
    def upload_profile_image(self, auth_token, file_path):
        url = f"{self.base_url}/api/profile/upload-image/{auth_token}/"
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(url, files=files)
        return response.json()
    def get_profile_data(self, user_id):
        url = f"{self.base_url}/api/profile/get-image/{user_id}/"
        response = requests.get(url)
        return response.json()
    def login(self, login, password):
        url = f"{self.base_url}/api/auth/login/"
        data = {"login": login, "password": password}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            self.auth_token = response.json().get("auth_token")
            self.save_auth_token(self.auth_token)
        return response.json()
    def save_auth_token(self, token):
        self.auth_token = token
        with open("auth_token.txt", "w") as f:
            f.write(token)
    def load_auth_token(self):
        try:
            with open("auth_token.txt", "r") as f:
                self.auth_token = f.read().strip()
        except FileNotFoundError:
            self.auth_token = None
    def get_all_datas(self):
        if not self.auth_token:
            return {"error": "No auth token"}
        endpoint = f"/api/datas/get-all/{self.auth_token}/"
        return self.get_request(endpoint)
    def get_modul_data(self, modul_id):
        if not self.auth_token:
            return {"error": "No auth token"}
        endpoint = f"/api/datas/get-modul/{modul_id}/{self.auth_token}/"
        return self.get_request(endpoint)
    def get_lesson_data(self, lesson_id):
        if not self.auth_token:
            return {"error": "No auth token"}
        endpoint = f"/api/datas/get-lesson/{lesson_id}/{self.auth_token}/"
        return self.get_request(endpoint)
    def send_chat_message(self, course_id, content):
        if not self.auth_token:
            return {"error": "No auth token"}
        endpoint = f"/api/chat-messages/send/{course_id}/{self.auth_token}/"
        data = {"content": content}
        return self.post_request(endpoint, data)

server = ServerConnection()
