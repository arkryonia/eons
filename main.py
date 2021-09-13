import jwt
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from tortoise import fields
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

from app.core.config import settings
from app.main import user_obj


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()

# class User(Model):
#     id = fields.IntField(pk=True)
#     username = fields.CharField(50, unique=True)
#     hash = fields.CharField(128)

#     @classmethod
#     async def get_user(cls, username):
#         return cls.get(username=username)

#     def verify_password(self, password):
#         return bcrypt.verify_password(password, self.hash)


# User_pydantic = pydantic_model_creator(User, name="User")
# UserIn_pydantic = pydantic_model_creator(
#     User, name="UserIn", exclude_readonly=True)

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')


# async def authenticate_user(username: str, password: str):
#     user = await User.get(username=username)
#     if not user:
#         return False
#     if not user.verify_password(hash=password):
#         return False
#     return user


# @app.post("/token")
# async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = await authenticate_user(form_data.username, form_data.password)

#     if not user:
#         return {"error": "invalid credentials"}

#     # convert user tortoise orm into pydantic model
#     user_obj = User_pydantic.from_tortoise_orm(user)

#     # Generate token
#     token = jwt.encode(user_obj.dict(), settings.JWT_SECRET)

#     return {"access_token": token, "token_type": "bearer"}


# @app.post("/", response_model=User_pydantic)
# async def create_user(user: UserIn_pydantic):
#     user_obj = User(username=user.username, hash=bcrypt.hash(user.hash))
#     await user_obj.save()
#     return await User_pydantic.from_tortoise_orm(user_obj)


@app.get("/", tags=["Index"])
def index():
    return {"Ping": "Pong"}


register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={'models': ['app.main']},
    generate_schemas=True,
    add_exception_handlers=True,
)
