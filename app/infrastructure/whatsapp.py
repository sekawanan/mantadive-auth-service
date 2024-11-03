import os
import requests
from urllib.parse import urlencode
from datetime import timedelta
from fastapi import HTTPException
from app.core.config import settings
from app.core.security import create_access_token

def send_whatsapp_verification(phone_number: str, full_name: str, user_id: str, username: str) -> None:
    # Load environment variables
    host_url = os.getenv('WHATSAPP_HOST_URL', 'http://localhost:3000')
    session_id = os.getenv('WHATSAPP_SESSION_ID', 'ABCD')
    
    token = create_access_token(data={"user_id": user_id, "username": username}, expires_delta=timedelta(hours=24))
    params = urlencode({"token": token})
    verification_link = f"{settings.VERIFICATION_BASE_URL}?{params}"
    message = f"Hello {full_name}, please verify your phone number by clicking the link: {verification_link}"

    payload = {
        "chatId": f"{phone_number}@c.us",
        "contentType": "string",
        "content": message
    }

    try:
        response = requests.post(f"{host_url}/client/sendMessage/{session_id}", json=payload)
        response.raise_for_status()  # Raise an exception for HTTP error codes
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to send WhatsApp verification: {e}")

def send_whatsapp_password_reset(phone_number: str, token: str) -> None:
    # Load environment variables
    host_url = os.getenv('HOST_URL', 'http://localhost:3000')
    session_id = os.getenv('WHATSAPP_SESSION_ID', 'ABCD')

    reset_link = f"{settings.RESET_PASSWORD_BASE_URL}?token={token}"
    message = f"Hello, reset your password by clicking the link: {reset_link}"

    payload = {
        "chatId": f"{phone_number}@c.us",
        "contentType": "string",
        "content": message
    }

    try:
        response = requests.post(f"{host_url}/client/sendMessage/{session_id}", json=payload)
        response.raise_for_status()  # Raise an exception for HTTP error codes
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to send WhatsApp password reset: {e}")
