# app/infrastructure/smtp.py
import smtplib
from email.mime.text import MIMEText
from urllib.parse import urlencode
from app.core.config import settings
from app.core.security import create_access_token
from datetime import timedelta

def send_verification_email(email: str, username: str) -> None:
    token = create_access_token(data={"sub": username}, expires_delta=timedelta(hours=24))
    params = urlencode({"token": token})
    verification_link = f"{settings.VERIFICATION_BASE_URL}?{params}"
    subject = "Verify Your Email"
    body = f"Hello {username},\n\nPlease verify your email by clicking the link below:\n{verification_link}\n\nThank you!"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_USERNAME
    msg["To"] = email

    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()
        print(settings.SMTP_PASSWORD)
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_USERNAME, email, msg.as_string())

def send_password_reset_email(email: str, token: str) -> None:
    params = urlencode({"token": token})
    reset_link = f"{settings.RESET_PASSWORD_BASE_URL}?{params}"
    subject = "Reset Your Password"
    body = f"Hello,\n\nPlease reset your password by clicking the link below:\n{reset_link}\n\nThank you!"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_USERNAME
    msg["To"] = email

    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_USERNAME, email, msg.as_string())
