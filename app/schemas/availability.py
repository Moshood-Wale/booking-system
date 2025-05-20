from pydantic import BaseModel, validator
from typing import Optional
from datetime import time
import re

class AvailabilityBase(BaseModel):
    day_of_week: str
    start_time: time
    end_time: time
    
    @validator('day_of_week')
    def validate_day_of_week(cls, v):
        valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        if v not in valid_days:
            raise ValueError(f"day_of_week must be one of {valid_days}")
        return v
    
    @validator('end_time')
    def validate_end_time(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v

class AvailabilityCreate(AvailabilityBase):
    class Config:
        json_schema_extra = {
            "example": {
                "day_of_week": "Tuesday",
                "start_time": "10:00:00",
                "end_time": "14:00:00"
            }
        }

class AvailabilityUpdate(BaseModel):
    day_of_week: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    is_active: Optional[bool] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "day_of_week": "Wednesday",
                "start_time": "13:00:00",
                "end_time": "17:00:00",
                "is_active": True
            }
        }

class Availability(AvailabilityBase):
    id: int
    doctor_id: int
    is_active: bool
    
    class Config:
        from_attributes = True