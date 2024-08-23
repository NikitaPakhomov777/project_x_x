from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    count: int


class ProductRead(BaseModel):
    id: int
    name: str
    description: str
    price: float
    count: int

    class Config:
        orm_mode = True
