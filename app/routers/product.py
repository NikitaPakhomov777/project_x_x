from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.async_session import get_async_session
from app.schemas.product import ProductCreate, ProductUpdate
from app.crud_operations.product_crud import ProductCrud

product_router = APIRouter(
    prefix='/products', tags=['product']
)


@product_router.get('/get/')
async def get_products(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)):
    get_all_products = await ProductCrud.get_all_products(skip=skip, limit=limit, session=session)
    return get_all_products


@product_router.post('/add/')
async def create_product(product: ProductCreate, session: AsyncSession = Depends(get_async_session)):
    new_product = await ProductCrud.post_new_product(product, session)
    return new_product


@product_router.delete('/delete_product/{product_id}')
async def delete_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
    deleted_product = await ProductCrud.delete_product(product_id, session)
    return deleted_product


@product_router.patch('/update_product/')
async def update_product(product: ProductUpdate, session: AsyncSession = Depends(get_async_session)):
    updated_product = await ProductCrud.update_product(product, session)
    return updated_product
