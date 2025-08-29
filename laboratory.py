from fastapi import APIRouter, Depends, HTTPException
from app.auth.security import get_current_user, PermissionChecker
from app.models.user import User

router = APIRouter()

@router.get("/tests")
async def get_lab_tests(current_user: User = Depends(get_current_user)):
    if not PermissionChecker.can_access_laboratory(current_user):
        raise HTTPException(status_code=403, detail="Permission denied")
    return {"message": "Laboratory tests endpoint - to be implemented"}

@router.get("/orders")
async def get_lab_orders(current_user: User = Depends(get_current_user)):
    if not PermissionChecker.can_access_laboratory(current_user):
        raise HTTPException(status_code=403, detail="Permission denied")
    return {"message": "Laboratory orders endpoint - to be implemented"}