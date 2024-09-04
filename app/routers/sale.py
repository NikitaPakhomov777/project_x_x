from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.async_session import get_async_session
from app.schemas.sale import SaleCreate, SaleUpdate
from app.crud_operations.sale_crud import SaleCrud

sale_router = APIRouter(
    prefix='/sales', tags=['sale']
)


@sale_router.get('/get/')
async def get_sales(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)):
    get_all_sales = await SaleCrud.get_all_sales(skip=skip, limit=limit, session=session)
    return get_all_sales


@sale_router.post('/add/')
async def create_sale(sale: SaleCreate, session: AsyncSession = Depends(get_async_session)):
    new_sale = await SaleCrud.post_new_sale(sale, session)
    return new_sale


@sale_router.delete('/delete_sale/{sale_id}')
async def delete_sale(sale_id: int, session: AsyncSession = Depends(get_async_session)):
    deleted_sale = await SaleCrud.delete_sale(sale_id, session)
    return deleted_sale


@sale_router.patch('/update_sale/')
async def update_sale(sale: SaleUpdate, session: AsyncSession = Depends(get_async_session)):
    updated_sale = await SaleCrud.update_sale(sale, session)
    return updated_sale
