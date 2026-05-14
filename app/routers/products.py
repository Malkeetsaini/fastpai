from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import shutil

from app.models.product import Product
from app.schemas.product import ProductCreate

from app.database.session import AsyncSessionLocal

from app.utils.dependencies import admin_required

router = APIRouter(prefix="/products", tags=["Products"])

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/")
async def create_product(
    data: ProductCreate = Depends(),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(admin_required)
):

    file_path = f"app/uploads/{image.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    product = Product(
        name=data.name,
        description=data.description,
        price=data.price,
        stock=data.stock,
        image=file_path
    )

    db.add(product)

    await db.commit()

    return {"message": "Product created"}

@router.get("/")
async def get_products(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    db: AsyncSession = Depends(get_db)
):

    query = select(Product)

    if search:
        query = query.where(
            Product.name.ilike(f"%{search}%")
        )

    result = await db.execute(
        query.offset((page - 1) * limit).limit(limit)
    )

    return result.scalars().all()
