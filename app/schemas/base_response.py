# app/schemas/base_response.py
from typing import Generic, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from datetime import datetime

T = TypeVar('T')

class ErrorDetail(BaseModel):
    code: int
    message: str

class BaseResponse(Generic[T], BaseModel):
    payload: Optional[T] = None
    errors: Optional[Union[ErrorDetail, list[ErrorDetail]]] = None
    timeStamp: datetime
    success: bool

    @classmethod
    def success_response(cls, payload: T) -> 'BaseResponse[T]':
        return cls(
            payload=payload,
            errors=None,
            timeStamp=datetime.utcnow(),
            success=True
        )

    @classmethod
    def error_response(cls, errors: Union[ErrorDetail, list[ErrorDetail]]) -> 'BaseResponse[None]':
        return cls(
            payload=None,
            errors=errors,
            timeStamp=datetime.utcnow(),
            success=False
        )
