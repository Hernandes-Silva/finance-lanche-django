from ninja import NinjaAPI, Router
from ninja.errors import HttpError
from django.contrib.auth.models import User
from typing import List

from .schemas import *
from .repository import ProductRepository

from categories.repository import CategoryRepository
# from .auth import AuthBearer
# from .product_repository import Asyncproduct_repository

product_repository = ProductRepository()
category_repository = CategoryRepository()
# Auth Router
product_router = Router(tags=["Produtos"])


@product_router.post("/", response=ProductSchema)
def create_product(request, product_data: ProductCreateSchema):
    """Criar novo produto"""
    store = request.user_store
    if not store:
        raise HttpError(404, "Usuário não possui loja")
    
    category = category_repository.get_category_by_uuid(product_data.category_uuid, store)
    if not category:
        raise HttpError(404, "Categoria não encontrada")
    
    product = product_repository.create_product(
        category,
        product_data.name,
        product_data.preco
    )
    
    return {
        **product.__dict__,
        "category_uuid": str(category.uuid),
        "category_name": category.name
    }


@product_router.get("/", response=List[ProductSchema])
def list_products(request, category_uuid: str = None):
    """Listar produtos da loja do usuário"""
    store = request.user_store
    if not store:
        raise HttpError(404, "Usuário não possui loja")
    
    products = product_repository.get_products_by_store(store, category_uuid)
    
    return [
        {
            **product.__dict__,
            "category_uuid": product.category.uuid,
            "category_name": product.category.name
        }
        for product in products
    ]


@product_router.get("/{product_uuid}", response=ProductSchema)
def get_product(request, product_uuid: str):
    """Obter produto específico"""
    store = request.user_store
    if not store:
        raise HttpError(404, "Usuário não possui loja")
    
    product = product_repository.get_product_by_uuid(product_uuid, store)
    if not product:
        raise HttpError(404, "Produto não encontrado")
    
    return {
        **product.__dict__,
        "category_uuid": str(product.category.uuid),
        "category_name": product.category.name
    }


@product_router.put("/{product_uuid}", response=ProductSchema)
def update_product(request, product_uuid: str, product_data: ProductUpdateSchema):
    """Atualizar produto"""
    store = request.user_store
    if not store:
        raise HttpError(404, "Usuário não possui loja")
    
    product = product_repository.get_product_by_uuid(product_uuid, store)
    if not product:
        raise HttpError(404, "Produto não encontrado")
    
    update_data = product_data.dict(exclude_unset=True)
    
    if 'category_uuid' in update_data:
        category = product_repository.get_category_by_uuid(
            update_data.pop('category_uuid'), 
            store
        )
        if not category:
            raise HttpError(404, "Categoria não encontrada")
        product.category = category
    
    for attr, value in update_data.items():
        setattr(product, attr, value)
    
    product = product_repository.save_model(product)
    
    return {
        **product.__dict__,
        "category_uuid": str(product.category.uuid),
        "category_name": product.category.name
    }


@product_router.delete("/{product_uuid}")
def delete_product(request, product_uuid: str):
    """Deletar produto"""
    store = request.user_store
    if not store:
        raise HttpError(404, "Usuário não possui loja")
    
    product = product_repository.get_product_by_uuid(product_uuid, store)
    if not product:
        raise HttpError(404, "Produto não encontrado")
    
    product_repository.delete_product(product)
    
    return {"message": "Produto deletado com sucesso"}