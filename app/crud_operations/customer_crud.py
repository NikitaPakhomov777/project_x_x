from app.models.shop_models import Customer


class CustomerCrud:
    @classmethod
    def get_all_customers(cls, skip, limit, session):
        customers = session.query(Customer).order_by(Customer.id).offset(skip).limit(limit).all()
        return customers

    @classmethod
    def post_new_customer(cls, customer, session):
        new_customer = Customer(
            name=customer.name,
            email=customer.email,
            phone=customer.phone
        )

        session.add(new_customer)
        session.commit()
        session.refresh(new_customer)

        return new_customer

    @classmethod
    def delete_customer(cls, customer_id: int, session):
        product = session.query(Customer).filter(Customer.id == customer_id).first()

        if product is None:
            raise ValueError(f"Product with id {id} not found.")

        session.delete(product)
        session.commit()

        return product

    @classmethod
    def update_customer(cls, updated_customer, session):
        existing_customer = session.query(Customer).filter(Customer.id == updated_customer.id_customer).first()
        if existing_customer is None:
            raise ValueError(f"Product with id {updated_customer.id_customer} not found.")

        existing_customer.name = updated_customer.new_name
        existing_customer.email = updated_customer.new_email
        existing_customer.phone = updated_customer.new_phone
        session.commit()
        session.refresh(existing_customer)
        return existing_customer
