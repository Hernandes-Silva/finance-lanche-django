from ninja import Schema
from typing import Optional
from stores.schemas import StoreSchema
from core.schemas import SchemaBase


class LoginSchema(Schema):
    username: str
    password: str

class TokenSchema(Schema):
    access_token: str
    token_type: str = "bearer"

class UserCreateSchema(Schema):
    username: str
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserSchema(SchemaBase):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str

class AuthSchema(SchemaBase):
    user: Optional[UserSchema] = None
    store: Optional[StoreSchema] = None