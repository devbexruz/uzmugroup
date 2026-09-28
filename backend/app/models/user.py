from sqlalchemy import Column, Integer, BigInteger, String, Boolean
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    group_name = Column(String, nullable=True)
    
    hemis_login = Column(String, unique=True, index=True, nullable=False)
    hemis_password = Column(String, nullable=False) # Parolni saqlaymiz (Token eskiganda orqa fonda yangilash uchun)
    hemis_token = Column(String, nullable=True)
    
    is_active = Column(Boolean(), default=True)
