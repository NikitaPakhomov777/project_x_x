from fastapi import FastAPI
from app.models.async_session import create_tables
from app.routers.product import product_router
from app.routers.customer import customer_router
from app.routers.endpoint_calls import endpoint_calls_router
from app.routers.sale import sale_router
from app.services.rabbitmq_worker import start_rabbitmq_worker
import asyncio
from uvicorn import Config, Server
from contextlib import asynccontextmanager
from app.services.middleware_call_count import register_middleware


@asynccontextmanager
async def lifespan(application: FastAPI):
    print(f"Starting lifespan for application: {application}")
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)

register_middleware(app)

routers = [product_router, customer_router, sale_router, endpoint_calls_router]

for router in routers:
    app.include_router(router)


async def main():
    config = Config(app="main:app", host="0.0.0.0", port=8000, reload=True)
    server = Server(config)

    await asyncio.gather(
        server.serve(),
        start_rabbitmq_worker()
    )


if __name__ == "__main__":
    asyncio.run(main())
