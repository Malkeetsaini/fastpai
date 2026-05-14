# FastAPI E-Commerce Backend

A production-ready asynchronous E-Commerce REST API built with FastAPI, SQLAlchemy, and SQLite.

## Prerequisites

Ensure you have **Python 3.8+** installed on your system.

## Setup Instructions

Follow these steps to set up and run the application locally on Linux / Ubuntu.

### 1. Create Virtual Environment
Initialize a fresh Python virtual environment to manage dependencies:
```bash
python3 -m venv venv
```

### 2. Activate Virtual Environment
Activate the environment before installing packages:
```bash
source venv/bin/activate
```
*Note: Your terminal prompt will change to show `(venv)` upon successful activation.*

### 3. Install Requirements
Install all necessary application dependencies:
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Copy the template file to create your active environment configuration:
```bash
cp .env.example .env
```

Open the newly created `.env` file and configure your variables:
```env
DATABASE_URL=sqlite+aiosqlite:///./ecommerce.db
SECRET_KEY=mysecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Initialize Package Structure
Create the required `__init__.py` files across all application directories to enable proper Python module discovery:
```bash
touch app/__init__.py
touch app/models/__init__.py
touch app/routers/__init__.py
touch app/schemas/__init__.py
touch app/database/__init__.py
touch app/services/__init__.py
touch app/utils/__init__.py
```

### 6. Database Initialization
Generate the database tables defined in the SQLAlchemy models. 

1. Ensure a helper script named `create_db.py` exists with the following setup logic:
```python
import asyncio
from app.database.connection import engine
from app.database.base import Base
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init())
```
2. Run the initialization script to generate your local `ecommerce.db` file:
```bash
python create_db.py
```

### 7. Seed Administrative User
Create a default administrator account for system access.

1. Ensure a helper script named `seed_admin.py` exists with the following setup logic:
```python
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
```
2. Execute the seeding script:
```bash
python seed_admin.py
```

---

## Running the Application

### Start the Uvicorn Server
Launch the development server with live-reload enabled:
```bash
uvicorn app.main:app --reload
```

### API Documentation & Testing
Once the server is running, you can interact with the endpoints directly from your browser:
* **Interactive Swagger UI Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Admin Authentication Flow
1. Navigate to the login endpoint on the Swagger UI page.
2. Authenticate using the default admin credentials:
   * **Email:** `admin@gmail.com`
   * **Password:** `admin123`
3. The server will return a JSON Web Token (JWT) structured as follows:
   ```json
   {
     "access_token": "YOUR_GENERATED_JWT_TOKEN",
     "token_type": "bearer"
   }
   ```
4. Copy the raw `access_token` value string and paste it into the **Authorize** lock button at the top of the Swagger page to test protected administration endpoints.
