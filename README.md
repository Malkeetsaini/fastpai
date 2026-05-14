2. Create Virtual Environment
Linux / Ubuntu
python3 -m venv venv
3. Activate Virtual Environment
Linux / Ubuntu
source venv/bin/activate

After activation you will see:

(venv)
4. Install Requirements
pip install -r requirements.txt
5. Create .env File

Copy .env.example

cp .env.example .env
6. Update .env

Open .env

DATABASE_URL=sqlite+aiosqlite:///./ecommerce.db

SECRET_KEY=mysecretkey

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
7. Create __init__.py Files

Important step.

Inside every folder create empty __init__.py

Example:

touch app/__init__.py

touch app/models/__init__.py
touch app/routers/__init__.py
touch app/schemas/__init__.py
touch app/database/__init__.py
touch app/services/__init__.py
touch app/utils/__init__.py
8. Create Database Tables

Create this file:

create_db.py
from app.database.connection import engine
from app.database.base import Base

from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem

import asyncio

async def init():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init())
9. Run Database File
python create_db.py

This creates:

ecommerce.db
10. Create Admin User

Create:

seed_admin.py
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

Run:

python seed_admin.py
11. Run FastAPI Server
uvicorn app.main:app --reload
12. Open Swagger Docs

Open browser:

http://127.0.0.1:8000/docs

You will see all APIs.

13. Login Admin

Use:

email: admin@gmail.com
password: admin123
14. Copy JWT Token

After login:

{
  "access_token": "TOKEN"
}

Copy token.
