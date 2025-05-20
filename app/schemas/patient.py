from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

class PatientBase(BaseModel):
    email: EmailStr
    full_name: str
    date_of_birth: Optional[date] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class PatientCreate(PatientBase):
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "patient@example.com",
                "full_name": "John Doe",
                "date_of_birth": "1985-05-15",
                "phone_number": "0987654321",
                "address": "123 Main St, City",
                "password": "securepassword"
            }
        }

class PatientUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    password: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "John Smith",
                "phone_number": "0987654321",
                "address": "456 New St, City"
            }
        }

class Patient(PatientBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True