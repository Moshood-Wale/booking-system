from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class WorkExperience(Base):
    __tablename__ = "work_experience"
    
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    hospital_name = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    description = Column(Text)
    
    doctor = relationship("Doctor", back_populates="work_experiences")

class AcademicHistory(Base):
    __tablename__ = "academic_history"
    
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    institution = Column(String(100), nullable=False)
    degree = Column(String(100), nullable=False)
    field_of_study = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    
    doctor = relationship("Doctor", back_populates="academic_histories")

class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    full_name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)
    phone_number = Column(String(20))
    is_active = Column(Boolean, default=True)
    
    work_experiences = relationship("WorkExperience", back_populates="doctor", cascade="all, delete-orphan")
    academic_histories = relationship("AcademicHistory", back_populates="doctor", cascade="all, delete-orphan")
    availabilities = relationship("Availability", back_populates="doctor", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="doctor", cascade="all, delete-orphan")