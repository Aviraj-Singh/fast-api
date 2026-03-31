from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import Base
from sqlalchemy.orm import relationship

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    owner = relationship("User", back_populates="items")