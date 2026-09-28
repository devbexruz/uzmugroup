from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies.database import get_db
from app.services.hemis_api import HemisClient
from app.models.user import User
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    telegram_id: int
    hemis_login: str
    hemis_password: str
    full_name: str = ""
    group_name: str = ""

@router.post("/login")
async def login(data: LoginRequest, db: Session = Depends(get_db)):
    token = await HemisClient.login(data.hemis_login, data.hemis_password)
    if not token:
        raise HTTPException(status_code=401, detail="HEMIS login yoki parol noto'g'ri")
    
    user = db.query(User).filter(User.telegram_id == data.telegram_id).first()
    if user:
        user.hemis_token = token
        user.hemis_login = data.hemis_login
        user.hemis_password = data.hemis_password
        db.commit()
    else:
        new_user = User(
            telegram_id=data.telegram_id,
            hemis_login=data.hemis_login,
            hemis_password=data.hemis_password,
            hemis_token=token,
            full_name=data.full_name,
            group_name=data.group_name
        )
        db.add(new_user)
        db.commit()

    return {"message": "Muvaffaqiyatli", "token": token}
