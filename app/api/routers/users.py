# app/api/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserOut
from app.domain.repositories.user_repository import IUserRepository
from app.api.dependencies import get_user_repository
from app.core.security import decode_access_token
from fastapi.security import OAuth2PasswordBearer
from app.domain.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter()

def get_current_user(token: str = Depends(oauth2_scheme), repo: IUserRepository = Depends(get_user_repository)) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload.get("sub")
    user = repo.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    return UserOut.from_orm(current_user)
