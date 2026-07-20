from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Index
from sqlalchemy.sql import func

from app.core.database import Base

class SystemSetting(Base):
    __tablename__ = "system_settings"
    __table_args__ = (
        Index('idx_setting_key', 'setting_key', unique=True),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    setting_key = Column(String(100), unique=True, nullable=False, index=True)
    setting_value = Column(Text, nullable=False)
    description = Column(String(500), nullable=True)
    is_public = Column(Boolean, default=False, nullable=False)  # Whether setting is exposed to frontend
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<SystemSetting(id={self.id}, key={self.setting_key})>"