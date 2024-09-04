from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.endpoint_call import EndpointCall


class EndpointCallCrud:

    @staticmethod
    async def increment_call_count(session: AsyncSession, endpoint_name: str):
        """
        Increment the call count for a given endpoint.

        If the endpoint does not exist, it creates a new record with a call count of 1.
        If the endpoint already exists, it increments the call count by 1.

        Args:
            session (AsyncSession): Asynchronous SQLAlchemy session used for database operations.
            endpoint_name (str): The name of the endpoint whose call count is to be incremented.

            Returns:
                None
        """
        result = await session.execute(select(EndpointCall).filter_by(endpoint_name=endpoint_name))
        endpoint_call = result.scalars().first()

        if not endpoint_call:
            endpoint_call = EndpointCall(endpoint_name=endpoint_name, call_count=1)
            session.add(endpoint_call)
        else:
            endpoint_call.call_count += 1

        await session.commit()
        await session.refresh(endpoint_call)

    @classmethod
    async def get_calls_endpoints_count(cls, skip: int, limit: int, session: AsyncSession):
        """
        Retrieve a paginated list of endpoint call records.

        This method fetches a specified number of endpoint call records, skipping a given number.

        Args:
            skip (int): The number of records to skip (for pagination).
            limit (int): The maximum number of records to return.
            session (AsyncSession): Asynchronous SQLAlchemy session used for database operations.

        Returns:
            list: A list of `EndpointCall` objects.
        """
        result = await session.execute(select(EndpointCall).order_by(EndpointCall.id).offset(skip).limit(limit))
        get_calls_count = result.scalars().all()
        return get_calls_count
