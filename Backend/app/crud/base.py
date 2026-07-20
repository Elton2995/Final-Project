from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc
from datetime import datetime, timezone

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base CRUD class with common operations."""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """Get a single record by ID."""
        return db.query(self.model).filter(
            self.model.id == id,
            self.model.deleted_at.is_(None)
        ).first()
    
    def get_with_deleted(self, db: Session, id: int) -> Optional[ModelType]:
        """Get a single record by ID including soft-deleted."""
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_by_id(self, db: Session, id: int) -> Optional[ModelType]:
        """Alias for get method."""
        return self.get(db, id)
    
    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
        filters: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None,
        search_fields: Optional[List[str]] = None
    ) -> List[ModelType]:
        """Get multiple records with pagination, sorting, and filtering."""
        query = db.query(self.model).filter(self.model.deleted_at.is_(None))
        
        # Apply filters
        if filters:
            for key, value in filters.items():
                if value is not None:
                    query = query.filter(getattr(self.model, key) == value)
        
        # Apply search
        if search and search_fields:
            search_conditions = []
            for field in search_fields:
                search_conditions.append(
                    getattr(self.model, field).ilike(f"%{search}%")
                )
            if search_conditions:
                from sqlalchemy import or_
                query = query.filter(or_(*search_conditions))
        
        # Apply sorting
        if sort_by:
            sort_column = getattr(self.model, sort_by)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(self.model.created_at))
        
        return query.offset(skip).limit(limit).all()
    
    def count(
        self,
        db: Session,
        filters: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None,
        search_fields: Optional[List[str]] = None
    ) -> int:
        """Count total records with filters."""
        query = db.query(self.model).filter(self.model.deleted_at.is_(None))
        
        if filters:
            for key, value in filters.items():
                if value is not None:
                    query = query.filter(getattr(self.model, key) == value)
        
        if search and search_fields:
            search_conditions = []
            for field in search_fields:
                search_conditions.append(
                    getattr(self.model, field).ilike(f"%{search}%")
                )
            if search_conditions:
                from sqlalchemy import or_
                query = query.filter(or_(*search_conditions))
        
        return query.count()
    
    def create(
        self,
        db: Session,
        *,
        obj_in: CreateSchemaType,
        **extra_data
    ) -> ModelType:
        """Create a new record."""
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, **extra_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Update an existing record."""
        obj_data = jsonable_encoder(db_obj)
        
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = jsonable_encoder(obj_in, exclude_unset=True)
        
        # Handle dates
        if 'updated_at' not in update_data:
            update_data['updated_at'] = datetime.now(timezone.utc)
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, *, id: int) -> Optional[ModelType]:
        """Hard delete a record."""
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj
    
    def soft_delete(self, db: Session, *, id: int) -> Optional[ModelType]:
        """Soft delete a record."""
        obj = self.get(db, id)
        if obj:
            obj.deleted_at = datetime.now(timezone.utc)
            obj.updated_at = datetime.now(timezone.utc)
            db.add(obj)
            db.commit()
            db.refresh(obj)
        return obj
    
    def restore(self, db: Session, *, id: int) -> Optional[ModelType]:
        """Restore a soft-deleted record."""
        obj = db.query(self.model).filter(
            self.model.id == id,
            self.model.deleted_at.is_not(None)
        ).first()
        if obj:
            obj.deleted_at = None
            obj.updated_at = datetime.now(timezone.utc)
            db.add(obj)
            db.commit()
            db.refresh(obj)
        return obj
    
    def exists(self, db: Session, **kwargs) -> bool:
        """Check if a record exists matching the given criteria."""
        query = db.query(self.model).filter(self.model.deleted_at.is_(None))
        for key, value in kwargs.items():
            query = query.filter(getattr(self.model, key) == value)
        return query.first() is not None