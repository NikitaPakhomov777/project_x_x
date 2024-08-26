from app.models.shop_models import Sale, Product


class SaleCrud:
    @classmethod
    def get_all_sales(cls, skip, limit, session):
        sales = session.query(Sale).order_by(Sale.id).offset(skip).limit(limit).all()
        return sales

    @classmethod
    def post_new_sale(cls, sale, session):

        new_sale = Sale(
            product_id=sale.product_id,
            customer_id=sale.customer_id,
            quantity=sale.quantity,
        )

        product = session.query(Product).filter(Product.id == new_sale.product_id).first()

        if product is None:
            raise ValueError(f"Product with id {sale.product_id} not found.")
        if product.count < sale.quantity:
            raise ValueError(f"Product with id {sale.product_id} count not enough.")

        product.count -= sale.quantity

        total_price = product.price * new_sale.quantity

        new_sale.total_price = total_price

        session.add(new_sale)
        session.commit()
        session.refresh(new_sale)

        return new_sale

    @classmethod
    def delete_sale(cls, sale_id: int, session):
        product = session.query(Sale).filter(Sale.id == sale_id).first()

        if product is None:
            raise ValueError(f"Product with id {sale_id} not found.")

        session.delete(product)
        session.commit()

        return product

    @classmethod
    def update_sale(cls, updated_sale, session):
        existing_sale = session.query(Sale).filter(Sale.id == updated_sale.id_sale).first()
        if existing_sale is None:
            raise ValueError(f"Product with id {updated_sale.id_sale} not found.")

        existing_sale.quantity = updated_sale.new_quantity
        existing_sale.total_price = updated_sale.new_total_price

        session.commit()
        session.refresh(existing_sale)

        return existing_sale
