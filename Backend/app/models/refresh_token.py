from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    __table_args__ = (
        Index('idx_refresh_token_user', 'user_id'),
        Index('idx_refresh_token_revoked', 'is_revoked'),
        Index('idx_refresh_token_expires', 'expires_at'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(500), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="refresh_tokens")
    
    def __repr__(self):
        return f"<RefreshToken(id={self.id}, user_id={self.user_id}, revoked={self.is_revoked})>"
    
    @property
    def is_expired(self):
        from datetime import datetime, timezone
        return self.expires_at < datetime.now(timezone.utc)