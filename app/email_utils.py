import os  # <-- Make sure this line is present
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables from .env file
load_dotenv()

# Function to send a verification email
def send_verification_email(to_email: str, token: str):
    # Load SMTP credentials from environment variables
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    verification_link = f"http://127.0.0.1:8000/verify?token={token}&email={to_email}"

    # Create email content
    message = MIMEMultipart()
    message["From"] = smtp_user
    message["To"] = to_email
    message["Subject"] = "Verify your email address"
    body = f"Please click the following link to verify your email address: {verification_link}"
    message.attach(MIMEText(body, "plain"))

    # Send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Start TLS encryption
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, message.as_string())
        server.quit()
        print(f"Verification email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send verification email: {str(e)}")
