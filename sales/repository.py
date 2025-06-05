from .models import Sale, SaleItem
from core.database import BaseRepository
from .schemas import SaleCreateSchema, HistoricSaleItem
from django.db.models import Sum

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
    def get_sale_items_by_store(store):
        items = (
            SaleItem.objects
            .filter(sale__store=store)
            .values('product_id', 'product__name', 'product__price', 'product__category__name')
            .annotate(total_quantity=Sum('quantity'))
        )

        return [
            HistoricSaleItem(
                    uuid=item["product_id"],
                    name=item["product__name"],            
                    quantity=item["total_quantity"], 
                    price=item["product__price"], 
                    category=item["product__category__name"]
            ) for item in items
        ]
    
    @staticmethod
    def remove_1_quantity_in_any_sale_item_by_product_uuid(product_uuid, store):
        produto = product_repository.get_product_by_uuid(uuid=product_uuid, store=store)

        last_item = (
            SaleItem.objects
            .filter(product=produto, sale__store=store)
            .order_by('-created_at')  # pode usar '-id' também
            .first()
        )

        if not last_item:
            return {"success": False, "message": "Nenhuma venda encontrada para esse produto."}

        if last_item.quantity > 1:
            last_item.quantity -= 1
            last_item.save()
            return {"success": True, "message": "Quantidade reduzida em 1."}
        else:
            # quantity == 1, então deletamos o item
            sale = last_item.sale
            can_remove_sale =  False if len(sale.items.all()) > 1 else True
            last_item.delete()
            
            if can_remove_sale:
                sale.delete()

            return {"success": True, "message": "Último item removido, SaleItem excluído."}