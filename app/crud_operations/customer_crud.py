from app.models.shop_models import Customer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class CustomerCrud:
    @classmethod
    async def get_all_customers(cls, skip: int, limit: int, session: AsyncSession):
        """
        Retrieve a paginated list of all customers.

        Args:
            skip (int): Number of records to skip (for pagination).
            limit (int): Maximum number of records to return.
            session (AsyncSession): Asynchronous SQLAlchemy session.

        Returns:
            list: List of `Customer` objects.
        """
        result = await session.execute(select(Customer).order_by(Customer.id).offset(skip).limit(limit))
        customers = result.scalars().all()
        return customers

    @classmethod
    async def post_new_customer(cls, customer, session: AsyncSession):
        """
        Create a new customer.

        Args:
            customer (Customer): `Customer` object containing the new customer's data.
            session (AsyncSession): Asynchronous SQLAlchemy session.

        Returns:
            Customer: Newly created `Customer` object.
        """
        new_customer = Customer(
            name=customer.name,
            email=customer.email,
            phone=customer.phone
        )

        session.add(new_customer)
        await session.commit()
        await session.refresh(new_customer)

        return new_customer

    @classmethod
    async def delete_customer(cls, customer_id: int, session: AsyncSession):
        """
        Delete a customer by their ID.

        Args:
            customer_id (int): ID of the customer to delete.
            session (AsyncSession): Asynchronous SQLAlchemy session.

        Returns:
            Customer: Deleted `Customer` object.

        Raises:
            ValueError: If the customer with the specified ID is not found.
        """
        result = await session.execute(select(Customer).filter(Customer.id == customer_id))
        customer = result.scalars().first()

        if customer is None:
            raise ValueError(f"Customer with id {customer_id} not found.")

        await session.delete(customer)
        await session.commit()

        return customer

    @classmethod
    async def update_customer(cls, updated_customer, session: AsyncSession):
        """
        Update the details of an existing customer.

        Args:
            updated_customer (Customer): `Customer` object containing the new data for the customer.
            session (AsyncSession): Asynchronous SQLAlchemy session.

        Returns:
            Customer: Updated `Customer` object.

            Raises:
            ValueError: If the customer with the specified ID is not found.
        """
        result = await session.execute(select(Customer).filter(Customer.id == updated_customer.id_customer))
        existing_customer = result.scalars().first()
        if existing_customer is None:
            raise ValueError(f"Customer with id {updated_customer.id_customer} not found.")

        existing_customer.name = updated_customer.new_name
        existing_customer.email = updated_customer.new_email
        existing_customer.phone = updated_customer.new_phone
        await session.commit()
        await session.refresh(existing_customer)

        return existing_customer
