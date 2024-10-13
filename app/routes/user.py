from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas import UserCreate, UserResponse
from app.models import users
from app.database import database
from sqlalchemy import select
from app.auth import get_password_hash
from app.email_utils import send_verification_email
import uuid

router = APIRouter()

# Function to generate email verification token
def generate_verification_token(email: str):
    return str(uuid.uuid4())  # Simple UUID as token

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, background_tasks: BackgroundTasks):
    # Check for duplicate email, phone number, or medical registration number
    query = select(users).where(
        (users.c.email == user.email) |
        (users.c.phone_number == user.phone_number) |
        (users.c.medical_registration_number == user.medical_registration_number)
    )
    existing_user = await database.fetch_one(query)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email, phone number, or medical registration number already registered")

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Insert the user into the database
    query = users.insert().values(
        full_name=user.full_name,
        date_of_birth=user.date_of_birth,
        gender=user.gender,
        email=user.email,
        phone_number=user.phone_number,
        mailing_address=user.mailing_address,
        medical_registration_number=user.medical_registration_number,
        specialty=user.specialty,
        reason_for_participation=user.reason_for_participation,
        agreement_to_terms=user.agreement_to_terms,
        consent_for_data_use=user.consent_for_data_use,
        privacy_agreement=user.privacy_agreement,
        verified=False,  # Initially set to false
        password=hashed_password  # Store the hashed password
    )
    user_id = await database.execute(query)

    # Generate email verification token and send it
    verification_token = generate_verification_token(user.email)
    background_tasks.add_task(send_verification_email, user.email, verification_token)

    return UserResponse(
        id=user_id,
        full_name=user.full_name,
        email=user.email,
        phone_number=user.phone_number,  # Make sure this is included
        medical_registration_number=user.medical_registration_number,  # Make sure this is included
        verified=False
    )
