from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies.database import get_db
from app.services.hemis_api import HemisClient
from app.models.user import User
from typing import Any

router = APIRouter()

@router.get("/semesters/{telegram_id}")
async def get_semesters(telegram_id: int, db: Session = Depends(get_db)) -> Any:
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user or not user.hemis_token:
        raise HTTPException(status_code=401, detail="Avtorizatsiyadan o'tmagan")
    
    data = await HemisClient.get_semesters(user.hemis_token)
    if not data:
        # Token muddati tugagan bo'lishi mumkin, yangilaymiz
        new_token = await HemisClient.login(user.hemis_login, user.hemis_password)
        if new_token:
            user.hemis_token = new_token
            db.commit()
            data = await HemisClient.get_semesters(new_token)
        else:
            raise HTTPException(status_code=401, detail="Parol o'zgargan yoki xatolik")
            
    return data

@router.get("/subjects/{telegram_id}")
async def get_subjects(telegram_id: int, semester_id: str, db: Session = Depends(get_db)) -> Any:
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user or not user.hemis_token:
        raise HTTPException(status_code=401, detail="Avtorizatsiyadan o'tmagan")
    
    data = await HemisClient.get_subjects(user.hemis_token, semester_id)
    if not data:
        new_token = await HemisClient.login(user.hemis_login, user.hemis_password)
        if new_token:
            user.hemis_token = new_token
            db.commit()
            data = await HemisClient.get_subjects(new_token, semester_id)
        else:
            raise HTTPException(status_code=401, detail="Parol o'zgargan yoki xatolik")
    return data
