# for user authentication
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from jwt import PyJWTError
# from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from schemas import LoginRequest, TokenData
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import database


from models import User


load_dotenv()

# Secret key
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
oath2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# hash the password using bcrypt 
def hash_password(password:str):
    hashed_password = pwd_context.hash(password)
    return hashed_password


# check between plain password and hashed password (plain_password:str, hashed_password:str) return-> pwd_context
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db:Session, username:str):
    return db.query(User).filter(User.username == username).first()

def create_access_token(data:dict, expires_delta:timedelta|None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) 
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt



# authenticate user
def authenticate_user(db:Session, username:str, password:str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return LoginRequest(username=user.username, password=password)

# to be used as a dependency for every end point after logging in (This function authenticates user) returns the current logged user
def get_current_user(token: Annotated[str, Depends(oath2_scheme)], db: Session = Depends(database.get_db) ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception

    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
   