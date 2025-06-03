from ninja import Schema
from datetime import datetime
from typing import Optional, List
from uuid import UUID

class SaleItem(Schema):
    product_uuid: UUID
    quantity: int

class SaleCreateSchema(Schema):
    list_sale_items: List[SaleItem]

class CategoryUpdateSchema(Schema):
    name: Optional[str] = None
    active: Optional[bool] = None


class CategorySchema(Schema):
    uuid: UUID
    name: str
    active: bool
    created_at: datetime
    store_uuid: str