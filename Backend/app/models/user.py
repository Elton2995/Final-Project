from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, Text, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from app.core.database import Base

class UserRole(str, enum.Enum):
    """User roles enum."""
    ADMIN = "admin"
    STAFF = "staff"
    CUSTOMER = "customer"

class UserStatus(str, enum.Enum):
    """User status enum."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index('idx_user_email', 'email'),
        Index('idx_user_role', 'role'),
        Index('idx_user_status', 'status'),
        Index('idx_user_deleted_at', 'deleted_at'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE, nullable=False)
    avatar = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # Soft delete
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    complaints = relationship("Complaint", back_populates="user", foreign_keys="Complaint.user_id")
    complaints_assigned = relationship("Complaint", back_populates="assigned_staff", foreign_keys="Complaint.assigned_to")
    service_requests = relationship("ServiceRequest", back_populates="user", foreign_keys="ServiceRequest.user_id")
    service_requests_assigned = relationship("ServiceRequest", back_populates="assigned_staff", foreign_keys="ServiceRequest.assigned_to")
    feedbacks = relationship("Feedback", back_populates="user")
    responses = relationship("Response", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role.value})>"
    
    @property
    def is_active(self):
        return self.status == UserStatus.ACTIVE and self.deleted_at is None
    
    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN
    
    @property
    def is_staff(self):
        return self.role in [UserRole.ADMIN, UserRole.STAFF]
    
    @property
    def is_customer(self):
        return self.role == UserRole.CUSTOMER