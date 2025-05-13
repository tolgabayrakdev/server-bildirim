from sqlalchemy.orm import Session
from ..schema.preview_page_schema import PreviewPageCreate, PreviewPageUpdate, PreviewPageResponse
from ..model import PreviewPage, User, FeedbackPage
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from datetime import timedelta, datetime
import uuid


class PreviewPageService:

    @staticmethod
    def create(db: Session, payload: PreviewPageCreate, user_id: int):
        try:
            # Kullanıcının mevcut preview sayfa sayısını kontrol et
            existing_previews = db.query(PreviewPage).filter(PreviewPage.user_id == user_id).count()
            if existing_previews >= 3:
                raise HTTPException(status_code=400, detail="You have reached the maximum number of preview pages (3).")

            expires_at = datetime.now() + timedelta(days=30)
            preview = PreviewPage(
                title=payload.title,
                description=payload.description,
                url_token=uuid.uuid4().hex,
                logo_url=payload.logo_url,
                gradient=payload.gradient,
                font=payload.font,
                expires_at=expires_at,
                user_id=user_id,
                feedback_page_id=payload.feedback_page_id
            )
            db.add(preview)
            db.commit()
            db.refresh(preview)
            
            # PreviewPageResponse modeline uygun bir sözlük oluştur
            preview_dict = {
                "id": preview.id,
                "title": preview.title,
                "description": preview.description,
                "url_token": preview.url_token,
                "logo_url": preview.logo_url,
                "gradient": preview.gradient,
                "font": preview.font,
                "expires_at": preview.expires_at,
                "user_id": preview.user_id,
                "feedback_page_id": preview.feedback_page_id
            }
            
            # PreviewPageResponse modelini kullanarak doğrulama yap ve döndür
            return PreviewPageResponse(**preview_dict)
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=500, detail="An unexpected server error occurred."
            )

    @staticmethod
    def delete(db: Session, preview_id: int):
        try:
            preview = db.query(PreviewPage).filter(PreviewPage.id == preview_id).first()
            if preview:
                db.delete(preview)
                db.commit()
                return {"message": "Preview deleted"}
            else:
                raise HTTPException(status_code=404, detail="Preview not found")
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=500, detail="An unexpected server error occurred."
            )

    @staticmethod
    def update(db: Session, preview_id: int, payload: PreviewPageUpdate):
        try:
            preview = db.query(PreviewPage).filter(PreviewPage.id == preview_id).first()
            if preview:
                for key, value in payload.model_dump(exclude_unset=True).items():
                    setattr(preview, key, value)
                db.commit()
                db.refresh(preview)
                
                # PreviewPageResponse modeline uygun bir sözlük oluştur
                preview_dict = {
                    "id": preview.id,
                    "title": preview.title,
                    "description": preview.description,
                    "url_token": preview.url_token,
                    "logo_url": preview.logo_url,
                    "gradient": preview.gradient,
                    "font": preview.font,
                    "expires_at": preview.expires_at,
                    "user_id": preview.user_id,
                    "feedback_page_id": preview.feedback_page_id
                }
                
                # PreviewPageResponse modelini kullanarak doğrulama yap ve döndür
                return PreviewPageResponse(**preview_dict)
            else:
                raise HTTPException(status_code=404, detail="Preview not found")
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=500, detail="An unexpected server error occurred."
            )

    @staticmethod
    def show(db: Session, url_token: str):
        preview = (
            db.query(PreviewPage).filter(PreviewPage.url_token == url_token).first()
        )
        if preview:
            if preview.expires_at < datetime.now():  # type: ignore
                raise HTTPException(status_code=400, detail="Token has expired")
            user = db.query(User).filter(User.id == preview.user_id).first()
            feedback_page = db.query(FeedbackPage).filter(FeedbackPage.id == preview.feedback_page_id).first() if preview.feedback_page_id else None # type: ignore
            if user:
                return {
                    "id": preview.id,
                    "title": preview.title,
                    "description": preview.description,
                    "url_token": preview.url_token,
                    "expires_at": preview.expires_at,
                    "username": user.username,
                    "logo_url": preview.logo_url,
                    "gradient": preview.gradient,
                    "font": preview.font,
                    "email": user.email,
                    "feedback_page": {
                        "id": feedback_page.id,
                        "title": feedback_page.title,
                        "url_token": feedback_page.url_token
                    } if feedback_page else None
                }
            else:
                raise HTTPException(status_code=404, detail="User not found")
        raise HTTPException(status_code=404, detail="Preview not found")

    @staticmethod
    def list(db: Session, user_id: int):
        previews = db.query(PreviewPage).filter(PreviewPage.user_id == user_id).all()
        return previews
