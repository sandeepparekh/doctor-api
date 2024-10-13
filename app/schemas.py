from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import date

class UserCreate(BaseModel):
    full_name: str
    date_of_birth: date
    gender: constr(pattern='^(Male|Female|Other)$')  # Restrict to Male, Female, Other
    email: EmailStr
    phone_number: constr(pattern=r'^\+?\d{10,15}$')  # Simple phone number validation
    mailing_address: str
    medical_registration_number: str
    specialty: str
    reason_for_participation: str
    agreement_to_terms: bool
    consent_for_data_use: bool
    privacy_agreement: bool
    password: str

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone_number: str
    medical_registration_number: str
    verified: bool

    class Config:
        from_attributes = True
