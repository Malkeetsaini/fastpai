import asyncio

from sqlalchemy import select

from app.models.user import User
from app.database.session import AsyncSessionLocal

from app.utils.hashing import hash_password

async def seed():

    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(User).where(User.email == "admin@gmail.com")
        )

        admin = result.scalar()

        if admin:
            print("Admin already exists")
            return

        user = User(
            name="Admin",
            email="admin@gmail.com",
            password=hash_password("admin123"),
            role="admin"
        )

        db.add(user)

        await db.commit()

        print("Admin Created")

asyncio.run(seed())