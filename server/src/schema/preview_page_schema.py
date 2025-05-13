from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import Optional

class PreviewPageCreate(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=10)
    logo_url: Optional[HttpUrl] = None
    gradient: str
    font: str
    background_color: str
    text_color: str
    feedback_page_id: int  

class PreviewPageUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3)
    description: Optional[str] = Field(None, min_length=10)
    feedback_page_id: Optional[int] = None

class PreviewPageResponse(BaseModel):
    id: int
    url_token: str
    title: str
    description: str
    expires_at: datetime
    user_id: int
    feedback_page_id: int  

