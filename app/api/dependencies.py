from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from typing import Optional, Union

from app.core.security import create_access_token
from app.database import get_db
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> Union[Doctor, Patient]:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if it's a doctor (first character: D) or patient (first character: P)
        if user_id.startswith("D"):
            doctor_id = int(user_id[1:])
            user = db.query(Doctor).filter(Doctor.id == doctor_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="Doctor not found")
            return user
        elif user_id.startswith("P"):
            patient_id = int(user_id[1:])
            user = db.query(Patient).filter(Patient.id == patient_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="Patient not found")
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user type",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_doctor(current_user: Union[Doctor, Patient] = Depends(get_current_user)) -> Doctor:
    if not isinstance(current_user, Doctor):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Doctor access required",
        )
    return current_user

def get_current_patient(current_user: Union[Doctor, Patient] = Depends(get_current_user)) -> Patient:
    if not isinstance(current_user, Patient):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patient access required",
        )
    return current_user