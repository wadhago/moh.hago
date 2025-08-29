from fastapi import APIRouter, Depends, HTTPException
from app.auth.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/exams")
async def get_radiology_exams(current_user: User = Depends(get_current_user)):
    return {"message": "Radiology exams endpoint"}

@router.get("/orders")
async def get_radiology_orders(current_user: User = Depends(get_current_user)):
    return {"message": "Radiology orders endpoint"}