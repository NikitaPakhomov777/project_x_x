from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.async_session import get_async_session
from app.crud_operations.endpoint_call_crud import EndpointCallCrud

endpoint_calls_router = APIRouter(
    prefix='/endpoints', tags=['endpoints']
)


@endpoint_calls_router.get('/get_calls_count/')
async def get_calls_count(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)):
    get_all_calls = await EndpointCallCrud.get_calls_endpoints_count(skip=skip, limit=limit, session=session)
    return get_all_calls
