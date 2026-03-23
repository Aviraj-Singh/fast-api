from fastapi import HTTPException, Depends, Header
from config import SECRET_KEY

def get_token(token: str = Header()):
    return token

def get_current_user(token=Depends(get_token)):
    print(f"Secret Token: {SECRET_KEY}")
    if SECRET_KEY is None:
        raise RuntimeError("SECRET_TOKEN not set")
    if token != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"user": "Aviraj"}