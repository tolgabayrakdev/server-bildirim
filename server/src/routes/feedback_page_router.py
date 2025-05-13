from fastapi import APIRouter, Depends
from ..security.authenticated_user import authenticated_user
from ..database import get_db
from sqlalchemy.orm import Session
from ..service.feedback_page_service import FeedbackPageService
from ..schema.feedback_page_schema import FeedbackPageCreate

router = APIRouter()


@router.post("/", status_code=201)
def create_page(
    feedback: FeedbackPageCreate,
    current_user: dict = Depends(authenticated_user),
    db: Session = Depends(get_db),
):
    return FeedbackPageService.create(
        db=db, payload=feedback, user_id=current_user["id"]
    )


@router.get("/")
def get_all_pages(db: Session = Depends(get_db), current_user: dict = Depends(authenticated_user)):
    return FeedbackPageService.get_all(db=db, user_id=current_user["id"])

@router.get("/{url_token}")
def show_feedback_page(url_token: str, db: Session = Depends(get_db)):
    return FeedbackPageService.show(db, url_token)


@router.delete("/{feedback_id}")
def delete_page(feedback_id: int, db: Session = Depends(get_db)):
    return FeedbackPageService.delete(db=db, feedback_id=feedback_id)

