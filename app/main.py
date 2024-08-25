from fastapi import FastAPI
from app.models.session import create_tables
from app.routers.product import product_router
from app.routers.customer import customer_router
from app.routers.sale import sale_router


def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)

routers = [product_router, customer_router, sale_router]

for router in routers:
    app.include_router(router)
