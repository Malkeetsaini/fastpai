import uuid
from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.sql import func

from app.database.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    image = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
