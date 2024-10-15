from fastapi import FastAPI, Request
from sqlalchemy import create_engine
from app.routes import user, auth, email_test, verify
from app.database import database, metadata
from dotenv import load_dotenv
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from app.limiter import limiter  # Import the limiter from limiter.py
import os

# Load environment variables from .env file
load_dotenv()

# Get the DATABASE_URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create a sync engine using pymysql for schema creation
sync_engine = create_engine(DATABASE_URL.replace('aiomysql', 'pymysql'))

# Initialize FastAPI app
app = FastAPI()

# Add the rate limiting middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda request, exc: JSONResponse(status_code=429, content={"message": "Too Many Requests"}))
app.add_middleware(SlowAPIMiddleware)

# Include all routers
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(email_test.router)
app.include_router(verify.router)

# Connect to the database when the app starts
@app.on_event("startup")
async def startup():
    metadata.create_all(sync_engine)  # Creates tables if they don't exist
    await database.connect()

# Disconnect from the database when the app stops
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the registration and login API"}
