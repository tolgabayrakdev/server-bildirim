from fastapi import APIRouter, Depends, HTTPException
from ..security.authenticated_user import authenticated_user
from ..database import get_db
from ..service.preview_page_service import PreviewPageService
from ..schema.preview_page_schema import PreviewPageCreate, PreviewPageUpdate
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", status_code=201)
async def create_page(
    preview: PreviewPageCreate,
    current_user: dict = Depends(authenticated_user),
    db: Session = Depends(get_db),
):
    try:
        return PreviewPageService.create(db=db, payload=preview, user_id=current_user["id"])
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{url_token}")
async def show_page(url_token: str, db: Session = Depends(get_db)):
    try:
        return PreviewPageService.show(db=db, url_token=url_token)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def get_all_pages(
    db: Session = Depends(get_db),
    current_user: dict = Depends(authenticated_user),
):
    return PreviewPageService.list(db=db, user_id=current_user["id"])


@router.delete("/{preview_id}")
async def delete_page(preview_id: int, db: Session = Depends(get_db)):
    return PreviewPageService.delete(db=db, preview_id=preview_id)
