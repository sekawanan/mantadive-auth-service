from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database connection string
    DATABASE_URL: str

    # Individual database settings (if needed)
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # SMTP Settings
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    VERIFICATION_BASE_URL: str
    RESET_PASSWORD_BASE_URL: str

    # Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    # WhatsApp Service
    WHATSAPP_HOST_URL: str
    WHATSAPP_SESSION_ID: str

    # Security
    SECRET_KEY: str = "YOUR_SECRET_KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"

settings = Settings()
