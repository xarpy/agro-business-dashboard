import logging
from decimal import Decimal

import pytest

from agrobusiness.models import FarmProperty

logger = logging.getLogger(__name__)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload, expected",
    [
        (
            {
                "name": "Mantegeira Fazenda",
                "city": "Joao Pessoa",
                "area": Decimal(10).to_eng_string(),
                "farming_area": Decimal(1).to_eng_string(),
                "plant_area": Decimal(2).to_eng_string(),
            },
            201,
        ),
        (
            {
                "name": "Mantegeira Fazenda",
                "city": "Joao Pessoa",
                "area": Decimal(10).to_eng_string(),
                "farming_area": Decimal(11).to_eng_string(),
                "plant_area": Decimal(2).to_eng_string(),
            },
            400,
        ),
        (
            {
                "name": "Mantegeira Fazenda",
                "city": "Joao Pessoa",
                "area": Decimal(10).to_eng_string(),
                "farming_area": Decimal(1).to_eng_string(),
                "plant_area": Decimal(12).to_eng_string(),
            },
            400,
        ),
        (
            {
                "name": "Mantegeira Fazenda",
                "city": "Joao Pessoa",
                "area": Decimal(10).to_eng_string(),
                "farming_area": Decimal(6).to_eng_string(),
                "plant_area": Decimal(5).to_eng_string(),
            },
            400,
        ),
    ],
)
def test_create_farm_property(api_client, payload, create_token, create_customer, create_state, expected) -> None:
    """_Unit test for validate endpoint to register farm_property"""
    headers = {"Authorization": f"Bearer {str(create_token.access_token)}"}
    payload.update({"state": create_state.acronym, "customer": str(create_customer.id)})
    response = api_client.post("/api/farm", data=payload, headers=headers, format="json")
    logger.info(f"Show data: {response.data}")
    assert response.status_code == expected


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data, expected",
    [
        (
            {
                "name": "Mantegeira Fazenda",
                "city": "Joao Pessoa",
                "area": Decimal(10),
                "farming_area": Decimal(1),
                "plant_area": Decimal(2),
            },
            200,
        )
    ],
)
def test_get_farm_property(api_client, create_token, create_customer, create_state, data, expected) -> None:
    """_Unit test for validate endpoint to get farm_property"""
    headers = {"Authorization": f"Bearer {str(create_token.access_token)}"}
    data.update({"state": create_state, "customer": create_customer})
    farm = FarmProperty.objects.create(**data)
    response = api_client.get(f"/api/farm/{farm.id}", headers=headers, format="json")
    logger.info(f"Show data: {response.data}")
    assert response.status_code == expected


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data, expected",
    [
        (
            {
                "name": "Mantegeira Fazenda",
                "city": "Joao Pessoa",
                "area": Decimal(10),
                "farming_area": Decimal(1),
                "plant_area": Decimal(2),
            },
            204,
        )
    ],
)
def test_delete_farm_property(api_client, create_token, create_customer, create_state, data, expected) -> None:
    """_Unit test for validate endpoint to delete farm_property"""
    headers = {"Authorization": f"Bearer {str(create_token.access_token)}"}
    data.update({"state": create_state, "customer": create_customer})
    farm = FarmProperty.objects.create(**data)
    response = api_client.delete(f"/api/farm/{farm.id}", headers=headers, format="json")
    assert response.status_code == expected


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data, payload, expected",
    [
        (
            {
                "name": "Mantegeira Fazenda",
                "city": "Joao Pessoa",
                "area": Decimal(10),
                "farming_area": Decimal(1),
                "plant_area": Decimal(2),
            },
            {
                "name": "Mantegeira 2",
                "city": "Joao Pessoa",
                "area": Decimal(10).to_eng_string(),
                "farming_area": Decimal(1).to_eng_string(),
                "plant_area": Decimal(2).to_eng_string(),
            },
            200,
        )
    ],
)
def test_update_farm_property(api_client, create_token, create_customer, create_state, data, payload, expected) -> None:
    """_Unit test for validate endpoint to update farm_property"""
    headers = {"Authorization": f"Bearer {str(create_token.access_token)}"}
    data.update({"state": create_state, "customer": create_customer})
    payload.update({"state": create_state.acronym, "customer": str(create_customer.id)})
    farm = FarmProperty.objects.create(**data)
    response = api_client.put(f"/api/farm/{farm.id}", data=payload, headers=headers, format="json")
    logger.info(f"Show data: {response.data}")
    assert response.status_code == expected


@pytest.mark.django_db
def test_chart_agricultural_land(api_client, django_db_setup, create_token) -> None:
    """_Unit test for validate endpoint for chart agricultural_land"""
    headers = {"Authorization": f"Bearer {str(create_token.access_token)}"}
    response = api_client.get("/api/farm/stats/chart/agricultural-land", headers=headers, format="json")
    logger.info(f"Show data: {response.data}")
    assert response.status_code == 200


@pytest.mark.django_db
def test_total_area(api_client, django_db_setup, create_token) -> None:
    """_Unit test for validate endpoint for stats total area"""
    headers = {"Authorization": f"Bearer {str(create_token.access_token)}"}
    response = api_client.get("/api/farm/stats/total-areas", headers=headers, format="json")
    logger.info(f"Show data: {response.data}")
    assert response.status_code == 200


@pytest.mark.django_db
def test_total_farm(api_client, django_db_setup, create_token) -> None:
    """_Unit test for validate endpoint for stats total farms quantities"""
    headers = {"Authorization": f"Bearer {str(create_token.access_token)}"}
    response = api_client.get("/api/farm/stats/total-farms", headers=headers, format="json")
    logger.info(f"Show data: {response.data}")
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_farm(api_client, django_db_setup, create_token) -> None:
    """_Unit test for validate endpoint to list all farms registered"""
    headers = {"Authorization": f"Bearer {str(create_token.access_token)}"}
    response = api_client.get(f"/api/farm", headers=headers, format="json")
    logger.info(f"Show data: {response.data}")
    assert response.status_code == 200
