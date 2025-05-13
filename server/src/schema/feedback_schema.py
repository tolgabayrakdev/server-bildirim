from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import enum

class FeedbackType(str, enum.Enum):
    complaint = "complaint"
    suggestion = "suggestion"
    request = "request"
    compliment = "compliment"

class FeedbackBase(BaseModel):
    content: str
    feedback_type: FeedbackType
    feedback_page_id: int
    customer_email: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackUpdate(FeedbackBase):
    pass

class FeedbackResponse(FeedbackBase):
    id: int
    created_at: datetime

