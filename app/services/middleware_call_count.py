from fastapi import Request
from app.models.async_session import get_async_session
from app.crud_operations.endpoint_call_crud import EndpointCallCrud
from fastapi import FastAPI


def register_middleware(app: FastAPI):
    """
    Register a middleware function to count endpoint calls.

    This middleware function is executed for each incoming request to the FastAPI application.
    It retrieves the current asynchronous session, extracts the endpoint name from the request URL,
    increments the call count for the endpoint using `EndpointCallCrud.increment_call_count`,
    and then passes the request to the next middleware or route handler.

    Args:
        app (FastAPI): The FastAPI application instance.

    Returns:
        None
    """
    @app.middleware('http')
    async def count_endpoint_calls(request: Request, call_next):
        """
        Middleware function to count endpoint calls.

        This function is executed for each incoming request to the FastAPI application.
        It retrieves the current asynchronous session, extracts the endpoint name from the request URL,
        increments the call count for the endpoint using `EndpointCallCrud.increment_call_count`,
        and then passes the request to the next middleware or route handler.

        Args:
            request (Request): The incoming request object.
            call_next: The next middleware or route handler to be executed.

        Returns:
            Response: The response returned by the next middleware or route handler.
        """
        async for session in get_async_session():
            endpoint_name = request.url.path
            response = await call_next(request)
            await EndpointCallCrud.increment_call_count(session, endpoint_name)
            return response
