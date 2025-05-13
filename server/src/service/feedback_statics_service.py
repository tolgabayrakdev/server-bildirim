from sqlalchemy.orm import Session
from sqlalchemy import func, distinct, extract
from ..model import Feedback, FeedbackPage, PreviewPage, FeedbackType
from fastapi import HTTPException
from datetime import datetime

class FeedbackStaticsService:

    @staticmethod
    def get_feedback_count(db: Session, user_id: int):
        try:
            # Her feedback tipi için sayıları hesapla
            feedback_counts = db.query(Feedback.feedback_type, func.count(distinct(Feedback.id)))\
                .join(FeedbackPage)\
                .join(PreviewPage)\
                .filter(PreviewPage.user_id == user_id)\
                .group_by(Feedback.feedback_type)\
                .all()
            
            # Sonuçları sözlük olarak hazırla
            result = {feedback_type.value: 0 for feedback_type in FeedbackType}
            for feedback_type, count in feedback_counts:
                result[feedback_type.value] = count

            # Toplam feedback sayısını hesapla
            total_feedback_count = sum(result.values())
            result["total_feedback_count"] = total_feedback_count

            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @staticmethod
    def get_monthly_feedback_count(db: Session, user_id: int):
        try:
            current_year = datetime.now().year
            
            # Her feedback tipi için aylık sayıları hesapla
            feedback_counts = db.query(
                Feedback.feedback_type,
                func.count(distinct(Feedback.id)).label('count'),
                extract('month', Feedback.created_at).label('month')
            ).join(FeedbackPage)\
             .join(PreviewPage)\
             .filter(PreviewPage.user_id == user_id)\
             .filter(extract('year', Feedback.created_at) == current_year)\
             .group_by(Feedback.feedback_type, extract('month', Feedback.created_at))\
             .all()

            # Sonuçları sözlük olarak hazırla
            result = {month: {feedback_type.value: 0 for feedback_type in FeedbackType} for month in range(1, 13)}
            
            for feedback_type, count, month in feedback_counts:
                result[month][feedback_type.value] = count

            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
