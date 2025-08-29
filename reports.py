from fastapi import APIRouter
router = APIRouter()

@router.get("/medical")
async def get_medical_reports():
    return {"message": "Medical reports endpoint"}

@router.get("/financial")  
async def get_financial_reports():
    return {"message": "Financial reports endpoint"}