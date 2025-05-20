from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.appointment import AppointmentStatus

class AppointmentBase(BaseModel):
    appointment_datetime: datetime
    reason: Optional[str] = None
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    doctor_id: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "doctor_id": 1,
                "appointment_datetime": "2025-05-20T11:00:00",
                "reason": "Annual checkup",
                "notes": "Patient has history of hypertension"
            }
        }

class AppointmentReschedule(BaseModel):
    appointment_datetime: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "appointment_datetime": "2025-05-22T14:00:00"
            }
        }

class AppointmentUpdate(BaseModel):
    appointment_datetime: Optional[datetime] = None
    status: Optional[AppointmentStatus] = None
    reason: Optional[str] = None
    notes: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "notes": "Updated notes about the appointment",
                "status": "confirmed"
            }
        }

class Appointment(AppointmentBase):
    id: int
    doctor_id: int
    patient_id: int
    status: AppointmentStatus
    
    class Config:
        from_attributes = True