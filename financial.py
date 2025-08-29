from fastapi import APIRouter, Depends, HTTPException
from app.auth.security import get_current_user, PermissionChecker
from app.models.user import User

router = APIRouter()

@router.get("/invoices")
async def get_invoices(current_user: User = Depends(get_current_user)):
    if not PermissionChecker.can_access_financial(current_user):
        raise HTTPException(status_code=403, detail="Permission denied")
    return {"message": "Financial invoices endpoint"}

@router.get("/payments")
async def get_payments(current_user: User = Depends(get_current_user)):
    if not PermissionChecker.can_access_financial(current_user):
        raise HTTPException(status_code=403, detail="Permission denied")
    return {"message": "Payments endpoint"}