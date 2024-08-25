from pydantic import BaseModel


class SaleCreate(BaseModel):
    product_id: int
    customer_id: int
    quantity: int


class SaleUpdate(BaseModel):
    id_sale: int
    product_id: int
    customer_id: int
    new_quantity: int
    new_total_price: float
