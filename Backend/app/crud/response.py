from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc

from app.crud.base import CRUDBase
from app.models.response import Response
from app.schemas.response import ResponseCreate, ResponseUpdate

class CRUDResponse(CRUDBase[Response, ResponseCreate, ResponseUpdate]):
    """Response CRUD operations."""
    
    def get_by_complaint(
        self,
        db: Session,
        complaint_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Response]:
        """Get responses for a specific complaint."""
        return db.query(Response).options(
            joinedload(Response.user)
        ).filter(
            Response.complaint_id == complaint_id,
            Response.deleted_at.is_(None)
        ).order_by(desc(Response.created_at)).offset(skip).limit(limit).all()
    
    def get_by_request(
        self,
        db: Session,
        request_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Response]:
        """Get responses for a specific service request."""
        return db.query(Response).options(
            joinedload(Response.user)
        ).filter(
            Response.request_id == request_id,
            Response.deleted_at.is_(None)
        ).order_by(desc(Response.created_at)).offset(skip).limit(limit).all()
    
    def get_by_user(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Response]:
        """Get responses by a specific user."""
        return db.query(Response).filter(
            Response.user_id == user_id,
            Response.deleted_at.is_(None)
        ).order_by(desc(Response.created_at)).offset(skip).limit(limit).all()
    
    def create_for_complaint(
        self,
        db: Session,
        *,
        complaint_id: int,
        user_id: int,
        message: str,
        is_staff_response: bool = False,
        is_system_response: bool = False
    ) -> Response:
        """Create a response for a complaint."""
        return self.create(
            db,
            obj_in=ResponseCreate(message=message),
            complaint_id=complaint_id,
            user_id=user_id,
            is_staff_response=is_staff_response,
            is_system_response=is_system_response
        )
    
    def create_for_request(
        self,
        db: Session,
        *,
        request_id: int,
        user_id: int,
        message: str,
        is_staff_response: bool = False,
        is_system_response: bool = False
    ) -> Response:
        """Create a response for a service request."""
        return self.create(
            db,
            obj_in=ResponseCreate(message=message),
            request_id=request_id,
            user_id=user_id,
            is_staff_response=is_staff_response,
            is_system_response=is_system_response
        )

# Singleton instance
response_crud = CRUDResponse(Response)