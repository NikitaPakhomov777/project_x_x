from fastapi import FastAPI
from app.models.session import create_tables
from app.routers.product import product_router
from app.routers.customer import customer_router
from app.routers.endpoint_calls import endpoint_calls_router
from app.routers.sale import sale_router
from app.services.middleware_call_count import count_endpoint_calls
from app.services.publish_endpoints import publish_endpoints

def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)

publish_endpoints()

app.middleware("http")(count_endpoint_calls)

routers = [product_router, customer_router, sale_router, endpoint_calls_router]

for router in routers:
    app.include_router(router)
