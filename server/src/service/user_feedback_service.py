from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..model import Feedback
from ..schema.feedback_schema import FeedbackCreate

class UserFeedbackService:

    @staticmethod
    def create(db: Session, payload: FeedbackCreate, user_id: int):
        try:
            feedback = Feedback(
                feedback_type=payload.feedback_type,
                content=payload.content,
                created_at=datetime.now(),
                customer_email=payload.customer_email,
                feedback_page_id=payload.feedback_page_id,)
            db.add(feedback)
            db.commit()
            db.refresh(feedback)
            return {"message": "Feedback created"}
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=500, detail="An unexpected server error occurred."
            )
        