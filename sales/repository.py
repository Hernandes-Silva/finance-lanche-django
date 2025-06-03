from .models import Sale, SaleItem
from core.database import BaseRepository
from .schemas import SaleCreateSchema

from products.repository import ProductRepository
product_repository = ProductRepository()

class SalesRepository(BaseRepository):
    @staticmethod
    def create_sale(store, sale_create: SaleCreateSchema):
        sale = Sale.objects.create(store=store)

        for sale_item in sale_create.list_sale_items:
            SaleItem.objects.create(
                sale=sale,
                product=product_repository.get_product_by_uuid(sale_item.product_uuid, store),
                quantity=sale_item.quantity
            )
    
    @staticmethod
    def get_sales_by_store(store):
        sales = Sale.objects.filter(
            store=store,
            active=True
        )
        
        
        return list(sales)
    
    @staticmethod
    def get_sale_by_uuid(uuid, store):
        try:
            return Sale.objects.get(
                uuid=uuid,
                store=store
            )
        except Sale.DoesNotExist:
            return None
    
    @staticmethod
    def delete_sale(sale):
        sale.delete()