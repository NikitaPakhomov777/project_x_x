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
            raise ValueError(f"Product with id {id} not found.")

        session.delete(product)
        session.commit()

        return product
