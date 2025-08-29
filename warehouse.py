from fastapi import APIRouter
router = APIRouter()

@router.get("/items")
async def get_warehouse_items():
    return {"message": "Warehouse items endpoint"}

@router.get("/transactions")
async def get_warehouse_transactions():
    return {"message": "Warehouse transactions endpoint"}