from fastapi import APIRouter, Depends
from dependencies.database import get_db
from models.schemas import UserCreate, ItemCreate
from models.user import User
from models.items import Item
from exceptions.exceptions import UserAlreadyExistsException, ItemAlreadyExistsException, UserNotFoundException


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/")
def create_user(user: UserCreate, db = Depends(get_db)):
    existing_user = db.query(User).filter(User.name == user.name).first()
    if existing_user:
        raise UserAlreadyExistsException(user.name)
    db_user = User(
        name=user.name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

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