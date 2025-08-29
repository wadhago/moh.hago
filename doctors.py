from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import date
from app.database.connection import get_db
from app.auth.security import get_current_user, PermissionChecker
from app.models.doctor import Doctor, Department
from app.models.user import User
import uuid

router = APIRouter()

class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    first_name_ar: Optional[str] = None
    last_name_ar: Optional[str] = None
    date_of_birth: date
    gender: str
    specialization: str
    rank: str
    license_number: str
    department_id: str
    phone: str
    email: str
    consultation_fee: int = 0

class DoctorResponse(BaseModel):
    id: str
    employee_id: str
    full_name: str
    specialization: str
    rank: str
    department_id: str
    phone: str
    email: str
    is_active: bool
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[DoctorResponse])
async def get_doctors(
    skip: int = 0,
    limit: int = 100,
    department_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all doctors"""
    query = db.query(Doctor)
    
    if department_id:
        query = query.filter(Doctor.department_id == department_id)
    
    doctors = query.offset(skip).limit(limit).all()
    return [DoctorResponse.from_orm(doctor) for doctor in doctors]

@router.post("/", response_model=DoctorResponse)
async def create_doctor(
    doctor_data: DoctorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new doctor"""
    if current_user.role not in ["admin"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    # Generate employee ID
    doctor_count = db.query(Doctor).count()
    employee_id = f"DOC{(doctor_count + 1):04d}"
    
    doctor = Doctor(
        id=str(uuid.uuid4()),
        employee_id=employee_id,
        hire_date=date.today(),
        **doctor_data.dict()
    )
    
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    
    return DoctorResponse.from_orm(doctor)