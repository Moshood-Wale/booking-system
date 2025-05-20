from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.database import get_db
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment, AppointmentStatus
from app.models.availability import Availability
from app.schemas.appointment import (
    Appointment as AppointmentSchema,
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentReschedule
)
from app.api.dependencies import get_current_doctor, get_current_patient

router = APIRouter()

def check_availability(
    db: Session,
    doctor_id: int,
    appointment_datetime: datetime
):
    # Check if the doctor has availability for this day and time
    weekday = appointment_datetime.strftime("%A")  # Monday, Tuesday, etc.
    time = appointment_datetime.time()
    
    availability = db.query(Availability).filter(
        Availability.doctor_id == doctor_id,
        Availability.day_of_week == weekday,
        Availability.start_time <= time,
        Availability.end_time >= time,
        Availability.is_active == True
    ).first()
    
    if not availability:
        return False
    
    # Check if there's already an appointment at this time
    existing_appointment = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.appointment_datetime >= appointment_datetime,
        Appointment.appointment_datetime < appointment_datetime + timedelta(minutes=30),
        Appointment.status.in_([AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED])
    ).first()
    
    if existing_appointment:
        return False
    
    return True

@router.post("/", response_model=AppointmentSchema, status_code=status.HTTP_201_CREATED)
def create_appointment(
    appointment_in: AppointmentCreate,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    # Check if doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == appointment_in.doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    # Check doctor's availability
    if not check_availability(db, appointment_in.doctor_id, appointment_in.appointment_datetime):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Doctor is not available at this time"
        )
    
    # Create new appointment
    db_appointment = Appointment(
        doctor_id=appointment_in.doctor_id,
        patient_id=current_patient.id,
        appointment_datetime=appointment_in.appointment_datetime,
        reason=appointment_in.reason,
        notes=appointment_in.notes,
        status=AppointmentStatus.PENDING
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@router.get("/doctor", response_model=List[AppointmentSchema])
def read_doctor_appointments(
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    appointments = db.query(Appointment).filter(
        Appointment.doctor_id == current_doctor.id
    ).all()
    return appointments

@router.get("/patient", response_model=List[AppointmentSchema])
def read_patient_appointments(
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    appointments = db.query(Appointment).filter(
        Appointment.patient_id == current_patient.id
    ).all()
    return appointments

@router.put("/{appointment_id}/cancel", response_model=AppointmentSchema)
def cancel_appointment(
    appointment_id: int,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    db_appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id,
        Appointment.doctor_id == current_doctor.id
    ).first()
    if not db_appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    if db_appointment.status == AppointmentStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment is already cancelled"
        )
    
    db_appointment.status = AppointmentStatus.CANCELLED
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@router.put("/{appointment_id}/reschedule", response_model=AppointmentSchema)
def reschedule_appointment(
    appointment_id: int,
    reschedule_in: AppointmentReschedule,
    current_patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    db_appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id,
        Appointment.patient_id == current_patient.id
    ).first()
    if not db_appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    if db_appointment.status == AppointmentStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot reschedule a cancelled appointment"
        )
    
    if db_appointment.status == AppointmentStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot reschedule a completed appointment"
        )
    
    # Check doctor's availability for the new time
    if not check_availability(db, db_appointment.doctor_id, reschedule_in.appointment_datetime):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Doctor is not available at this time"
        )
    
    db_appointment.appointment_datetime = reschedule_in.appointment_datetime
    db_appointment.status = AppointmentStatus.RESCHEDULED
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment