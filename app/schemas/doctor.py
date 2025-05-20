from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import date

class WorkExperienceBase(BaseModel):
    hospital_name: str
    position: str
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None

class WorkExperienceCreate(WorkExperienceBase):
    class Config:
        json_schema_extra = {
            "example": {
                "hospital_name": "City Hospital",
                "position": "Senior Cardiologist",
                "start_date": "2018-01-01",
                "end_date": "2022-12-31",
                "description": "Specialized in cardiac surgery"
            }
        }

class WorkExperienceInDB(WorkExperienceBase):
    id: int
    doctor_id: int
    
    class Config:
        from_attributes = True

class AcademicHistoryBase(BaseModel):
    institution: str
    degree: str
    field_of_study: str
    start_date: date
    end_date: Optional[date] = None

class AcademicHistoryCreate(AcademicHistoryBase):
    class Config:
        json_schema_extra = {
            "example": {
                "institution": "Medical University",
                "degree": "MD",
                "field_of_study": "Medicine",
                "start_date": "2010-09-01",
                "end_date": "2016-06-30"
            }
        }

class AcademicHistoryInDB(AcademicHistoryBase):
    id: int
    doctor_id: int
    
    class Config:
        from_attributes = True

class DoctorBase(BaseModel):
    email: EmailStr
    full_name: str
    specialization: str
    phone_number: Optional[str] = None

class DoctorCreate(DoctorBase):
    password: str
    work_experiences: Optional[List[WorkExperienceCreate]] = []
    academic_histories: Optional[List[AcademicHistoryCreate]] = []
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "doctor@example.com",
                "full_name": "Dr. Jane Smith",
                "specialization": "Cardiologist",
                "phone_number": "1234567890",
                "password": "securepassword",
                "work_experiences": [
                    {
                        "hospital_name": "City Hospital",
                        "position": "Senior Cardiologist",
                        "start_date": "2018-01-01",
                        "end_date": "2022-12-31",
                        "description": "Specialized in cardiac surgery"
                    }
                ],
                "academic_histories": [
                    {
                        "institution": "Medical University",
                        "degree": "MD",
                        "field_of_study": "Medicine",
                        "start_date": "2010-09-01",
                        "end_date": "2016-06-30"
                    }
                ]
            }
        }

class DoctorUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    specialization: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None

class Doctor(DoctorBase):
    id: int
    is_active: bool
    work_experiences: List[WorkExperienceInDB] = []
    academic_histories: List[AcademicHistoryInDB] = []
    
    class Config:
        from_attributes = True