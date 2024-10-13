from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.models import users
from app.database import database

router = APIRouter()

@router.get("/verify")
async def verify_email(token: str, email: str):
    # Check if the user with the given email exists
    query = select(users).where(users.c.email == email)
    user = await database.fetch_one(query)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Assuming you validate the token (you can customize this as needed)
    # For this example, we assume the token is valid if it matches some simple criteria.
    if not token:
        raise HTTPException(status_code=400, detail="Invalid token")

    # Update the user's verified status
    query = users.update().where(users.c.email == email).values(verified=True)
    await database.execute(query)

    return {"message": "Email verified successfully"}
