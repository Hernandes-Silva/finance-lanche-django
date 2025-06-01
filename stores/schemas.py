from ninja import Schema
from uuid import UUID
from datetime import datetime
from typing import Optional
from core.schemas import SchemaBase

class StoreCreateSchema(Schema):
    name: str


class StoreUpdateSchema(Schema):
    name: Optional[str] = None
    active: Optional[bool] = None


class StoreSchema(SchemaBase):
    uuid: UUID
    name: str
    active: bool
    created: datetime