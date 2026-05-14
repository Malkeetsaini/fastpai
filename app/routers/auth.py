from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.auth import *
from app.models.user import User

from app.database.session import AsyncSessionLocal

from app.utils.hashing import *
from app.utils.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/register")
async def register(
    data: RegisterSchema,
    db: AsyncSession = Depends(get_db)
):

    user = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password)
    )

    db.add(user)

    await db.commit()

    return {"message": "User registered"}

@router.post("/login")
async def login(
    data: LoginSchema,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(User).where(User.email == data.email)
    )

    user = result.scalar()

    if not user:
        return {"message": "Invalid Credentials"}

    if not verify_password(data.password, user.password):
        return {"message": "Invalid Credentials"}

    token = create_access_token({
        "id": user.id,
        "role": user.role
    })

    return {
        "access_token": token
    }
