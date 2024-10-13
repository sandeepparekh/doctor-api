from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.email_utils import send_verification_email
import uuid

router = APIRouter()

# Generate a simple test token
def generate_test_token():
    return str(uuid.uuid4())

# Define the request schema
class EmailRequest(BaseModel):
    email: str

@router.post("/send-test-email")
async def send_test_email(request: EmailRequest):
    # Extract email from the request body
    email = request.email

    # Generate a fake token for the test
    token = generate_test_token()

    try:
        # Send the email using the existing send_verification_email function
        send_verification_email(email, token)
        return {"message": f"Test email sent to {email}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
