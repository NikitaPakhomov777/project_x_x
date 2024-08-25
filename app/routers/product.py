from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.session import get_session
from app.schemas.product import ProductCreate
from app.services.product import ProductCrud
from app.schemas.product import ProductUpdate

product_router = APIRouter(
    prefix='/products', tags=['product']
)


@product_router.get('/get')
def get_products(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    get_all_products = ProductCrud.get_all_products(skip=skip, limit=limit, session=session)
    return get_all_products


@product_router.post('/add/')
def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    new_product = ProductCrud.post_new_product(product, session)
    return new_product


@product_router.delete('/delete_product/')
def delete_product(product_id, session: Session = Depends(get_session)):
    new_product = ProductCrud.delete_product(product_id, session)
    return new_product


@product_router.patch('/update_product/')
def update_customer(product: ProductUpdate, session: Session = Depends(get_session)):
    updated_customer = ProductCrud.update_product(product, session)
    return updated_customer
