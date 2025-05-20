from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.doctor import Doctor, WorkExperience, AcademicHistory
from app.schemas.doctor import (
    Doctor as DoctorSchema,
    DoctorCreate,
    DoctorUpdate,
    WorkExperienceCreate,
    AcademicHistoryCreate
)
from app.core.security import get_password_hash
from app.api.dependencies import get_current_doctor

router = APIRouter()

@router.post("/", response_model=DoctorSchema, status_code=status.HTTP_201_CREATED)
def create_doctor(
    doctor_in: DoctorCreate,
    db: Session = Depends(get_db)
):
    # Check if email already exists
    db_doctor = db.query(Doctor).filter(Doctor.email == doctor_in.email).first()
    if db_doctor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new doctor
    db_doctor = Doctor(
        email=doctor_in.email,
        hashed_password=get_password_hash(doctor_in.password),
        full_name=doctor_in.full_name,
        specialization=doctor_in.specialization,
        phone_number=doctor_in.phone_number
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    
    # Add work experiences
    if doctor_in.work_experiences:
        for exp in doctor_in.work_experiences:
            db_exp = WorkExperience(
                doctor_id=db_doctor.id,
                hospital_name=exp.hospital_name,
                position=exp.position,
                start_date=exp.start_date,
                end_date=exp.end_date,
                description=exp.description
            )
            db.add(db_exp)
    
    # Add academic histories
    if doctor_in.academic_histories:
        for history in doctor_in.academic_histories:
            db_history = AcademicHistory(
                doctor_id=db_doctor.id,
                institution=history.institution,
                degree=history.degree,
                field_of_study=history.field_of_study,
                start_date=history.start_date,
                end_date=history.end_date
            )
            db.add(db_history)
    
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@router.get("/me", response_model=DoctorSchema)
def read_doctor_me(
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    return current_doctor

@router.put("/me", response_model=DoctorSchema)
def update_doctor_me(
    doctor_in: DoctorUpdate,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    if doctor_in.email and doctor_in.email != current_doctor.email:
        # Check if new email already exists
        db_doctor = db.query(Doctor).filter(Doctor.email == doctor_in.email).first()
        if db_doctor:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Update doctor fields
    update_data = doctor_in.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for key, value in update_data.items():
        setattr(current_doctor, key, value)
    
    db.add(current_doctor)
    db.commit()
    db.refresh(current_doctor)
    return current_doctor

@router.post("/me/work-experience", status_code=status.HTTP_201_CREATED)
def add_work_experience(
    experience_in: WorkExperienceCreate,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    db_exp = WorkExperience(
        doctor_id=current_doctor.id,
        hospital_name=experience_in.hospital_name,
        position=experience_in.position,
        start_date=experience_in.start_date,
        end_date=experience_in.end_date,
        description=experience_in.description
    )
    db.add(db_exp)
    db.commit()
    db.refresh(db_exp)
    return {"success": True, "id": db_exp.id}

@router.post("/me/academic-history", status_code=status.HTTP_201_CREATED)
def add_academic_history(
    history_in: AcademicHistoryCreate,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    db_history = AcademicHistory(
        doctor_id=current_doctor.id,
        institution=history_in.institution,
        degree=history_in.degree,
        field_of_study=history_in.field_of_study,
        start_date=history_in.start_date,
        end_date=history_in.end_date
    )
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return {"success": True, "id": db_history.id}

@router.get("/{doctor_id}", response_model=DoctorSchema)
def read_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    return db_doctor

@router.get("/", response_model=List[DoctorSchema])
def read_doctors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    doctors = db.query(Doctor).offset(skip).limit(limit).all()
    return doctors