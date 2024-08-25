from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: str


class CustomerUpdate(BaseModel):
    id_customer: int
    new_name: str
    new_email: EmailStr
    new_phone: str
