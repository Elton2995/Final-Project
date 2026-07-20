from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import require_admin, require_customer
from app.schemas.feedback import (
    Feedback,
    FeedbackCreate,
    FeedbackUpdate,
    FeedbackListResponse,
    FeedbackStats
)
from app.schemas.common import ResponseMessage
from app.crud.feedback import feedback_crud
from app.crud.audit_log import audit_log_crud
from app.models.user import UserRole

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post(
    "/feedback",
    response_model=Feedback,
    status_code=status.HTTP_201_CREATED,
    summary="Submit feedback",
    description="Submit feedback about the service. Customer only."
)
async def submit_feedback(
    feedback_data: FeedbackCreate,
    request: Request,
    current_user: User = Depends(require_customer),
    db: Session = Depends(get_db)
):
    """Submit feedback."""
    feedback = feedback_crud.create(
        db,
        obj_in=feedback_data,
        user_id=current_user.id
    )
    
    audit_log_crud.log_action(
        db,
        user_id=current_user.id,
        action="create",
        resource_type="feedback",
        resource_id=feedback.id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    logger.info(f"User {current_user.email} submitted feedback (rating: {feedback.rating})")
    
    return feedback

@router.get(
    "/feedback",
    response_model=FeedbackListResponse,
    summary="Get feedback",
    description="Get feedback with filtering. Admin or staff only."
)
async def get_feedback(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = None,
    rating: Optional[int] = Query(None, ge=1, le=5),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get feedback with filtering."""
    filters = {}
    if category:
        filters["category"] = category
    if rating:
        filters["rating"] = rating
    
    feedback_list = feedback_crud.get_multi(
        db,
        skip=skip,
        limit=limit,
        filters=filters
    )
    
    total = feedback_crud.count(db, filters=filters)
    
    return FeedbackListResponse(
        items=feedback_list,
        total=total
    )

@router.get(
    "/feedback/my",
    response_model=FeedbackListResponse,
    summary="Get my feedback",
    description="Get current user's feedback."
)
async def get_my_feedback(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's feedback."""
    feedback_list = feedback_crud.get_by_user(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    
    total = len(feedback_list)
    
    return FeedbackListResponse(
        items=feedback_list,
        total=total
    )

@router.get(
    "/feedback/stats",
    response_model=FeedbackStats,
    summary="Get feedback statistics",
    description="Get feedback statistics. Admin only."
)
async def get_feedback_stats(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get feedback statistics."""
    stats = feedback_crud.get_stats(db)
    
    return FeedbackStats(
        total=stats["total"],
        average_rating=stats["average_rating"],
        rating_distribution=stats["rating_distribution"],
        would_recommend=stats["would_recommend"],
        by_category=stats["by_category"]
    )