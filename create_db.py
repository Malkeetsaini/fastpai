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