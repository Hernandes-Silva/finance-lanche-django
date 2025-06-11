from .models import Sale, SaleItem
from core.database import BaseRepository
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncYear, Coalesce
from .schemas import SaleCreateSchema, HistoricSaleItem, LineChatFilterType, ResponseLineChartType, ResponseBarChartType, ResponsePieChartType
from django.db.models import Sum, F, DecimalField
from datetime import date, timedelta
from decimal import Decimal

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

        sales_by_period = {item['period'].date(): item for item in sale_items}

        result = []
        current = start_date

        def get_label(dt: date) -> str:
            if type_filter == LineChatFilterType.day:
                return dt.strftime("%d/%m")
            elif type_filter == LineChatFilterType.month:
                return f"{dt.month}/{str(dt.year)[-2:]}"
            else:  # year
                return f"{dt.year}"

        def increment(dt: date):
            if type_filter == LineChatFilterType.day:
                return dt + timedelta(days=1)
            elif type_filter == LineChatFilterType.month:
                return (dt.replace(day=1) + timedelta(days=32)).replace(day=1)
            else:  # year
                return dt.replace(month=1, day=1).replace(year=dt.year + 1)

        while current <= end_date:
            found = sales_by_period.get(current)
            number = found['numberProductsSales'] if found else 0
            value = found['valueProductsSales'] if found else 0

            result.append(ResponseLineChartType(
                label=get_label(current),
                numberProductsSales=number,
                valueProductsSales=value,
            ))

            current = increment(current)

        return result


    @staticmethod
    def get_sales_by_range_date(store, start_date: date, end_date: date):
        sales_items = (
            SaleItem.objects
            .filter(
                sale__store=store,
                sale__sold_at__date__range=[start_date, end_date]
            )
            .values('product__name')
            .annotate(
                numberProductsSales=Coalesce(Sum('quantity'), 0),
                valueProductsSales=Coalesce(
                    Sum(F('quantity') * F('product__price'), output_field=DecimalField()),
                    Decimal('0.00')
                )
            )
            .order_by('-numberProductsSales')
        )

        total_value = sum(item['numberProductsSales'] for item in sales_items) or Decimal('1.00')

        result = []
        for item in sales_items:
            result.append(ResponseBarChartType(
                productName=item['product__name'],
                numberProductsSales=item['numberProductsSales'],
                valueProductsSales=float(item['valueProductsSales']),
                percentageProductsSales=round((item['numberProductsSales'] / total_value) * 100, 2)
            ))

        return result
    
    @staticmethod
    def get_categories_sales_by_range_date(store, start_date: date, end_date: date):
        sales_items = (
            SaleItem.objects
            .filter(
                sale__store=store,
                sale__sold_at__date__range=[start_date, end_date]
            )
            .values('product__category__name')
            .annotate(
                numberProductsSales=Coalesce(Sum('quantity'), 0),
                valueProductsSales=Coalesce(
                    Sum(F('quantity') * F('product__price'), output_field=DecimalField()),
                    Decimal('0.00')
                )
            )
            .order_by('-numberProductsSales')
        )

        total_value = sum(item['numberProductsSales'] for item in sales_items) or Decimal('1.00')


        result = []
        for item in sales_items:
            result.append(ResponsePieChartType(
                categoryName=item['product__category__name'],
                numberProductsSales=item['numberProductsSales'],
                valueProductsSales=item['valueProductsSales'],
                percentageProductsSales=round((item['numberProductsSales'] / total_value) * 100, 2)
            ))

        return result