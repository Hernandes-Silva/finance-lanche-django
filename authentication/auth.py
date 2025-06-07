from ninja.security import HttpBearer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from ninja.errors import HttpError
from django.http import HttpRequest
from asgiref.sync import sync_to_async

from .schemas import AuthSchema
from .jwt import verify_token
from stores.repository import StoreRepository


class AuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str):
        payload = verify_token(token)
        if not payload or "user_id" not in payload:
            raise HttpError(401, "Invalid token or expired token")
        try:
            user_id = payload["user_id"]
            user = User.objects.get(id=user_id, is_active=True)
            store = StoreRepository.get_user_store(user)
            request.user_store = store
            return user
        except (ValueError, User.DoesNotExist):
            raise HttpError(401, "User not found")