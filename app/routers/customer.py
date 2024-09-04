from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.async_session import get_async_session
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.crud_operations.customer_crud import CustomerCrud

customer_router = APIRouter(
    prefix='/customers', tags=['customer']
)


@customer_router.get('/get/')
async def get_customers(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)):
    get_all_products = await CustomerCrud.get_all_customers(skip=skip, limit=limit, session=session)
    return get_all_products


@customer_router.post('/add/')
async def create_customer(customer: CustomerCreate, session: AsyncSession = Depends(get_async_session)):
    new_customer = await CustomerCrud.post_new_customer(customer, session)
    return new_customer


@customer_router.delete('/delete_customer/{customer_id}/')
async def delete_customer(customer_id: int, session: AsyncSession = Depends(get_async_session)):
    deleted_customer = await CustomerCrud.delete_customer(customer_id, session)
    return deleted_customer


@customer_router.patch('/update_customer/')
async def update_customer(customer: CustomerUpdate, session: AsyncSession = Depends(get_async_session)):
    updated_customer = await CustomerCrud.update_customer(customer, session)
    return updated_customer
