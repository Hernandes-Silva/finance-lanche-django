from .models import Product
from core.database import BaseRepository

class ProductRepository(BaseRepository):
    @staticmethod
    def create_product(category, name, price):
        return Product.objects.create(category=category, name=name, price=price)
    
    @staticmethod
    def get_products_by_store(store, category_uuid=None):
        products = Product.objects.filter(
            category__store=store,
            active=True
        ).select_related('category')
        
        if category_uuid:
            products = products.filter(category__uuid=category_uuid)
        
        return list(products)
    
    @staticmethod
    def get_product_by_uuid(uuid, store):
        try:
            return Product.objects.select_related('category').get(
                uuid=uuid,
                category__store=store
            )
        except Product.DoesNotExist:
            return None
    
    @staticmethod
    def delete_product(product):
        product.delete()