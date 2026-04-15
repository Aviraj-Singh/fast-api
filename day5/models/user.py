from sqlalchemy import Column, String, Integer
from models.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    items = relationship("Item", back_populates="owner", cascade="all, delete")
    refresh_tokens = relationship("RefreshToken", cascade="all, delete")