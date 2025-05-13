from .database import Base
from sqlalchemy import Integer, String, Column, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum


class SubscriptionPlan(enum.Enum):
    free = "free"
    pro = "pro"


class FeedbackType(enum.Enum):
    complaint = "complaint"  # Şikayet
    suggestion = "suggestion"  # Öneri
    request = "request"  # İstek
    compliment = "compliment"  # Tebrik


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("roles.id"), default=1)
    created_at = Column(DateTime, default=datetime.now())
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.free)

    # İlişki ekleniyor
    #feedback_pages = relationship("FeedbackPage", back_populates="owner")


class FeedbackPage(Base):
    __tablename__ = "feedback_pages"

    id = Column(Integer, primary_key=True, index=True)
    url_token = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    expires_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    #owner = relationship("User", back_populates="feedback_pages")
    #feedbacks = relationship("Feedback", back_populates="feedback_page", cascade="all, delete-orphan")


class PreviewPage(Base):
    __tablename__ = "preview_pages"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    url_token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime)
    logo_url = Column(String, nullable=True)
    gradient = Column(String)
    font = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    background_color = Column(String)
    feedback_page_id = Column(Integer, ForeignKey("feedback_pages.id"))

    #feedback_page = relationship("FeedbackPage", back_populates="preview_pages")


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    feedback_type = Column(Enum(FeedbackType), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    feedback_page_id = Column(Integer, ForeignKey("feedback_pages.id"), nullable=False)
    customer_email = Column(String, nullable=True)

    #feedback_page = relationship("FeedbackPage", back_populates="feedbacks")
