from fastapi import APIRouter, Depends
from app.auth.security import get_current_user, PermissionChecker
from app.models.user import User

router = APIRouter()

@router.get("/visits")
async def get_emergency_visits(current_user: User = Depends(get_current_user)):
    if not PermissionChecker.can_access_emergency(current_user):
        raise HTTPException(status_code=403, detail="Permission denied")
    return {"message": "Emergency visits endpoint - to be implemented"}

@router.post("/visits")
async def create_emergency_visit(current_user: User = Depends(get_current_user)):
    if not PermissionChecker.can_access_emergency(current_user):
        raise HTTPException(status_code=403, detail="Permission denied")
    return {"message": "Create emergency visit endpoint - to be implemented"}