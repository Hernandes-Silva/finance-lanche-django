from ninja import NinjaAPI, Router
from ninja.errors import HttpError
from django.contrib.auth.models import User
from .schemas import *
from .auth import AuthBearer
from .repository import AuthRepository
from .jwt import create_access_token

auth = AuthBearer()
auth_repository = AuthRepository()

# Auth Router
auth_router = Router()


@auth_router.post("/register", response=UserSchema)
def register(request, user_data: UserCreateSchema):
    """Registrar novo usuário"""
    if auth_repository.user_exists_by_username(user_data.username):
        raise HttpError(400, "Username já existe")
    
    if auth_repository.user_exists_by_email(user_data.email):
        raise HttpError(400, "Email já está em uso")
    
    user = auth_repository.create_user(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        first_name=user_data.first_name or "",
        last_name=user_data.last_name or ""
    )
    
    return user


@auth_router.post("/login", response=TokenSchema)
def login_user(request, credentials: LoginSchema):
    """Login do usuário"""
    user = auth_repository.authenticate_user(
        request,
        username=credentials.username,
        password=credentials.password
    )
    
    if user is None:
        raise HttpError(401, "Credenciais inválidas")
    
    if not user.is_active:
        raise HttpError(401, "Usuário inativo")
    
    # Em produção, use JWT
    token = create_access_token({"user_id": str(user.id)})
    
    return {"access_token": token}

