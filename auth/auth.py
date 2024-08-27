import os
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Annotated

from models.users import find_user_by_username
from utils.utils import AUTH_INVALID

load_dotenv()

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

class Token(BaseModel):
    access_token: str
    token_type: str
    message: str


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

@router.post("/token", response_model=Token)
def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if authenticate_user(form_data.username, form_data.password):
        user = find_user_by_username(form_data.username)
        generated_token = create_access_token(user["username"], timedelta(minutes=5))
        return {"access_token": generated_token, "token_type": "bearer", "message": "Token is valid for 5 minutes!"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AUTH_INVALID)
    
def authenticate_user(username: str, password: str) -> bool:
    user = find_user_by_username(username)
    if not user:
        return False
    if not bcrypt_context.verify(password, user["password"]):
        return False
    return True

def create_access_token(username: str, expires_delta: timedelta):
    encode = {"username": username}
    expires = datetime.now() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_from_jwt(provided_token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(provided_token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"username": payload.get("username")}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired JWT")