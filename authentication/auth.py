from ninja.security import HttpBearer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpRequest
from asgiref.sync import sync_to_async

from .schemas import AuthSchema
from stores.repository import StoreRepository

class AuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str):
        print("entrouu aqui")
        """Autenticação"""
        try:
            user_id = int(token)
            user = User.objects.get(id=user_id, is_active=True)
            store = StoreRepository.get_user_store(user)
            request.user_store = store
            return user
        except (ValueError, User.DoesNotExist):
            return None
