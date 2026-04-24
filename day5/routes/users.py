from fastapi import APIRouter, Depends, HTTPException
from dependencies.database import get_db
from fastapi.params import Body
from models.schemas import UserCreate, UserLogin, ItemCreate, UserResponse, Token
from models.user import User
from models.items import Item
from models.refresh_token import RefreshToken
from exceptions.exceptions import (UserAlreadyExistsException, ItemAlreadyExistsException,
                                   InvalidUserException, InvalidCredentialsException, UserNotFoundException)
from utils.security import hash_password, verify_password, create_access_token, get_current_user, require_role
import secrets
from datetime import datetime, timezone, timedelta

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise UserAlreadyExistsException(user.email)
    hashed_password = hash_password(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login_user(user: UserLogin, db = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user:
        raise InvalidCredentialsException()
    is_valid = verify_password(user.password, existing_user.hashed_password)
    if not is_valid:
        raise InvalidCredentialsException()
    access_token = create_access_token(data={"sub": str(existing_user.id)})
    token_id = secrets.token_urlsafe(8)
    secret = secrets.token_urlsafe(32)
    refresh_token = f"{token_id}.{secret}"
    hashed_refresh_token = hash_password(secret)
    expires = datetime.now(timezone.utc) + timedelta(days=7)
    db_refresh_token = RefreshToken(
        id=token_id,
        user_id=existing_user.id,
        hashed_token=hashed_refresh_token,
        expires_at=expires
    )
    db.add(db_refresh_token)
    db.commit()
    db.refresh(db_refresh_token)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
def refresh_access_token(refresh_token: str = Body(..., embed=True), db=Depends(get_db)):
    try:
        token_id, secret = refresh_token.split(".")
    except ValueError:
        raise InvalidCredentialsException()

    db_token = db.query(RefreshToken).filter(RefreshToken.id == token_id).first()
    if not db_token:
        raise InvalidCredentialsException()

    if not verify_password(secret, db_token.hashed_token):
        raise InvalidCredentialsException()

    if db_token.expires_at < datetime.now(timezone.utc):
        db.delete(db_token)
        db.commit()
        raise InvalidCredentialsException()

    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user:
        raise InvalidCredentialsException()

    # rotate
    db.delete(db_token)
    db.commit()

    new_access_token = create_access_token(data={"sub": str(user.id)})

    new_token_id = secrets.token_urlsafe(8)
    new_secret = secrets.token_urlsafe(32)
    new_refresh_token = f"{new_token_id}.{new_secret}"

    new_hashed_token = hash_password(new_secret)
    new_expires = datetime.now(timezone.utc) + timedelta(days=7)

    new_db_token = RefreshToken(
        id=new_token_id,
        user_id=user.id,
        hashed_token=new_hashed_token,
        expires_at=new_expires
    )

    db.add(new_db_token)
    db.commit()

    return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}

@router.post("/logout")
def logout(refresh_token: str = Body(..., embed=True), db=Depends(get_db)):
    try:
        token_id, secret = refresh_token.split(".")
    except ValueError:
        raise InvalidCredentialsException()

    db_token = db.query(RefreshToken).filter(RefreshToken.id == token_id).first()
    if not db_token:
        raise InvalidCredentialsException()

    if not verify_password(secret, db_token.hashed_token):
        raise InvalidCredentialsException()

    db.delete(db_token)
    db.commit()

    return {"message": "Logged out successfully"}

@router.get("/{user_id}/items")
def get_user_items(user_id: int, db = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException(user_id)
    return user.items

@router.post("/{user_id}/items")
def create_item_for_user(user_id: int, item: ItemCreate, db = Depends(get_db)):
    user = db.query(User.id).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException(user_id)
    existing_item = db.query(Item).filter(Item.name == item.name, Item.user_id == user_id).first()
    if existing_item:
        raise ItemAlreadyExistsException(item.name)
    db_item = Item(
        name=item.name,
        price=item.price,
        user_id=user_id,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{user_id}")
def delete_user(user_id: int, db = Depends(get_db), current_admin: User = Depends(require_role("admin"))):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException(user_id)
    db.delete(user)
    db.commit()
    return {"message": "user deleted"}