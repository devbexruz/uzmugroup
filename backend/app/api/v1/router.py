from fastapi import APIRouter
from app.api.v1.endpoints import auth, hemis

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Avtorizatsiya (Auth)"])
api_router.include_router(hemis.router, prefix="/hemis", tags=["HEMIS API"])
