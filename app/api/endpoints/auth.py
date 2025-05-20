from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.core.security import create_access_token, verify_password
from app.config import settings

router = APIRouter()

@router.post("/login")
def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    # Try to authenticate as doctor
    doctor = db.query(Doctor).filter(Doctor.email == form_data.username).first()
    if doctor and verify_password(form_data.password, doctor.hashed_password):
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return {
            "access_token": create_access_token(
                f"D{doctor.id}", expires_delta=access_token_expires
            ),
            "token_type": "bearer",
            "user_type": "doctor",
            "user_id": doctor.id
        }
    
    # Try to authenticate as patient
    patient = db.query(Patient).filter(Patient.email == form_data.username).first()
    if patient and verify_password(form_data.password, patient.hashed_password):
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return {
            "access_token": create_access_token(
                f"P{patient.id}", expires_delta=access_token_expires
            ),
            "token_type": "bearer",
            "user_type": "patient",
            "user_id": patient.id
        }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )