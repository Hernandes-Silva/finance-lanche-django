from ninja import Schema
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
class ProductCreateSchema(Schema):
    name: str
    price: Decimal
    category_uuid: str
    


class ProductUpdateSchema(Schema):
    name: Optional[str] = None
    price: Optional[Decimal] = None
    category_uuid: Optional[str] = None
    active: Optional[bool] = None


class ProductSchema(Schema):
    uuid: UUID
    name: str
    price: Decimal
    active: bool
    created_at: datetime
    category_uuid: UUID
    category_name: str