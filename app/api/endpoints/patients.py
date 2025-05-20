from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.patient import Patient
from app.schemas.patient import Patient as PatientSchema, PatientCreate, PatientUpdate
from app.core.security import get_password_hash
from app.api.dependencies import get_current_patient

router = APIRouter()

@router.post("/", response_model=PatientSchema, status_code=status.HTTP_201_CREATED)
def create_patient(
    patient_in: PatientCreate,
    db: Session = Depends(get_db)
):
    # Check if email already exists
    db_patient = db.query(Patient).filter(Patient.email == patient_in.email).first()
    if db_patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new patient
    db_patient = Patient(
        email=patient_in.email,
        hashed_password=get_password_hash(patient_in.password),
        full_name=patient_in.full_name,
        date_of_birth=patient_in.date_of_birth,
        phone_number=patient_in.phone_number,
        address=patient_in.address
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.get("/me", response_model=PatientSchema)
def read_patient_me(
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    return current_patient

@router.put("/me", response_model=PatientSchema)
def update_patient_me(
    patient_in: PatientUpdate,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    if patient_in.email and patient_in.email != current_patient.email:
        # Check if new email already exists
        db_patient = db.query(Patient).filter(Patient.email == patient_in.email).first()
        if db_patient:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Update patient fields
    update_data = patient_in.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for key, value in update_data.items():
        setattr(current_patient, key, value)
    
    db.add(current_patient)
    db.commit()
    db.refresh(current_patient)
    return current_patient

@router.get("/{patient_id}", response_model=PatientSchema)
def read_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    return db_patient