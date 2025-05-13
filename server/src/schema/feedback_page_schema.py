from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime



class FeedbackPageCreate(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=10)


class FeedbackPageUpdate(BaseModel):
    title: Optional[str] = None 
    description: Optional[str] = None
