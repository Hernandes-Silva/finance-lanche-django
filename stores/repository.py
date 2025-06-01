from .models import Store
from core.database import BaseRepository
class StoreRepository(BaseRepository):
    @staticmethod
    def has_store(user):
        return hasattr(user, 'store')
    
    @staticmethod
    def create_store(user, name):
        return Store.objects.create(user=user, name=name)
    
    @staticmethod
    def get_user_store(user):
        try:
            return user.store
        except Store.DoesNotExist:
            return None
