from app.models.shop_models import Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class ProductCrud:
    @classmethod
    async def get_all_products(cls, skip: int, limit: int, session: AsyncSession):
        """
        Retrieve a paginated list of all products.

        Args:
            skip (int): Number of records to skip (for pagination).
            limit (int): Maximum number of records to return.
            session (AsyncSession): Asynchronous SQLAlchemy session used for database operations.

        Returns:
            list: A list of `Product` objects.
        """
        result = await session.execute(select(Product).order_by(Product.id).offset(skip).limit(limit))
        products = result.scalars().all()
        return products

    @classmethod
    async def post_new_product(cls, product, session: AsyncSession):
        """
        Create a new product.

        Args:
            product (Product): `Product` object containing the new product's data.
            session (AsyncSession): Asynchronous SQLAlchemy session used for database operations.

        Returns:
            Product: Newly created `Product` object.
        """
        new_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            count=product.count
        )

        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)

        return new_product

    @classmethod
    async def delete_product(cls, product_id: int, session: AsyncSession):
        """
        Delete a product by its ID.

        Args:
            product_id (int): ID of the product to delete.
            session (AsyncSession): Asynchronous SQLAlchemy session used for database operations.

        Returns:
            Product: Deleted `Product` object.

        Raises:
            ValueError: If the product with the specified ID is not found.
        """
        result = await session.execute(select(Product).filter(Product.id == product_id))
        product = result.scalars().first()

        if product is None:
            raise ValueError(f"Product with id {product_id} not found.")

        await session.delete(product)
        await session.commit()

        return product

    @classmethod
    async def update_product(cls, updated_product, session: AsyncSession):
        """
        Update the details of an existing product.

        Args:
            updated_product (Product): `Product` object containing the new data for the product.
            session (AsyncSession): Asynchronous SQLAlchemy session used for database operations.

            Returns:
                Product: Updated `Product` object.

        Raises:
            ValueError: If the product with the specified ID is not found.
        """
        result = await session.execute(select(Product).filter(Product.id == updated_product.id_product))
        existing_product = result.scalars().first()

        if existing_product is None:
            raise ValueError(f"Product with id {updated_product.id_product} not found.")

        existing_product.name = updated_product.new_name
        existing_product.description = updated_product.new_description
        existing_product.price = updated_product.new_price
        existing_product.count = updated_product.new_count

        await session.commit()
        await session.refresh(existing_product)

        return existing_product
