from typing import Generic, TypeVar, Union, List
from app.schemas.base_response import BaseResponse, ErrorDetail
from pydantic import BaseModel

T = TypeVar('T')

def create_success_response(payload: T) -> BaseResponse[T]:
    return BaseResponse.success_response(payload)

def create_error_response(code: int, message: str) -> BaseResponse[None]:
    error = ErrorDetail(code=code, message=message)
    return BaseResponse.error_response(error)

def create_validation_error_response(errors: List[dict]) -> BaseResponse[None]:
    error_details = [ErrorDetail(code=422, message=err['msg']) for err in errors]
    return BaseResponse.error_response(error_details)