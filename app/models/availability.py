from sqlalchemy import Column, Integer, ForeignKey, String, Time, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Availability(Base):
    __tablename__ = "availabilities"
    
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    day_of_week = Column(String(10), nullable=False)  # Monday, Tuesday, etc.
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_active = Column(Boolean, default=True)
    
    doctor = relationship("Doctor", back_populates="availabilities")