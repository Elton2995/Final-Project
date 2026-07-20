from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, Text, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base

class FeedbackCategory(str, enum.Enum):
    """Feedback category enum."""
    OVERALL = "Overall Experience"
    SERVICE_QUALITY = "Service Quality"
    STAFF_PROFESSIONALISM = "Staff Professionalism"
    RESOLUTION_TIME = "Resolution Time"
    COMMUNICATION = "Communication"
    WEBSITE_USABILITY = "Website/App Usability"

class Feedback(Base):
    __tablename__ = "feedbacks"
    __table_args__ = (
        Index('idx_feedback_user', 'user_id'),
        Index('idx_feedback_rating', 'rating'),
        Index('idx_feedback_created', 'created_at'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    category = Column(Enum(FeedbackCategory), nullable=False)
    message = Column(Text, nullable=False)
    suggestion = Column(Text, nullable=True)
    would_recommend = Column(Boolean, nullable=True)
    
    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # Soft delete
    
    # Relationships
    user = relationship("User", back_populates="feedbacks")
    
    def __repr__(self):
        return f"<Feedback(id={self.id}, user_id={self.user_id}, rating={self.rating})>"