from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.shop_models import Sale, Product


class SaleCrud:
    @classmethod
    async def get_all_sales(cls, skip: int, limit: int, session: AsyncSession):
        """
        Retrieve a paginated list of all sales.

        Args:
            skip (int): Number of records to skip (for pagination).
            limit (int): Maximum number of records to return.
            session (AsyncSession): Asynchronous SQLAlchemy session used for database operations.

        Returns:
            list: A list of `Sale` objects.
        """
        result = await session.execute(select(Sale).order_by(Sale.id).offset(skip).limit(limit))
        sales = result.scalars().all()
        return sales

    @classmethod
    async def post_new_sale(cls, sale, session: AsyncSession):
        """
        Create a new sale.

        Args:
            sale (Sale): `Sale` object containing the new sale's data.
            session (AsyncSession): Asynchronous SQLAlchemy session used for database operations.

        Returns:
            Sale: Newly created `Sale` object.

            Raises:
                ValueError: If the product associated with the sale is not found or has insufficient count.
        """
        new_sale = Sale(
            product_id=sale.product_id,
            customer_id=sale.customer_id,
            quantity=sale.quantity,
        )

        result = await session.execute(select(Product).filter(Product.id == new_sale.product_id))
        product = result.scalars().first()

        if product is None:
            raise ValueError(f"Product with id {sale.product_id} not found.")
        if product.count < sale.quantity:
            raise ValueError(f"Product with id {sale.product_id} count not enough.")

        product.count -= sale.quantity

        total_price = product.price * new_sale.quantity
        new_sale.total_price = total_price

        session.add(new_sale)
        await session.commit()
        await session.refresh(new_sale)

        return new_sale

    @classmethod
    async def delete_sale(cls, sale_id: int, session: AsyncSession):
        """
        Delete a sale by its ID.

        Args:
            sale_id (int): ID of the sale to delete.
            session (AsyncSession): Asynchronous SQLAlchemy session used for database operations.

        Returns:
            Sale: Deleted `Sale` object.

        Raises:
            ValueError: If the sale with the specified ID is not found.
        """
        result = await session.execute(select(Sale).filter(Sale.id == sale_id))
        sale = result.scalars().first()

        if sale is None:
            raise ValueError(f"Sale with id {sale_id} not found.")

        await session.delete(sale)
        await session.commit()

        return sale

    @classmethod
    async def update_sale(cls, updated_sale, session: AsyncSession):
        """
        Update the details of an existing sale.

        Args:
            updated_sale (Sale): `Sale` object containing the new data for the sale.
            session (AsyncSession): Asynchronous SQLAlchemy session used for database operations.

        Returns:
                Sale: Updated `Sale` object.

        Raises:
                ValueError: If the sale with the specified ID is not found.
        """
        result = await session.execute(select(Sale).filter(Sale.id == updated_sale.id_sale))
        existing_sale = result.scalars().first()

        if existing_sale is None:
            raise ValueError(f"Sale with id {updated_sale.id_sale} not found.")

        existing_sale.quantity = updated_sale.new_quantity
        existing_sale.total_price = updated_sale.new_total_price

        await session.commit()
        await session.refresh(existing_sale)

        return existing_sale
