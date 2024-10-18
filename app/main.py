# app/main.py
from fastapi import FastAPI, HTTPException
from app.api.routers import auth, users
from app.infrastructure.database import engine
from app.domain.models import Base  # Ensure all models are imported
from app.api.exceptions import http_exception_handler, generic_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.schemas.base_response import BaseResponse, ErrorDetail

from fastapi.exceptions import RequestValidationError
from app.api.exceptions import validation_exception_handler

app = FastAPI(
    title="FastAPI Authentication Service",
    description="A robust authentication service built with FastAPI, JWT, and PostgreSQL.",
    version="1.0.0",
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])

# Register Exception Handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

