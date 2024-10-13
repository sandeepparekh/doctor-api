from fastapi import BackgroundTasks
import smtplib  # For sending emails (you can replace with SendGrid, etc.)

def send_verification_email(email: str, token: str):
    # Create verification link
    verification_link = f"http://127.0.0.1:8000/verify?token={token}&email={email}"

    # Send email (simplified)
    with smtplib.SMTP('smtp.mailtrap.io', 587) as smtp:
        smtp.login('your_username', 'your_password')  # Use proper email credentials
        message = f"Subject: Verify Your Email\n\nClick the link to verify: {verification_link}"
        smtp.sendmail('noreply@example.com', email, message)
