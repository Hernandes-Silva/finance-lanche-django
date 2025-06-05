from ninja import NinjaAPI
from authentication.api import auth_router
from categories.api import category_router
from products.api import product_router
from sales.api import sale_router
from authentication.auth import AuthBearer

auth = AuthBearer()
api = NinjaAPI(title="API de finanças de Lojas")


api.add_router("/auth", router=auth_router, tags=["Autenticação"],)
api.add_router("/categories", router=category_router, tags=["Categorias"], auth=auth)
api.add_router("/products", router=product_router, tags=["Produtos"], auth=auth)
api.add_router("/sales", router=sale_router, tags=["Vendas"], auth=auth)
