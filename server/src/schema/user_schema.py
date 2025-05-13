from pydantic import BaseModel

class UserUpdate(BaseModel):
    username: str | None = None 
    email: str | None = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str