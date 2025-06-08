from ninja import Schema
from typing import List
from uuid import UUID
from core.schemas import SchemaBase

class SaleItem(Schema):
    product_uuid: UUID
    quantity: int

class SaleCreateSchema(Schema):
    list_sale_items: List[SaleItem]

class HistoricSaleItem(SchemaBase):
    uuid: UUID
    name: str
    quantity: int
    price: float
    category_name: str

class DeleteResponse(Schema):
    success: bool
    message: str