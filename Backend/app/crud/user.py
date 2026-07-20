from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import datetime, timezone

from app.crud.base import CRUDBase
from app.models.user import User, UserRole, UserStatus
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """User CRUD operations."""
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email."""
        return db.query(User).filter(
            User.email == email,
            User.deleted_at.is_(None)
        ).first()
    
    def get_by_email_with_deleted(self, db: Session, email: str) -> Optional[User]:
        """Get user by email including soft-deleted."""
        return db.query(User).filter(User.email == email).first()
    
    def get_active_users(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """Get all active users."""
        return db.query(User).filter(
            User.status == UserStatus.ACTIVE,
            User.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    
    def get_by_role(
        self,
        db: Session,
        role: UserRole,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """Get users by role."""
        return db.query(User).filter(
            User.role == role,
            User.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    
    def get_staff(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all staff (admin + staff roles)."""
        return db.query(User).filter(
            User.role.in_([UserRole.ADMIN, UserRole.STAFF]),
            User.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """Create a new user with hashed password."""
        db_obj = User(
            full_name=obj_in.full_name,
            email=obj_in.email,
            phone=obj_in.phone,
            role=obj_in.role,
            password_hash=get_password_hash(obj_in.password),
            status=UserStatus.ACTIVE
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update_password(
        self,
        db: Session,
        *,
        user: User,
        new_password: str
    ) -> User:
        """Update user password."""
        user.password_hash = get_password_hash(new_password)
        user.updated_at = datetime.now(timezone.utc)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def authenticate(
        self,
        db: Session,
        *,
        email: str,
        password: str
    ) -> Optional[User]:
        """Authenticate user by email and password."""
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        if user.status != UserStatus.ACTIVE:
            return None
        if user.deleted_at:
            return None
        return user
    
    def update_last_login(self, db: Session, *, user: User) -> User:
        """Update user's last login timestamp."""
        user.last_login = datetime.now(timezone.utc)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def update_role(self, db: Session, *, user: User, role: UserRole) -> User:
        """Update user role."""
        user.role = role
        user.updated_at = datetime.now(timezone.utc)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def update_status(self, db: Session, *, user: User, status: UserStatus) -> User:
        """Update user status."""
        user.status = status
        user.updated_at = datetime.now(timezone.utc)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def search_users(
        self,
        db: Session,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """Search users by name or email."""
        return db.query(User).filter(
            User.deleted_at.is_(None),
            or_(
                User.full_name.ilike(f"%{query}%"),
                User.email.ilike(f"%{query}%")
            )
        ).offset(skip).limit(limit).all()
    
    def get_count_by_status(self, db: Session) -> Dict[str, int]:
        """Get user count by status."""
        result = {}
        for status in UserStatus:
            count = db.query(User).filter(
                User.status == status,
                User.deleted_at.is_(None)
            ).count()
            result[status.value] = count
        return result
    
    def get_count_by_role(self, db: Session) -> Dict[str, int]:
        """Get user count by role."""
        result = {}
        for role in UserRole:
            count = db.query(User).filter(
                User.role == role,
                User.deleted_at.is_(None)
            ).count()
            result[role.value] = count
        return result

# Singleton instance
user_crud = CRUDUser(User)