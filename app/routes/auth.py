from fastapi import APIRouter, HTTPException, Depends, Request  # Make sure Request is imported
from app.database import database
from sqlalchemy import select, update
from app.models import users
from app.email_utils import send_verification_email
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.limiter import limiter  # Import limiter
import random
import os
from datetime import datetime, timedelta
from pydantic import BaseModel

# Create an instance of APIRouter
router = APIRouter()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT secret key and algorithm
SECRET_KEY = os.getenv("SECRET_KEY", "myjwtsecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Helper function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Helper function to hash password
def get_password_hash(password):
    return pwd_context.hash(password)

# Generate JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Generate a random OTP
def generate_otp():
    return f"{random.randint(100000, 999999)}"  # 6 digit OTP

# Define Pydantic models for request validation
class LoginPasswordRequest(BaseModel):
    email: str
    password: str

class LoginOTPRequest(BaseModel):
    email: str
    otp: str

class OTPRequest(BaseModel):
    email: str

# OTP login request - sends OTP to user's email
@router.post("/login-otp-request")
async def request_otp(request: OTPRequest):
    query = select(users).where(users.c.email == request.email)
    user = await database.fetch_one(query)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the user's account is verified
    if not user.verified:
        raise HTTPException(status_code=403, detail="Account not verified")

    # Generate and save the OTP in the database
    otp = generate_otp()
    update_query = update(users).where(users.c.email == request.email).values(otp=otp)
    await database.execute(update_query)

    # Send OTP via email
    send_verification_email(request.email, otp)

    return {"message": f"OTP sent to {request.email}"}

# OTP verification login
@router.post("/login-otp")
async def login_with_otp(request: LoginOTPRequest):
    query = select(users).where(users.c.email == request.email)
    user = await database.fetch_one(query)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the user's account is verified
    if not user.verified:
        raise HTTPException(status_code=403, detail="Account not verified")

    if user.otp != request.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # OTP is correct, generate JWT token
    access_token = create_access_token(data={"sub": user.email})

    # Clear OTP after successful login
    update_query = update(users).where(users.c.email == request.email).values(otp=None)
    await database.execute(update_query)

    return {"access_token": access_token, "token_type": "bearer"}

# Password-based login
@router.post("/login-password")
@limiter.limit("5/minute")  # Rate limit applied here
async def login_with_password(request: Request, login_request: LoginPasswordRequest):  # Add `Request` type
    query = select(users).where(users.c.email == login_request.email)
    user = await database.fetch_one(query)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the user's account is verified
    if not user.verified:
        raise HTTPException(status_code=403, detail="Account not verified")

    if not verify_password(login_request.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Password is correct, generate JWT token
    access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}
