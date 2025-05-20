from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Enum, Text
from sqlalchemy.orm import relationship
import enum
from app.database import Base

class AppointmentStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    RESCHEDULED = "rescheduled"

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))
    appointment_datetime = Column(DateTime, nullable=False)
    status = Column(String, default=AppointmentStatus.PENDING)
    reason = Column(Text)
    notes = Column(Text)
    
    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")