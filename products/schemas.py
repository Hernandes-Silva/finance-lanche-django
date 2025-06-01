from ninja import Schema
from datetime import datetime
from decimal import Decimal
from typing import Optional

class ProductCreateSchema(Schema):
    name: str
    preco: Decimal
    category_uuid: str
    


class ProductUpdateSchema(Schema):
    name: Optional[str] = None
    preco: Optional[Decimal] = None
    category_uuid: Optional[str] = None
    active: Optional[bool] = None


class ProductSchema(Schema):
    uuid: str
    name: str
    preco: Decimal
    active: bool
    created_at: datetime
    category_uuid: str
    category_name: str