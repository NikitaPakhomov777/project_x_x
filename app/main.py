from fastapi import FastAPI
from app.models.session import create_tables
from app.routers import product


def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(product.product_router)
