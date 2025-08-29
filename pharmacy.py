from fastapi import APIRouter, Depends, HTTPException
from app.auth.security import get_current_user, PermissionChecker
from app.models.user import User

router = APIRouter()

@router.get("/medications")
async def get_medications(current_user: User = Depends(get_current_user)):
    if not PermissionChecker.can_access_pharmacy(current_user):
        raise HTTPException(status_code=403, detail="Permission denied")
    return {"message": "Medications endpoint"}

@router.get("/sales")
async def get_pharmacy_sales(current_user: User = Depends(get_current_user)):
    if not PermissionChecker.can_access_pharmacy(current_user):
        raise HTTPException(status_code=403, detail="Permission denied")
    return {"message": "Pharmacy sales endpoint"}