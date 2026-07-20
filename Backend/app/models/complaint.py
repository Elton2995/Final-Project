from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, Text, ForeignKey, Index, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from app.core.database import Base

class ComplaintStatus(str, enum.Enum):
    """Complaint status enum."""
    OPEN = "open"
    IN_PROGRESS = "inprogress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class ComplaintPriority(str, enum.Enum):
    """Complaint priority enum."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class ComplaintCategory(str, enum.Enum):
    """Complaint category enum."""
    TECHNICAL = "Technical Issue"
    BILLING = "Billing"
    SERVICE_OUTAGE = "Service Outage"
    ACCOUNT = "Account Management"
    PRODUCT_QUALITY = "Product Quality"
    CUSTOMER_SERVICE = "Customer Service"
    OTHER = "Other"

class Complaint(Base):
    __tablename__ = "complaints"
    __table_args__ = (
        Index('idx_complaint_user', 'user_id'),
        Index('idx_complaint_assigned', 'assigned_to'),
        Index('idx_complaint_status', 'status'),
        Index('idx_complaint_priority', 'priority'),
        Index('idx_complaint_created', 'created_at'),
        Index('idx_complaint_updated', 'updated_at'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(String(50), unique=True, nullable=False, index=True)  # User-friendly ID like CMP-001
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(Enum(ComplaintCategory), nullable=False)
    status = Column(Enum(ComplaintStatus), default=ComplaintStatus.OPEN, nullable=False)
    priority = Column(Enum(ComplaintPriority), default=ComplaintPriority.MEDIUM, nullable=False)
    
    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Additional fields
    attachments = Column(JSON, default=list, nullable=True)  # List of file URLs
    resolution_notes = Column(Text, nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    closed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # Soft delete
    
    # Relationships
    user = relationship("User", back_populates="complaints", foreign_keys=[user_id])
    assigned_staff = relationship("User", back_populates="complaints_assigned", foreign_keys=[assigned_to])
    responses = relationship("Response", back_populates="complaint", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Complaint(id={self.id}, complaint_id={self.complaint_id}, status={self.status.value})>"
    
    @property
    def is_open(self):
        return self.status in [ComplaintStatus.OPEN, ComplaintStatus.IN_PROGRESS]
    
    @property
    def is_resolved(self):
        return self.status == ComplaintStatus.RESOLVED