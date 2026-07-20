from sqlalchemy import Column, Integer, String, DateTime, Enum, Text, ForeignKey, Index, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base

class AuditAction(str, enum.Enum):
    """Audit action enum."""
    LOGIN = "login"
    LOGOUT = "logout"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    SOFT_DELETE = "soft_delete"
    RESTORE = "restore"
    ROLE_CHANGE = "role_change"
    PERMISSION_CHANGE = "permission_change"
    STATUS_CHANGE = "status_change"
    ASSIGN = "assign"
    RESOLVE = "resolve"
    CLOSE = "close"

class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = (
        Index('idx_audit_user', 'user_id'),
        Index('idx_audit_action', 'action'),
        Index('idx_audit_created', 'created_at'),
        Index('idx_audit_resource', 'resource_type', 'resource_id'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(Enum(AuditAction), nullable=False)
    resource_type = Column(String(50), nullable=True)  # Table or entity name
    resource_id = Column(Integer, nullable=True)  # ID of the affected resource
    details = Column(JSON, nullable=True)  # Additional details as JSON
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, user_id={self.user_id}, action={self.action.value})>"
    
    @classmethod
    def create_log(
        cls,
        user_id: int,
        action: AuditAction,
        resource_type: str = None,
        resource_id: int = None,
        details: dict = None,
        ip_address: str = None,
        user_agent: str = None
    ):
        """Factory method to create an audit log entry."""
        return cls(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent
        )