from app.schemas.doctor import (
    Doctor, DoctorCreate, DoctorUpdate,
    WorkExperienceCreate, WorkExperienceInDB,
    AcademicHistoryCreate, AcademicHistoryInDB
)
from app.schemas.patient import Patient, PatientCreate, PatientUpdate
from app.schemas.availability import Availability, AvailabilityCreate, AvailabilityUpdate
from app.schemas.appointment import Appointment, AppointmentCreate, AppointmentUpdate, AppointmentReschedule