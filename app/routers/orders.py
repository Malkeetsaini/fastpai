from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product

from app.schemas.order import OrderCreate

from app.database.session import AsyncSessionLocal

from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/")
async def create_order(
    data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):

    total = 0

    order = Order(
        user_id=user["id"]
    )

    db.add(order)

    await db.flush()

    for item in data.items:

        result = await db.execute(
            select(Product).where(
                Product.id == item.product_id
            )
        )

        product = result.scalar()

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail="Stock unavailable"
            )

        product.stock -= item.quantity

        price = product.price * item.quantity

        total += price

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=price
        )

        db.add(order_item)

    order.total_amount = total

    await db.commit()

    return {
        "message": "Order created",
        "total": total
    }
