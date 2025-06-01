
from ninja import NinjaAPI, Router
from ninja.errors import HttpError
from django.contrib.auth.models import User
from typing import List

from .repository import CategoryRepository
from .schemas import *
from stores.repository import StoreRepository


category_router = Router()
category_reposiory = CategoryRepository()
store_repository = StoreRepository()

@category_router.post("/", response=CategorySchema)
def create_category(request, category_data: CategoryCreateSchema):
    """Criar nova categoria"""
    store = request.user_store
    if not store:
        raise HttpError(404, "Usuário não possui loja")
    
    category = category_reposiory.create_category(store, category_data.name)
    
    return {
        **category.__dict__,
        "store_uuid": str(store.uuid)
    }


@category_router.get("/", response=List[CategorySchema])
def list_categories(request):
    """Listar categorias da loja do usuário"""
    store = request.user_store
    if not store:
        raise HttpError(404, "Usuário não possui loja")
    
    categories = category_reposiory.get_categories_by_store(store)
    
    return [
        {
            **category.__dict__,
            "store_uuid": str(store.uuid)
        }
        for category in categories
    ]


@category_router.get("/{category_uuid}", response=CategorySchema)
def get_category(request, category_uuid: str):
    """Obter categoria específica """
    store = request.user_store
    if not store:
        raise HttpError(404, "Usuário não possui loja")
    
    category = category_reposiory.get_category_by_uuid(category_uuid, store)
    if not category:
        raise HttpError(404, "Categoria não encontrada")
    
    return {
        **category.__dict__,
        "store_uuid": str(store.uuid)
    }


@category_router.put("/{category_uuid}", response=CategorySchema)
def update_category(request, category_uuid: str, category_data: CategoryUpdateSchema):
    """Atualizar categoria """
    store = request.user_store
    if not store:
        raise HttpError(404, "Usuário não possui loja")
    
    category = category_reposiory.get_category_by_uuid(category_uuid, store)
    if not category:
        raise HttpError(404, "Categoria não encontrada")
    
    for attr, value in category_data.dict(exclude_unset=True).items():
        setattr(category, attr, value)
    
    category = category_reposiory.save_model(category)
    
    return {
        **category.__dict__,
        "store_uuid": str(store.uuid)
    }


@category_router.delete("/{category_uuid}")
def delete_category(request, category_uuid: str):
    """Deletar categoria """
    store = request.user_store
    if not store:
        raise HttpError(404, "Usuário não possui loja")
    
    category =  category_reposiory.get_category_by_uuid(category_uuid, store)
    if not category:
        raise HttpError(404, "Categoria não encontrada")
    
    category_reposiory.delete_category(category)
    
    return {"message": "Categoria deletada com sucesso"}