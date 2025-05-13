from fastapi import APIRouter, Response, Request, HTTPException, Depends
from ..service.authentication_service import AuthenticationService
from ..schema.authentication_schema import LoginSchema, RegisterSchema
from sqlalchemy.orm import Session
from ..database import get_db
import jwt
from ..util.helper import Helper
from typing import Dict

router = APIRouter()
helper = Helper()


@router.post("/login")
async def login(user: LoginSchema, response: Response, db: Session = Depends(get_db)):
    result = AuthenticationService.login(
        email=user.email, password=user.password, db=db
    )
    response.set_cookie(key="access_token", value=result["access_token"], httponly=True)
    response.set_cookie(
        key="refresh_token", value=result["refresh_token"], httponly=True
    )
    return {"message": "Login is successful."}


@router.post("/register", status_code=201)
async def register(user: RegisterSchema, db: Session = Depends(get_db)):
    return AuthenticationService.register(payload=user, db=db)


@router.post("/verify", status_code=200)
async def verify_user(request: Request, db: Session = Depends(get_db)):
    try:
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        if access_token and refresh_token:
            user_id = helper.decode_jwt(token=access_token)
            result = AuthenticationService.verify_user(user_id, db=db)

            if result:
                return {
                    "success": True,
                    "user": {"username": result.username, "email": result.email},
                }
            else:
                raise HTTPException(status_code=404, detail="User not found")
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Access token has expired.")
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=400, detail="Invalid token: " + str(e))


@router.post("/logout")
async def logout(response: Response) -> Dict[str, str]:
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "You are logged out."}
