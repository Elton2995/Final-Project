from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.crud.base import CRUDBase
from app.models.feedback import Feedback, FeedbackCategory
from app.schemas.feedback import FeedbackCreate, FeedbackUpdate

class CRUDFeedback(CRUDBase[Feedback, FeedbackCreate, FeedbackUpdate]):
    """Feedback CRUD operations."""
    
    def get_by_user(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Feedback]:
        """Get feedback by a specific user."""
        return db.query(Feedback).filter(
            Feedback.user_id == user_id,
            Feedback.deleted_at.is_(None)
        ).order_by(desc(Feedback.created_at)).offset(skip).limit(limit).all()
    
    def get_by_category(
        self,
        db: Session,
        category: FeedbackCategory,
        skip: int = 0,
        limit: int = 100
    ) -> List[Feedback]:
        """Get feedback by category."""
        return db.query(Feedback).filter(
            Feedback.category == category,
            Feedback.deleted_at.is_(None)
        ).order_by(desc(Feedback.created_at)).offset(skip).limit(limit).all()
    
    def get_stats(self, db: Session) -> Dict[str, Any]:
        """Get feedback statistics."""
        total = db.query(Feedback).filter(Feedback.deleted_at.is_(None)).count()
        
        # Average rating
        avg_rating = db.query(func.avg(Feedback.rating)).filter(
            Feedback.deleted_at.is_(None)
        ).scalar() or 0
        
        # Rating distribution
        rating_distribution = {}
        for i in range(1, 6):
            count = db.query(Feedback).filter(
                Feedback.rating == i,
                Feedback.deleted_at.is_(None)
            ).count()
            rating_distribution[str(i)] = count
        
        # Would recommend
        would_recommend = {
            "yes": db.query(Feedback).filter(
                Feedback.would_recommend == True,
                Feedback.deleted_at.is_(None)
            ).count(),
            "no": db.query(Feedback).filter(
                Feedback.would_recommend == False,
                Feedback.deleted_at.is_(None)
            ).count(),
            "unspecified": db.query(Feedback).filter(
                Feedback.would_recommend.is_(None),
                Feedback.deleted_at.is_(None)
            ).count()
        }
        
        # By category
        category_counts = {}
        for category in FeedbackCategory:
            count = db.query(Feedback).filter(
                Feedback.category == category,
                Feedback.deleted_at.is_(None)
            ).count()
            category_counts[category.value] = count
        
        return {
            "total": total,
            "average_rating": round(float(avg_rating), 2),
            "rating_distribution": rating_distribution,
            "would_recommend": would_recommend,
            "by_category": category_counts
        }

# Singleton instance
feedback_crud = CRUDFeedback(Feedback)