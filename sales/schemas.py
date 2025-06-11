from ninja import Schema
from typing import List
from uuid import UUID
from core.schemas import SchemaBase
from enum import Enum
from datetime import date

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

class LineChatFilterType(str, Enum):
    day = 'day'
    month = 'month'
    year = 'year'

class LineChartRequest(Schema):
    start_date: date
    end_date: date
    filter_type: LineChatFilterType

class ResponseLineChartType(Schema):
    label: str
    numberProductsSales: int
    valueProductsSales: float

class InitDateAndEndDateRequest(Schema):
    start_date: date
    end_date: date

class BarChartRequest(InitDateAndEndDateRequest):
    ...

class PieChartRequest(InitDateAndEndDateRequest):
    ...

class ResponseBarChartType(Schema):
    productName: str
    numberProductsSales: int
    valueProductsSales: float
    percentageProductsSales: float

class ResponsePieChartType(Schema):
    categoryName: str
    numberProductsSales: int
    valueProductsSales: float
    percentageProductsSales: float