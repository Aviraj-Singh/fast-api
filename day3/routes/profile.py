from fastapi import APIRouter, Depends
from dependencies.auth import get_current_user

router = APIRouter()

@router.get("/profile")
def profile(user = Depends(get_current_user)):
    return user