from sqlalchemy.orm import Mapped, mapped_column
from app.models.shop_models import Model


class EndpointCall(Model):
    __tablename__ = "endpoint_calls"

    id: Mapped[int] = mapped_column(primary_key=True)
    endpoint_name: Mapped[str] = mapped_column(nullable=False)
    call_count: Mapped[int] = mapped_column(default=0, nullable=False)
