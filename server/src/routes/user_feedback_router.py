from fastapi import APIRouter, Depends, HTTPException
from ..security.authenticated_user import authenticated_user
from ..database import get_db
from ..service.user_feedback_service import UserFeedbackService
from ..schema.feedback_schema import FeedbackCreate
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", status_code=201)
async def create_page(
    payload: FeedbackCreate,
    current_user: dict = Depends(authenticated_user),
    db: Session = Depends(get_db),
):
    return UserFeedbackService.create(
        db=db, payload=payload, user_id=current_user["id"]
    )