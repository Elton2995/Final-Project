from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_
from datetime import datetime, timedelta

from app.crud.base import CRUDBase
from app.models.audit_log import AuditLog, AuditAction
from app.schemas.audit_log import AuditLogCreate

class CRUDAuditLog(CRUDBase[AuditLog, AuditLogCreate, AuditLogCreate]):
    """Audit Log CRUD operations."""
    
    def get_by_user(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        """Get audit logs for a specific user."""
        return db.query(AuditLog).filter(
            AuditLog.user_id == user_id
        ).order_by(desc(AuditLog.created_at)).offset(skip).limit(limit).all()
    
    def get_by_action(
        self,
        db: Session,
        action: AuditAction,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        """Get audit logs by action type."""
        return db.query(AuditLog).filter(
            AuditLog.action == action
        ).order_by(desc(AuditLog.created_at)).offset(skip).limit(limit).all()
    
    def get_by_resource(
        self,
        db: Session,
        resource_type: str,
        resource_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        """Get audit logs for a specific resource."""
        return db.query(AuditLog).filter(
            AuditLog.resource_type == resource_type,
            AuditLog.resource_id == resource_id
        ).order_by(desc(AuditLog.created_at)).offset(skip).limit(limit).all()
    
    def get_recent(
        self,
        db: Session,
        days: int = 7,
        limit: int = 100
    ) -> List[AuditLog]:
        """Get recent audit logs."""
        cutoff = datetime.now() - timedelta(days=days)
        return db.query(AuditLog).filter(
            AuditLog.created_at >= cutoff
        ).order_by(desc(AuditLog.created_at)).limit(limit).all()
    
    def log_action(
        self,
        db: Session,
        user_id: Optional[int],
        action: AuditAction,
        resource_type: Optional[str] = None,
        resource_id: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AuditLog:
        """Log an action."""
        return self.create(
            db,
            obj_in=AuditLogCreate(
                user_id=user_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                details=details,
                ip_address=ip_address,
                user_agent=user_agent
            )
        )
    
    def get_stats(self, db: Session) -> Dict[str, Any]:
        """Get audit log statistics."""
        total = db.query(AuditLog).count()
        
        action_counts = {}
        for action in AuditAction:
            count = db.query(AuditLog).filter(
                AuditLog.action == action
            ).count()
            if count > 0:
                action_counts[action.value] = count
        
        # Last 7 days activity
        cutoff = datetime.now() - timedelta(days=7)
        daily_counts = db.query(
            func.date(AuditLog.created_at).label('date'),
            func.count(AuditLog.id).label('count')
        ).filter(
            AuditLog.created_at >= cutoff
        ).group_by(func.date(AuditLog.created_at)).all()
        
        return {
            "total": total,
            "by_action": action_counts,
            "daily_counts": [
                {"date": str(d.date), "count": d.count} 
                for d in daily_counts
            ]
        }

# Singleton instance
audit_log_crud = CRUDAuditLog(AuditLog)