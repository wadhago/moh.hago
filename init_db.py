#!/usr/bin/env python3
"""
Database initialization script for Hospital Management System
Creates database tables and inserts initial data
"""

import sys
import os
from datetime import date, datetime
import uuid

# Add the parent directory to the path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from app.core.config import get_settings
from app.database.connection import Base, SessionLocal
from app.models.user import User, DEFAULT_PERMISSIONS
from app.models.doctor import Department, Doctor, HOSPITAL_DEPARTMENTS, MEDICAL_SPECIALIZATIONS
from app.models.patient import Patient
from app.auth.security import hash_password

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    
    settings = get_settings()
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False
    
    return True

def create_admin_user(db):
    """Create default admin user"""
    print("Creating admin user...")
    
    # Check if admin user already exists
    existing_admin = db.query(User).filter(User.username == "admin").first()
    if existing_admin:
        print("ℹ️  Admin user already exists")
        return existing_admin
    
    admin_user = User(
        id=str(uuid.uuid4()),
        username="admin",
        email="admin@hospital.com",
        full_name="System Administrator",
        phone="+966123456789",
        hashed_password=hash_password("admin123"),
        role="admin",
        permissions=DEFAULT_PERMISSIONS["admin"],
        is_active=True,
        is_verified=True
    )
    
    db.add(admin_user)
    print("✅ Admin user created successfully")
    print("   Username: admin")
    print("   Password: admin123")
    print("   ⚠️  Please change the password after first login!")
    
    return admin_user

def create_departments(db):
    """Create hospital departments"""
    print("Creating hospital departments...")
    
    for dept_data in HOSPITAL_DEPARTMENTS:
        existing_dept = db.query(Department).filter(Department.code == dept_data["code"]).first()
        if existing_dept:
            continue
            
        department = Department(
            id=str(uuid.uuid4()),
            name=dept_data["name_en"],
            name_ar=dept_data["name_ar"],
            code=dept_data["code"],
            description=f"{dept_data['name_en']} Department",
            description_ar=f"قسم {dept_data['name_ar']}"
        )
        
        db.add(department)
    
    print(f"✅ Created {len(HOSPITAL_DEPARTMENTS)} departments")

def create_sample_doctors(db):
    """Create sample doctors"""
    print("Creating sample doctors...")
    
    # Get some departments
    emergency_dept = db.query(Department).filter(Department.code == "EMER").first()
    cardiology_dept = db.query(Department).filter(Department.code == "CARD").first()
    
    if not emergency_dept or not cardiology_dept:
        print("⚠️  Departments not found, skipping doctor creation")
        return
    
    sample_doctors = [
        {
            "first_name": "Ahmed", "last_name": "Al-Rashid",
            "first_name_ar": "أحمد", "last_name_ar": "الراشد",
            "specialization": "Emergency Medicine", "specialization_ar": "طب الطوارئ",
            "rank": "consultant", "department": emergency_dept,
            "email": "ahmed.rashid@hospital.com", "phone": "+966501234567"
        },
        {
            "first_name": "Fatima", "last_name": "Al-Zahra",
            "first_name_ar": "فاطمة", "last_name_ar": "الزهراء",
            "specialization": "Cardiology", "specialization_ar": "أمراض القلب",
            "rank": "specialist", "department": cardiology_dept,
            "email": "fatima.zahra@hospital.com", "phone": "+966502345678"
        }
    ]
    
    created_count = 0
    for i, doctor_data in enumerate(sample_doctors, 1):
        existing_doctor = db.query(Doctor).filter(Doctor.email == doctor_data["email"]).first()
        if existing_doctor:
            continue
            
        doctor = Doctor(
            id=str(uuid.uuid4()),
            employee_id=f"DOC{i:04d}",
            first_name=doctor_data["first_name"],
            last_name=doctor_data["last_name"],
            first_name_ar=doctor_data["first_name_ar"],
            last_name_ar=doctor_data["last_name_ar"],
            date_of_birth=date(1980, 1, 1),
            gender="male" if doctor_data["first_name"] == "Ahmed" else "female",
            specialization=doctor_data["specialization"],
            specialization_ar=doctor_data["specialization_ar"],
            rank=doctor_data["rank"],
            license_number=f"LIC{i:06d}",
            department_id=doctor_data["department"].id,
            phone=doctor_data["phone"],
            email=doctor_data["email"],
            hire_date=date.today(),
            consultation_fee=20000,  # 200 SAR in halalas
            nationality="Saudi Arabia"
        )
        
        db.add(doctor)
        created_count += 1
    
    print(f"✅ Created {created_count} sample doctors")

def create_sample_patients(db):
    """Create sample patients"""
    print("Creating sample patients...")
    
    sample_patients = [
        {
            "first_name": "Mohammed", "last_name": "Al-Salem",
            "first_name_ar": "محمد", "last_name_ar": "السالم",
            "phone": "+966501111111", "email": "mohammed.salem@email.com",
            "date_of_birth": date(1985, 6, 15), "gender": "male",
            "national_id": "1234567890"
        },
        {
            "first_name": "Aisha", "last_name": "Al-Mahmoud",
            "first_name_ar": "عائشة", "last_name_ar": "المحمود",
            "phone": "+966502222222", "email": "aisha.mahmoud@email.com",
            "date_of_birth": date(1992, 3, 22), "gender": "female",
            "national_id": "0987654321"
        }
    ]
    
    created_count = 0
    for i, patient_data in enumerate(sample_patients, 1):
        existing_patient = db.query(Patient).filter(Patient.national_id == patient_data["national_id"]).first()
        if existing_patient:
            continue
            
        patient = Patient(
            id=str(uuid.uuid4()),
            patient_id=f"P{i:06d}",
            first_name=patient_data["first_name"],
            last_name=patient_data["last_name"],
            first_name_ar=patient_data["first_name_ar"],
            last_name_ar=patient_data["last_name_ar"],
            date_of_birth=patient_data["date_of_birth"],
            gender=patient_data["gender"],
            phone=patient_data["phone"],
            email=patient_data["email"],
            national_id=patient_data["national_id"],
            nationality="Saudi Arabia",
            address="Riyadh, Saudi Arabia",
            address_ar="الرياض، المملكة العربية السعودية"
        )
        
        db.add(patient)
        created_count += 1
    
    print(f"✅ Created {created_count} sample patients")

def main():
    """Main initialization function"""
    print("🏥 Hospital Management System Database Initialization")
    print("=" * 60)
    
    # Create tables
    if not create_tables():
        return
    
    # Initialize database session
    db = SessionLocal()
    
    try:
        # Create initial data
        create_admin_user(db)
        create_departments(db)
        create_sample_doctors(db)
        create_sample_patients(db)
        
        # Commit all changes
        db.commit()
        print("\n✅ Database initialization completed successfully!")
        print("\n📊 Summary:")
        print(f"   - Users: {db.query(User).count()}")
        print(f"   - Departments: {db.query(Department).count()}")
        print(f"   - Doctors: {db.query(Doctor).count()}")
        print(f"   - Patients: {db.query(Patient).count()}")
        
        print("\n🔐 Login Information:")
        print("   URL: http://localhost:8000")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n⚠️  Remember to change the default password!")
        
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()