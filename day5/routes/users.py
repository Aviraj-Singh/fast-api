from fastapi import APIRouter, Depends
from dependencies.database import get_db
from models.schemas import UserCreate, UserLogin, ItemCreate, UserResponse, Token
from models.user import User
from models.items import Item
from exceptions.exceptions import UserAlreadyExistsException, ItemAlreadyExistsException, InvalidUserException
from utils.security import hash_password, verify_password, create_access_token, get_current_user

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
        raise InvalidUserException()
    is_valid = verify_password(user.password, existing_user.hashed_password)
    if not is_valid:
        raise InvalidUserException()
    access_token = create_access_token(data={"sub": str(existing_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

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
def delete_user(user_id: int, db = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException(user_id)
    db.delete(user)
    db.commit()
    return {"message": "user deleted"}