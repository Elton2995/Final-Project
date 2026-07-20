from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base

class Response(Base):
    __tablename__ = "responses"
    __table_args__ = (
        Index('idx_response_complaint', 'complaint_id'),
        Index('idx_response_request', 'request_id'),
        Index('idx_response_user', 'user_id'),
        Index('idx_response_created', 'created_at'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    is_staff_response = Column(Boolean, default=False, nullable=False)
    is_system_response = Column(Boolean, default=False, nullable=False)
    
    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    complaint_id = Column(Integer, ForeignKey("complaints.id", ondelete="CASCADE"), nullable=True)
    request_id = Column(Integer, ForeignKey("service_requests.id", ondelete="CASCADE"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # Soft delete
    
    # Relationships
    user = relationship("User", back_populates="responses")
    complaint = relationship("Complaint", back_populates="responses")
    service_request = relationship("ServiceRequest", back_populates="responses")
    
    def __repr__(self):
        return f"<Response(id={self.id}, user_id={self.user_id})>"