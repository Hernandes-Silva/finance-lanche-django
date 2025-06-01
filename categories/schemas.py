from ninja import Schema
from datetime import datetime
from typing import Optional
from uuid import UUID
class CategoryCreateSchema(Schema):
    name: str


class CategoryUpdateSchema(Schema):
    name: Optional[str] = None
    active: Optional[bool] = None


class CategorySchema(Schema):
    uuid: UUID
    name: str
    active: bool
    created_at: datetime
    store_uuid: str