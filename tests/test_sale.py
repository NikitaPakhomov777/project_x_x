import pytest
from app.crud_operations.sale_crud import SaleCrud
from app.schemas.sale import SaleCreate, SaleUpdate


@pytest.mark.asyncio
async def test_get_sales(client, session):
    await SaleCrud.post_new_sale(
        SaleCreate(product_id=1, customer_id=1, quantity=5), session)
    await SaleCrud.post_new_sale(
        SaleCreate(product_id=2, customer_id=2, quantity=3), session)

    response = await client.get("/sales/get/")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_create_sale(client, session):
    sale_data = SaleCreate(
        product_id=3,
        customer_id=4,
        quantity=10
    )

    created_sale = await SaleCrud.post_new_sale(sale_data, session)

    response = await client.post("/sales/add/", json=sale_data.model_dump())

    assert response.status_code == 200
    assert response.json()["product_id"] == created_sale.product_id
    assert response.json()["customer_id"] == created_sale.customer_id
    assert response.json()["quantity"] == created_sale.quantity


@pytest.mark.asyncio
async def test_update_sale(client, session):
    sale_data = SaleCreate(
        product_id=1,
        customer_id=1,
        quantity=10
    )
    await SaleCrud.post_new_sale(sale_data, session)

    update_data = SaleUpdate(
        id_sale=1,
        product_id=1,
        customer_id=1,
        new_quantity=2000,
        new_total_price=40000.0
    )

    response = await client.patch("/sales/update_sale/", json=update_data.model_dump())

    assert response.status_code == 200
    assert response.json()["product_id"] == update_data.product_id
    assert response.json()["customer_id"] == update_data.customer_id
    assert response.json()["quantity"] == update_data.new_quantity
    assert response.json()["total_price"] == update_data.new_total_price


@pytest.mark.asyncio
async def test_delete_sale(client, session):
    sale_data = SaleCreate(
        product_id=5,
        customer_id=1,
        quantity=25
    )

    new_sale = await SaleCrud.post_new_sale(sale_data, session)

    response = await client.delete(f"/sales/delete_sale/{new_sale.id}")

    assert response.status_code == 200
