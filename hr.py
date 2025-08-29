from fastapi import APIRouter, Depends, HTTPException
from app.auth.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/employees")
async def get_employees(current_user: User = Depends(get_current_user)):
    if current_user.role not in ["admin", "hr_manager"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    return {"message": "HR employees endpoint"}

@router.get("/leaves")
async def get_employee_leaves(current_user: User = Depends(get_current_user)):
    if current_user.role not in ["admin", "hr_manager"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    return {"message": "Employee leaves endpoint"}