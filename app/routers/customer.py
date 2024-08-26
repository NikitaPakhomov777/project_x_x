from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.session import get_session
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.crud_operations.customer_crud import CustomerCrud

customer_router = APIRouter(
    prefix='/customers', tags=['customer']
)


@customer_router.get('/get')
def get_customers(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    get_all_products = CustomerCrud.get_all_customers(skip=skip, limit=limit, session=session)
    return get_all_products


@customer_router.post('/add/')
def create_customer(customer: CustomerCreate, session: Session = Depends(get_session)):
    new_customer = CustomerCrud.post_new_customer(customer, session)
    return new_customer


@customer_router.delete('/delete_customer/')
def delete_customer(customer_id: int, session: Session = Depends(get_session)):
    deleted_customer = CustomerCrud.delete_customer(customer_id, session)
    return deleted_customer


@customer_router.patch('/update_customer/')
def update_customer(customer: CustomerUpdate, session: Session = Depends(get_session)):
    updated_customer = CustomerCrud.update_customer(customer, session)
    return updated_customer
