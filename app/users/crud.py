import jwt 
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import bcrypt

from app.core.config import settings
from app.users.models import User, UserInPydantic, UserPydantic
from app.users.oauth2 import authenticate_user, get_current_user

users = APIRouter()



@users.post("/", response_model=UserPydantic)
async def create_user(user: UserInPydantic):
    user_obj = User(username=user.username, hash=bcrypt.hash(user.hash))
    await user_obj.save()
    return await UserPydantic.from_tortoise_orm(user_obj)

@users.get('/users/me', response_model=UserPydantic)
async def get_user(user: UserPydantic = Depends(get_current_user)):
    return user

@users.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        return {"error": "invalid credentials"}

    # convert user tortoise orm into pydantic model
    user_obj = await UserPydantic.from_tortoise_orm(user)

    # Generate token
    token = jwt.encode(user_obj.dict(), settings.JWT_SECRET)

    return {"access_token": token, "token_type": "bearer"}
