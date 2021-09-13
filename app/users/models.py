from tortoise.models import Model
from tortoise import fields

from tortoise.contrib.pydantic import pydantic_model_creator
from passlib.hash import bcrypt

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    hash = fields.CharField(128)

    @classmethod
    async def get_user(cls, username):
        return cls.get(username=username)

    def verify_password(self, password):
        return bcrypt.verify(password, self.hash)

UserPydantic = pydantic_model_creator(User, name="User")
UserInPydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)