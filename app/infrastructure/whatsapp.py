# app/infrastructure/whatsapp.py
from twilio.rest import Client
from urllib.parse import urlencode
from app.core.config import settings
from app.core.security import create_access_token
from datetime import timedelta

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def send_whatsapp_verification(phone_number: str, username: str) -> None:
    token = create_access_token(data={"sub": username}, expires_delta=timedelta(hours=24))
    params = urlencode({"token": token})
    verification_link = f"{settings.VERIFICATION_BASE_URL}?{params}"
    message = f"Hello {username}, please verify your phone number by clicking the link: {verification_link}"

    client.messages.create(
        body=message,
        from_=settings.WHATSAPP_FROM,
        to=f"whatsapp:{phone_number}"
    )

def send_whatsapp_password_reset(phone_number: str, token: str) -> None:
    reset_link = f"{settings.RESET_PASSWORD_BASE_URL}?token={token}"
    message = f"Hello, reset your password by clicking the link: {reset_link}"

    client.messages.create(
        body=message,
        from_=settings.WHATSAPP_FROM,
        to=f"whatsapp:{phone_number}"
    )
