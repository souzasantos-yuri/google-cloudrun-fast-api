from pydantic import BaseModel
from decimal import Decimal

class Message(BaseModel):
    message: str

class CustomerRevenueOut(BaseModel):
    cd_customer: str
    vl_revenue: Decimal