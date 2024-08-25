from app.models.shop_models import Product


class ProductCrud:
    @classmethod
    def get_all_products(cls, skip, limit, session):
        products = session.query(Product).order_by(Product.id).offset(skip).limit(limit).all()
        return products

    @classmethod
    def post_new_product(cls, product, session):
        new_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            count=product.count
        )

        session.add(new_product)
        session.commit()
        session.refresh(new_product)

        return new_product

    @classmethod
    def delete_product(cls, product_id: int, session):
        product = session.query(Product).filter(Product.id == product_id).first()

        if product is None:
            raise ValueError(f"Product with id {product_id} not found.")

        session.delete(product)
        session.commit()

        return product

    @classmethod
    def update_product(cls, updated_product, session):
        existing_product = session.query(Product).filter(Product.id == updated_product.id_product).first()
        if existing_product is None:
            raise ValueError(f"Product with id {updated_product.id_product} not found.")

        existing_product.name = updated_product.new_name
        existing_product.description = updated_product.new_description
        existing_product.price = updated_product.new_price
        existing_product.count = updated_product.new_count

        session.commit()
        session.refresh(existing_product)
        return existing_product
