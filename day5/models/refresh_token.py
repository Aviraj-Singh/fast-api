from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from models.base import Base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    hashed_token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user = relationship("User", back_populates="refresh_tokens")