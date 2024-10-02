from fastapi import FastAPI
from app.api.routers import auth, users
from app.infrastructure.database import engine
from app.domain.models.user import Base

# Create all tables (ensure migrations are applied instead for production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Authentication Service",
    description="A robust authentication service built with FastAPI, JWT, and PostgreSQL.",
    version="1.0.0",
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
