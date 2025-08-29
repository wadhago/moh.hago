from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date, datetime
from app.database.connection import get_db
from app.auth.security import get_current_user, PermissionChecker
from app.models.patient import Patient
from app.models.user import User
import uuid

router = APIRouter()

class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    first_name_ar: Optional[str] = None
    last_name_ar: Optional[str] = None
    date_of_birth: date
    gender: str
    blood_type: Optional[str] = None
    marital_status: Optional[str] = None
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None
    national_id: Optional[str] = None
    nationality: Optional[str] = "Saudi Arabia"

class PatientResponse(BaseModel):
    id: str
    patient_id: str
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    phone: str
    email: Optional[str]
    age: Optional[int]
    is_active: bool
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[PatientResponse])
async def get_patients(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all patients"""
    if not PermissionChecker.can_view_patients(current_user):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    query = db.query(Patient)
    
    if search:
        query = query.filter(
            (Patient.first_name.contains(search)) |
            (Patient.last_name.contains(search)) |
            (Patient.patient_id.contains(search)) |
            (Patient.phone.contains(search))
        )
    
    patients = query.offset(skip).limit(limit).all()
    return [PatientResponse.from_orm(patient) for patient in patients]

@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get patient by ID or patient_id"""
    if not PermissionChecker.can_view_patients(current_user):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    patient = db.query(Patient).filter(
        (Patient.id == patient_id) | (Patient.patient_id == patient_id)
    ).first()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return PatientResponse.from_orm(patient)

@router.post("/", response_model=PatientResponse)
async def create_patient(
    patient_data: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new patient"""
    if not PermissionChecker.can_modify_patients(current_user):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    # Generate patient ID
    patient_count = db.query(Patient).count()
    patient_id = f"P{(patient_count + 1):06d}"
    
    patient = Patient(
        id=str(uuid.uuid4()),
        patient_id=patient_id,
        **patient_data.dict()
    )
    
    db.add(patient)
    db.commit()
    db.refresh(patient)
    
    return PatientResponse.from_orm(patient)