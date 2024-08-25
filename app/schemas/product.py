from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    count: int


class ProductUpdate(BaseModel):
    id_product: int
    new_name: str
    new_description: str
    new_price: float
    new_count: int
