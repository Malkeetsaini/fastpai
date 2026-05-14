import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func

from app.database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="user")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
