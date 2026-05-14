from pydantic import BaseModel
from typing import List

class OrderItemSchema(BaseModel):
    product_id: str
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemSchema]
