from sqlalchemy.orm import Session
from ..model import Feedback, FeedbackPage, PreviewPage
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class FeedbackService:


    @staticmethod
    def list(db: Session, user_id: int):
        feedbacks = db.query(Feedback).join(FeedbackPage).join(PreviewPage).filter(PreviewPage.user_id == user_id).all()
        return feedbacks
    
    @staticmethod
    def delete(db: Session, feedback_id: int, user_id: int):
        try:
            feedback = (
                db.query(Feedback).join(FeedbackPage).join(PreviewPage)
                .filter(Feedback.id == feedback_id, PreviewPage.user_id == user_id).first()
            )
            if feedback:
                db.delete(feedback)
                db.commit()
                return {"message": "Feedback deleted"}
            else:
                raise HTTPException(status_code=404, detail="Feedback not found")
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=500, detail="An unexpected server error occurred."
            )

    @staticmethod
    def delete_all(db: Session, user_id: int):
        try:
            feedbacks = db.query(Feedback).join(FeedbackPage).join(PreviewPage).filter(PreviewPage.user_id == user_id).all()
            for feedback in feedbacks:
                db.delete(feedback)
            db.commit()
            return {"message": "All feedbacks deleted"}
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=500, detail="An unexpected server error occurred."
            )

    @staticmethod
    def list_by_user(db: Session, user_id: int):
        feedbacks = (
            db.query(Feedback.id, Feedback.content, Feedback.customer_email, Feedback.feedback_type, Feedback.created_at, FeedbackPage.title)
            .join(FeedbackPage)
            .filter(PreviewPage.user_id == user_id)
            .all()
        )
        print(f"Fetched feedbacks: {feedbacks}")

        def format_date(date):
            if isinstance(date, str):
                date = datetime.fromisoformat(date)
            return date.strftime("%d.%m.%Y %H:%M")

        result = [
            {
                "id": feedback.id,
                "content": feedback.content,
                "customer_email": feedback.customer_email,
                "feedback_type": feedback.feedback_type,
                "created_at": format_date(feedback.created_at),
                "feedback_page_title": feedback.title
            }
            for feedback in feedbacks
        ]
        return result