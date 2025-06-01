from ninja import NinjaAPI
from authentication.api import auth_router
from categories.api import category_router
from authentication.auth import AuthBearer
auth = AuthBearer()
api = NinjaAPI(title="API de finanças de Lojas")


api.add_router("/auth", router=auth_router, tags=["Autenticação"],)
api.add_router("/categories", router=category_router, tags=["Categorias"], auth=auth)
