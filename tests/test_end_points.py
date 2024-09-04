import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud_operations.endpoint_call_crud import EndpointCallCrud
from app.models.endpoint_call import EndpointCall
from sqlalchemy import select


@pytest.mark.asyncio
async def test_increment_call_count(session: AsyncSession):
    """
    Test the `increment_call_count` method of `EndpointCallCrud`.

    This test checks that the call count is incremented correctly for an endpoint.
        If the endpoint does not exist, it should be created with an initial call count of 1.

    Args:
        session (AsyncSession): Asynchronous SQLAlchemy session used for database operations.
    """
    endpoint_name = "test_endpoint"

    await EndpointCallCrud.increment_call_count(session, endpoint_name)

    result = await session.execute(select(EndpointCall).filter_by(endpoint_name=endpoint_name))
    endpoint_call = result.scalars().first()
    assert endpoint_call is not None
    assert endpoint_call.call_count == 1

    await EndpointCallCrud.increment_call_count(session, endpoint_name)

    result = await session.execute(select(EndpointCall).filter_by(endpoint_name=endpoint_name))
    endpoint_call = result.scalars().first()
    assert endpoint_call.call_count == 2


@pytest.mark.asyncio
async def test_get_calls_endpoints_count(session: AsyncSession):
    """
    Test the `get_calls_endpoints_count` method of `EndpointCallCrud`.

    This test checks that the method returns the expected list of endpoint call records
        based on the provided `skip` and `limit` parameters.

    Args:
        session (AsyncSession): Asynchronous SQLAlchemy session used for database operations.
    """
    await EndpointCallCrud.increment_call_count(session, "endpoint_1")
    await EndpointCallCrud.increment_call_count(session, "endpoint_2")
    await EndpointCallCrud.increment_call_count(session, "endpoint_3")

    calls = await EndpointCallCrud.get_calls_endpoints_count(skip=0, limit=10, session=session)

    assert len(calls) == 4

    assert calls[1].endpoint_name == "endpoint_1"
    assert calls[2].endpoint_name == "endpoint_2"
    assert calls[3].endpoint_name == "endpoint_3"
