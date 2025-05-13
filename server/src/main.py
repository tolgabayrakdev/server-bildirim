from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import (
    authentication_router,
    user_router,
    feedback_page_router,
    preview_page_router,
    user_feedback_router,
    feedback_router,
    feedback_statics_router,
)
from . import model
from .database import engine


model.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://localhost:5173", "https://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=authentication_router.router, prefix="/api/auth")
app.include_router(router=user_router.router, prefix="/api/user")
app.include_router(router=feedback_page_router.router, prefix="/api/feedback-page")
app.include_router(router=preview_page_router.router, prefix="/api/preview-page")
app.include_router(router=user_feedback_router.router, prefix="/api/user-feedback")
app.include_router(router=feedback_router.router, prefix="/api/feedback")
app.include_router(router=feedback_statics_router.router, prefix="/api/feedback-statics")


@app.get("/")
def read_root():
    return {"Hello": "World"}
