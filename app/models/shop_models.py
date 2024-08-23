from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import ForeignKey


class Model(DeclarativeBase):
    pass


class Product(Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    count: Mapped[int]

    sales = relationship("Sale", back_populates="product")


class Customer(Model):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str]

    sales = relationship("Sale", back_populates="customer")


class Sale(Model):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    quantity: Mapped[int]
    total_price: Mapped[float]

    product = relationship("Product", back_populates="sales")
    customer = relationship("Customer", back_populates="sales")
