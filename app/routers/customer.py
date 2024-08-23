from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.session import get_session
from app.schemas.product import ProductCreate, ProductRead
from app.services.product import ProductCrud

product_router = APIRouter(
    prefix='/customers', tags=['customer']
)

