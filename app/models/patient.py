from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    full_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date)
    phone_number = Column(String(20))
    address = Column(String(200))
    is_active = Column(Boolean, default=True)
    
    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")