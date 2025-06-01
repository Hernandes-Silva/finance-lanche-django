from django.contrib.auth.models import User
from .models import Category
from core.database import BaseRepository

class CategoryRepository(BaseRepository):
    @staticmethod
    def create_category(store, name):
        return Category.objects.create(store=store, name=name)

    @staticmethod
    def get_categories_by_store(store):
        return list(Category.objects.filter(store=store, active=True))

    @staticmethod
    def get_category_by_uuid(uuid, store):
        try:
            return Category.objects.get(uuid=uuid, store=store)
        except Category.DoesNotExist:
            return None
        
    @staticmethod
    def get_or_create_category_by_name(name, store):
        return Category.objects.get_or_create(name=name, store=store)


    @staticmethod
    def delete_category(category):
        category.delete()