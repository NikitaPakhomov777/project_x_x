from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.session import get_session
from app.crud_operations.endpoint_call_crud import EndpointCallCrud

endpoint_calls_router = APIRouter(
    prefix='/endpoints', tags=['endpoints']
)


@endpoint_calls_router.get('/get_calls_count')
def get_calls_count(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    get_all_calls = EndpointCallCrud.get_calls_endpoints_count(skip=skip, limit=limit, session=session)
    return get_all_calls
