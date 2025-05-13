from fastapi import APIRouter, Depends
from ..security.authenticated_user import authenticated_user
from ..database import get_db
from ..service.feedback_service import FeedbackService
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", status_code=201)
def list_feedbacks(
    db: Session = Depends(get_db), current_user: dict = Depends(authenticated_user)
):
    return FeedbackService.list(db=db, user_id=current_user["id"])


@router.get("/user-feedbacks", status_code=200)
def list_user_feedbacks(
    db: Session = Depends(get_db), current_user: dict = Depends(authenticated_user)
):
    return FeedbackService.list_by_user(db=db, user_id=current_user["id"])


@router.delete("/{feedback_id}", status_code=200)
def delete_feedback(
    feedback_id: int, db: Session = Depends(get_db), current_user: dict = Depends(authenticated_user)
):
    return FeedbackService.delete(db=db, feedback_id=feedback_id, user_id=current_user["id"])


@router.delete("/", status_code=200)
def delete_all_feedbacks(
    db: Session = Depends(get_db), current_user: dict = Depends(authenticated_user)
):
    return FeedbackService.delete_all(db=db, user_id=current_user["id"])


