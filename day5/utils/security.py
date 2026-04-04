# security.py
import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from config import SECRET_KEY, ALGORITHM, EXPIRY_MINUTES
from fastapi import Depends
from sqlalchemy.orm import Session
from dependencies.database import get_db
from fastapi.security import OAuth2PasswordBearer
from exceptions.exceptions import InvalidCredentialsException
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRY_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise InvalidCredentialsException()
    except JWTError:
        raise InvalidCredentialsException()
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise InvalidCredentialsException()
    return user