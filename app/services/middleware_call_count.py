from fastapi import Request
from sqlalchemy.orm import Session
from app.models.session import get_session
from app.crud_operations.endpoint_call_crud import EndpointCallCrud


def count_endpoint_calls(request: Request, call_next):
    session: Session = next(get_session())
    response = call_next(request)

    endpoint_name = request.url.path
    EndpointCallCrud.increment_call_count(session, endpoint_name)

    return response
