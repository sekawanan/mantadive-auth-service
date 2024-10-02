# app/infrastructure/google_oauth.py
import os
import requests
from app.core.config import settings

def get_google_oauth_token(code: str) -> str:
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()["access_token"]

def get_google_user_info(token: str) -> dict:
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(user_info_url, headers=headers)
    response.raise_for_status()
    return response.json()
