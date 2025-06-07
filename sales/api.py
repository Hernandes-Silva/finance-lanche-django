from ninja import NinjaAPI, Router
from ninja.errors import HttpError
from ninja.responses import Response
from django.contrib.auth.models import User
from typing import List, Dict

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
    
    sale_items = []
    for sale_item in payload.list_sale_items:
        sale_items.append({
            "product": product_repository.get_product_by_uuid(sale_item.product_uuid, store),
            "quantity": sale_item.quantity
        })

    sales_repository.create_sale(store, sale_items=sale_items)
    
    return Response({"message": "Venda registrada com sucesso!"}, status=201)

@sale_router.get("/historic", response=List[HistoricSaleItem])
def get_historic_sales(request):
    """pegar historico de vendas"""
    store = request.user_store
    if not store:
        raise HttpError(404, "Usuário não possui loja")
    
    return sales_repository.get_sale_items_by_store(store)


@sale_router.delete("/remove/{product_uuid}", response=DeleteResponse)
def remove_product_in_sale_item(request, product_uuid: str):
    """Deletar um produto do um historico de vendas"""
    store = request.user_store
    if not store:
        raise HttpError(404, "Usuário não possui loja")
    
    response = sales_repository.remove_1_quantity_in_any_sale_item_by_product_uuid(store=store, product_uuid=product_uuid)

    return response