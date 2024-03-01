import logging

import pytest

from agrobusiness.models import Customer

logger = logging.getLogger(__name__)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload, expected",
    [
        ({"personal_document": "61526731002", "name": "John Doe"}, 201),
        ({"personal_document": "15076648000119", "name": "John Doe"}, 201),
        ({"personal_document": "6152673100A", "name": "John Doe"}, 400),
        ({"personal_document": "1507C648000119", "name": "John Doe"}, 400),
    ],
)
def test_create_customer(api_client, payload, create_token, expected) -> None:
    """_Unit test for validate endpoint to register customer"""
    headers = {"Authorization": f"Bearer {str(create_token.access_token)}"}
    response = api_client.post("/api/customer", data=payload, headers=headers, format="json")
    logger.info(f"Show example: {response.data}")
    assert response.status_code == expected


@pytest.mark.django_db
def test_get_customer(api_client, create_token) -> None:
    """_Unit test for validate endpoint to get customer"""
    headers = {"Authorization": f"Bearer {str(create_token.access_token)}"}
    customer = Customer.objects.create(personal_document="61526731002", name="John Doe")
    response = api_client.get(f"/api/customer/{customer.id}", headers=headers, format="json")
    logger.info(f"Show example: {response.data}")
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_customer(api_client, create_token) -> None:
    """_Unit test for validate endpoint to delete customer"""
    headers = {"Authorization": f"Bearer {str(create_token.access_token)}"}
    customer = Customer.objects.create(personal_document="61526731002", name="John Doe")
    response = api_client.delete(f"/api/customer/{customer.id}", headers=headers, format="json")
    assert response.status_code == 204


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload, expected",
    [
        ({"personal_document": "61526731002", "name": "Teste 2"}, 200),
    ],
)
def test_update_customer(api_client, payload, create_token, expected) -> None:
    """_Unit test for validate endpoint to update customer"""
    headers = {"Authorization": f"Bearer {str(create_token.access_token)}"}
    customer = Customer.objects.create(personal_document="61526731002", name="John Doe")
    response = api_client.put(f"/api/customer/{customer.id}", data=payload, headers=headers, format="json")
    logger.info(f"Show example: {response.data}")
    assert response.status_code == expected
