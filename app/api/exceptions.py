from datetime import datetime
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.base_response import BaseResponse, ErrorDetail
from fastapi.exceptions import RequestValidationError

async def http_exception_handler(request: Request, exc: HTTPException):
    error = ErrorDetail(code=exc.status_code, message=exc.detail)
    response = BaseResponse.error_response(error)
    return JSONResponse(status_code=exc.status_code, content=response.dict())

async def generic_exception_handler(request: Request, exc: Exception):
    error = ErrorDetail(code=500, message="Internal Server Error")
    response = BaseResponse.error_response(error)
    return JSONResponse(status_code=500, content=response.dict())

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [ErrorDetail(code=422, message=err['msg']) for err in exc.errors()]
    response = BaseResponse.error_response(errors)
    return JSONResponse(status_code=422, content=response.dict())

