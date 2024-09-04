import pytest
from app.crud_operations.product_crud import ProductCrud
from app.schemas.product import ProductCreate, ProductUpdate


@pytest.mark.asyncio
async def test_get_products(client, session):
    await ProductCrud.post_new_product(
        ProductCreate(name="Product A", description="Description A", price=10.99, count=100), session)
    await ProductCrud.post_new_product(
        ProductCreate(name="Product B", description="Description B", price=20.99, count=200), session)

    response = await client.get("/products/get/")
    assert response.status_code == 200
    assert len(response.json()) == 2  # Проверяем, что два продукта


@pytest.mark.asyncio
async def test_create_product(client, session):
    product_data = ProductCreate(
        name="Product C",
        description="Description C",
        price=15.99,
        count=150
    )

    created_product = await ProductCrud.post_new_product(product_data, session)

    response = await client.post("/products/add/", json=product_data.model_dump())

    assert response.status_code == 200
    assert response.json()["name"] == created_product.name
    assert response.json()["description"] == created_product.description
    assert response.json()["price"] == created_product.price
    assert response.json()["count"] == created_product.count


@pytest.mark.asyncio
async def test_update_product(client, session):
    # Создание продукта для обновления
    product_data = ProductCreate(
        name="Product D",
        description="Description D",
        price=30.99,
        count=300
    )

    new_product = await ProductCrud.post_new_product(product_data, session)

    # Обновление данных продукта
    update_data = ProductUpdate(
        id_product=new_product.id,
        new_name="Updated Product D",
        new_description="Updated Description D",
        new_price=35.99,
        new_count=350
    )

    response = await client.patch("/products/update_product/", json=update_data.model_dump())

    assert response.status_code == 200
    assert response.json()["name"] == update_data.new_name
    assert response.json()["description"] == update_data.new_description
    assert response.json()["price"] == update_data.new_price
    assert response.json()["count"] == update_data.new_count


@pytest.mark.asyncio
async def test_delete_product(client, session):

    product_data = ProductCreate(
        name="Product E",
        description="Description E",
        price=25.99,
        count=250
    )

    new_product = await ProductCrud.post_new_product(product_data, session)

    response = await client.delete(f"/products/delete_product/{new_product.id}")

    assert response.status_code == 200
