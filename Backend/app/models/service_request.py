from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, Text, ForeignKey, Index, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base

class RequestStatus(str, enum.Enum):
    """Service request status enum."""
    PENDING = "open"
    IN_PROGRESS = "inprogress"
    COMPLETED = "resolved"
    CANCELLED = "closed"

class RequestPriority(str, enum.Enum):
    """Service request priority enum."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class RequestCategory(str, enum.Enum):
    """Service request category enum."""
    INSTALLATION = "Installation"
    NEW_SERVICE = "New Service"
    UPGRADE = "Upgrade"
    REPAIR = "Repair"
    MAINTENANCE = "Maintenance"
    OTHER = "Other"

class ServiceRequest(Base):
    __tablename__ = "service_requests"
    __table_args__ = (
        Index('idx_request_user', 'user_id'),
        Index('idx_request_assigned', 'assigned_to'),
        Index('idx_request_status', 'status'),
        Index('idx_request_created', 'created_at'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String(50), unique=True, nullable=False, index=True)  # User-friendly ID like REQ-001
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(Enum(RequestCategory), nullable=False)
    status = Column(Enum(RequestStatus), default=RequestStatus.PENDING, nullable=False)
    priority = Column(Enum(RequestPriority), default=RequestPriority.MEDIUM, nullable=False)
    
    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Additional fields
    preferred_date = Column(DateTime(timezone=True), nullable=True)
    preferred_time = Column(String(50), nullable=True)
    attachments = Column(JSON, default=list, nullable=True)
    technician_name = Column(String(255), nullable=True)
    completion_notes = Column(Text, nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # Soft delete
    
    # Relationships
    user = relationship("User", back_populates="service_requests", foreign_keys=[user_id])
    assigned_staff = relationship("User", back_populates="service_requests_assigned", foreign_keys=[assigned_to])
    responses = relationship("Response", back_populates="service_request", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ServiceRequest(id={self.id}, request_id={self.request_id}, status={self.status.value})>"
    
    @property
    def is_pending(self):
        return self.status == RequestStatus.PENDING
    
    @property
    def is_completed(self):
        return self.status == RequestStatus.COMPLETED