from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.session import get_session
from app.schemas.sale import SaleCreate, SaleUpdate
from app.services.sale import SaleCrud

sale_router = APIRouter(
    prefix='/sales', tags=['sale']
)


@sale_router.get('/get')
def get_sales(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    get_all_sales = SaleCrud.get_all_sales(skip=skip, limit=limit, session=session)
    return get_all_sales


@sale_router.post('/add_sale/')
def create_sale(sale: SaleCreate, session: Session = Depends(get_session)):
    new_sale = SaleCrud.post_new_sale(sale, session)
    return new_sale


@sale_router.delete('/delete_sale/')
def delete_sale(sale_id, session: Session = Depends(get_session)):
    deleted_sale = SaleCrud.delete_sale(sale_id, session)
    return deleted_sale


@sale_router.patch('/update_sale')
def update_sale(sale: SaleUpdate, session: Session = Depends(get_session)):
    updated_sale = SaleCrud.update_sale(sale, session)
    return updated_sale
