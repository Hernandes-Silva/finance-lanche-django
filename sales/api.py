from ninja import NinjaAPI, Router, Query
from ninja.errors import HttpError
from ninja.responses import Response
from django.contrib.auth.models import User
from typing import List, Dict, Optional
from datetime import date

from .schemas import *
from .repository import SalesRepository

from categories.repository import CategoryRepository
from products.repository import ProductRepository
# from .auth import AuthBearer
# from .product_repository import Asyncproduct_repository

sales_repository = SalesRepository()
category_repository = CategoryRepository()
product_repository = ProductRepository()
# Auth Router
sale_router = Router()


@sale_router.post("/")
def create_sale(request, payload: SaleCreateSchema):
    """Registrar nova venda"""
    store = request.user_store
    if not store:
        raise HttpError(404, "Usuário não possui loja")
    
    sales_repository.create_sale(store, sale_create=payload)
    
    return Response({"message": "Venda registrada com sucesso!"}, status=201)

@sale_router.get("/historic", response=List[HistoricSaleItem])
def get_historic_sales(request, sale_date: Optional[date] = Query(None)):
    """pegar historico de vendas"""
    store = request.user_store
    if not store:
        raise HttpError(404, "Usuário não possui loja")
    
    return sales_repository.get_sale_items_by_store(store, sale_date=sale_date)


@sale_router.delete("/remove/product/{product_uuid}", response=DeleteResponse)
def remove_product_in_sale_item(request, product_uuid: str):
    """Deletar um produto do um historico de vendas"""
    store = request.user_store
    if not store:
        raise HttpError(404, "Usuário não possui loja")
    
    response = sales_repository.remove_1_quantity_in_any_sale_item_by_product_uuid(store=store, product_uuid=product_uuid)

    return response


@sale_router.post("/chart/line", response=List[ResponseLineChartType])
def get_line_chart_data(request, data: LineChartRequest):
    store = request.user_store
    if not store:
        raise HttpError(404, "Loja não encontrada")

    response = sales_repository.get_sales_by_date_and_type(store, data.start_date, data.end_date, data.filter_type)

    return response

@sale_router.post("/chart/bar", response=List[ResponseBarChartType])
def get_bar_chart_data(request, data: BarChartRequest):
    store = request.user_store
    if not store:
        raise HttpError(404, "Loja não encontrada")

    response = sales_repository.get_sales_by_range_date(store, data.start_date, data.end_date)

    return response