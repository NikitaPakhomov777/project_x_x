import pytest
from app.crud_operations.customer_crud import CustomerCrud
from app.schemas.customer import CustomerCreate, CustomerUpdate


@pytest.mark.asyncio
async def test_get_customers(client, session):
    await CustomerCrud.post_new_customer(
        CustomerCreate(name="John Doe", email="john@example.com", phone="1234567890"), session)
    await CustomerCrud.post_new_customer(
        CustomerCreate(name="Jane Doe", email="jane@example.com", phone="0987654321"), session)
    response = await client.get("/customers/get/")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_create_customer(client, session):
    customer_data = CustomerCreate(
        name="Alice Smith",
        email="alice@example.com",
        phone="555-1234"
    )

    created_customer = await CustomerCrud.post_new_customer(customer_data, session)

    response = await client.post("/customers/add/", json=customer_data.model_dump())

    assert response.status_code == 200
    assert response.json()["name"] == created_customer.name
    assert response.json()["email"] == created_customer.email
    assert response.json()["phone"] == created_customer.phone


@pytest.mark.asyncio
async def test_update_customer(client, session):
    customer_data = CustomerCreate(
        name="Bob Brown",
        email="bob@example.com",
        phone="555-5678"
    )

    new_customer = await CustomerCrud.post_new_customer(customer_data, session)
    update_data = CustomerUpdate(
        id_customer=new_customer.id,
        new_name="Robert Brown",
        new_email="robert@example.com",
        new_phone="555-8765"
    )

    response = await client.patch("/customers/update_customer/", json=update_data.model_dump())

    assert response.status_code == 200
    assert response.json()["name"] == update_data.new_name
    assert response.json()["email"] == update_data.new_email
    assert response.json()["phone"] == update_data.new_phone


@pytest.mark.asyncio
async def test_delete_customer(client, session):
    customer_data = CustomerCreate(
        name="Charlie Green",
        email="charlie@example.com",
        phone="555-4321"
    )

    new_customer = await CustomerCrud.post_new_customer(customer_data, session)

    response = await client.delete(f"/customers/delete_customer/{new_customer.id}/")

    assert response.status_code == 200
