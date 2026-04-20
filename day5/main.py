from fastapi import FastAPI
from models.base import Base
from dependencies.database import engine
from models.user import User
from models.items import Item
from models.refresh_token import RefreshToken
from routes import users
from exceptions.exceptions import (ItemNotFoundException, ItemAlreadyExistsException,
                                   UserAlreadyExistsException, InvalidUserException, InvalidCredentialsException)
from fastapi.responses import JSONResponse
app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(users.router)

@app.exception_handler(InvalidUserException)
def invalid_credentials_handler(request, exc: InvalidUserException):
    return JSONResponse(
        status_code=401,
        content={
            "error": "Invalid Credentials",
        }
    )

@app.exception_handler(InvalidCredentialsException)
def item_already_exists_handler(request, exc: InvalidCredentialsException):
    return JSONResponse(
        status_code=401,
        content={
            "error": "Unauthorized Access",
        }
    )

@app.exception_handler(UserAlreadyExistsException)
def user_already_exists_handler(request, exc: UserAlreadyExistsException):
    return JSONResponse(
        status_code=409,
        content={
            "error": "User already exists",
            "user_name": exc.user_name
        }
    )

@app.exception_handler(ItemAlreadyExistsException)
def item_already_exists_handler(request, exc: ItemAlreadyExistsException):
    return JSONResponse(
        status_code=409,
        content={
            "error": "Item already exists",
            "item_name": exc.item_name
        }
    )
