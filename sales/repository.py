from .models import Sale, SaleItem
from core.database import BaseRepository
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncYear
from .schemas import SaleCreateSchema, HistoricSaleItem, LineChatFilterType, ResponseLineChartType
from django.db.models import Sum, F
from datetime import date, timedelta

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
    def get_sale_items_by_store(store, sale_date: date = None):
        sales = Sale.objects.filter(store=store)

        if sale_date:
            sales = sales.filter(sold_at__date=sale_date)

        items = (
            SaleItem.objects
            .filter(sale__in=sales)
            .values('product_id', 'product__name', 'product__price', 'product__category__name')
            .annotate(total_quantity=Sum('quantity'))
        )

        return [
            HistoricSaleItem(
                    uuid=item["product_id"],
                    name=item["product__name"],            
                    quantity=item["total_quantity"], 
                    price=item["product__price"], 
                    category_name=item["product__category__name"]
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
    
    @staticmethod
    def get_sales_by_date_and_type(store, start_date: date, end_date: date, type_filter: LineChatFilterType):
        trunc_func = {
            LineChatFilterType.day: TruncDay,
            LineChatFilterType.week: TruncWeek,
            LineChatFilterType.month: TruncMonth,
            LineChatFilterType.year: TruncYear,
        }[type_filter]

        sale_items = (
            SaleItem.objects
            .filter(
                sale__store=store,
                sale__sold_at__range=[start_date, end_date+timedelta(days=1)]
            )
            .annotate(period=trunc_func('sale__sold_at'))
            .values('period')
            .annotate(
                numberProductsSales=Sum('quantity'),
                valueProductsSales=Sum(F('quantity') * F('product__price'))
            )
            .order_by('period')
        )

        result = []
        for item in sale_items:
            period = item['period']
            if type_filter == LineChatFilterType.day:
                label = period.strftime("%d/%m")
            elif type_filter == LineChatFilterType.week:
                label = period.strftime("%d/%m")  # semana começa nesse dia
            elif type_filter == LineChatFilterType.month:
                label = period.strftime("Mês %m")
            else:  # year
                label = period.strftime("Ano %Y")

            result.append(ResponseLineChartType(
                label=label,
                numberProductsSales=item['numberProductsSales'],
                valueProductsSales=item['valueProductsSales']
            ))

        return result