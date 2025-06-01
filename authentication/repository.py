from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from core.database import BaseRepository

class AuthRepository(BaseRepository):
    @staticmethod
    def create_user(**kwargs):
        return User.objects.create_user(**kwargs)

    @staticmethod
    def user_exists_by_username(username):
        return User.objects.filter(username=username).exists()

    @staticmethod
    def user_exists_by_email(email):
        return User.objects.filter(email=email).exists()

    @staticmethod
    def authenticate_user(request, username, password):
        return authenticate(request, username=username, password=password)