from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.doctor import Doctor
from app.models.availability import Availability
from app.schemas.availability import (
    Availability as AvailabilitySchema,
    AvailabilityCreate,
    AvailabilityUpdate
)
from app.api.dependencies import get_current_doctor

router = APIRouter()

@router.post("/", response_model=AvailabilitySchema, status_code=status.HTTP_201_CREATED)
def create_availability(
    availability_in: AvailabilityCreate,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    # Create new availability
    db_availability = Availability(
        doctor_id=current_doctor.id,
        day_of_week=availability_in.day_of_week,
        start_time=availability_in.start_time,
        end_time=availability_in.end_time,
        is_active=True
    )
    db.add(db_availability)
    db.commit()
    db.refresh(db_availability)
    return db_availability

@router.get("/", response_model=List[AvailabilitySchema])
def read_availabilities(
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    availabilities = db.query(Availability).filter(
        Availability.doctor_id == current_doctor.id
    ).all()
    return availabilities

@router.get("/{availability_id}", response_model=AvailabilitySchema)
def read_availability(
    availability_id: int,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    db_availability = db.query(Availability).filter(
        Availability.id == availability_id,
        Availability.doctor_id == current_doctor.id
    ).first()
    if not db_availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Availability not found"
        )
    return db_availability

@router.put("/{availability_id}", response_model=AvailabilitySchema)
def update_availability(
    availability_id: int,
    availability_in: AvailabilityUpdate,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    db_availability = db.query(Availability).filter(
        Availability.id == availability_id,
        Availability.doctor_id == current_doctor.id
    ).first()
    if not db_availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Availability not found"
        )
    
    # Update availability fields
    update_data = availability_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_availability, key, value)
    
    db.add(db_availability)
    db.commit()
    db.refresh(db_availability)
    return db_availability

@router.delete("/{availability_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_availability(
    availability_id: int,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    db_availability = db.query(Availability).filter(
        Availability.id == availability_id,
        Availability.doctor_id == current_doctor.id
    ).first()
    if not db_availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Availability not found"
        )
    db.delete(db_availability)
    db.commit()
    return None

@router.get("/doctor/{doctor_id}", response_model=List[AvailabilitySchema])
def read_doctor_availabilities(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    # Check if doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    availabilities = db.query(Availability).filter(
        Availability.doctor_id == doctor_id,
        Availability.is_active == True
    ).all()
    return availabilities