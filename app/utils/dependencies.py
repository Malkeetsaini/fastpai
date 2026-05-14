from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt

from app.database.config import SECRET_KEY, ALGORITHM

security = HTTPBearer()

def get_current_user(token=Depends(security)):

    try:
        payload = jwt.decode(
            token.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

def admin_required(user=Depends(get_current_user)):

    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin only"
        )

    return user
