import httpx
from typing import Optional, Dict, Any
import json

class HemisClient:
    BASE_URL = "https://hstudent.nuu.uz/rest/v1"
    
    @staticmethod
    async def login(login_str: str, password_str: str) -> Optional[str]:
        url = f"{HemisClient.BASE_URL}/auth/my-hemis-login"
        headers = {
            "accept": "*/*",
            "content-type": "application/json",
            "referrer": "https://my.hemis.uz/"
        }
        payload = {
            "login": login_str,
            "password": password_str
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    # API response'dan tokenni olish (API formatiga qarab o'zgartirilishi mumkin)
                    return data.get("data", {}).get("token") or data.get("token")
            except Exception as e:
                print(f"HEMIS Login Error: {e}")
        return None

    @staticmethod
    async def get_semesters(token: str) -> Optional[Dict[str, Any]]:
        url = f"{HemisClient.BASE_URL}/education/semesters?l=uz-UZ"
        headers = {
            "accept": "*/*",
            "authorization": f"Bearer {token}",
            "referrer": "https://my.hemis.uz/"
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers)
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                print(f"HEMIS Semesters Error: {e}")
        return None

    @staticmethod
    async def get_subjects(token: str, semester_id: str) -> Optional[Dict[str, Any]]:
        url = f"{HemisClient.BASE_URL}/education/subject-list?l=uz-UZ&semester={semester_id}"
        headers = {
            "accept": "*/*",
            "authorization": f"Bearer {token}",
            "referrer": "https://my.hemis.uz/"
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers)
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                print(f"HEMIS Subjects Error: {e}")
        return None
