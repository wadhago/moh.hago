from fastapi import APIRouter
router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats():
    return {
        "total_patients": 1250,
        "active_appointments": 45,
        "emergency_cases": 12,
        "available_beds": 23
    }