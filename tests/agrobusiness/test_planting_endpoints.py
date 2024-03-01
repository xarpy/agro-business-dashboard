import logging

import pytest

from agrobusiness.models import PlantingType

logger = logging.getLogger(__name__)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload, expected",
    [
        ({"plant_name": "milho"}, 201),
    ],
)
def test_create_planting(api_client, payload, create_token, create_farm, expected) -> None:
    """_Unit test for validate endpoint to register planting type"""
    headers = {"Authorization": f"Bearer {str(create_token.access_token)}"}
    payload["farm"] = str(create_farm.id)
    response = api_client.post("/api/planting", data=payload, headers=headers, format="json")
    logger.info(f"Show example: {response.data}")
    assert response.status_code == expected


@pytest.mark.django_db
def test_get_planting(api_client, create_token, create_farm) -> None:
    """_Unit test for validate endpoint to get planting type"""
    headers = {"Authorization": f"Bearer {str(create_token.access_token)}"}
    plant_type = PlantingType.objects.create(plant_name="milho", farm=create_farm)
    response = api_client.get(f"/api/planting/{plant_type.id}", headers=headers, format="json")
    logger.info(f"Show example: {response.data}")
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_planting(api_client, create_token, create_farm) -> None:
    """_Unit test for validate endpoint to delete planting type"""
    headers = {"Authorization": f"Bearer {str(create_token.access_token)}"}
    plant_type = PlantingType.objects.create(plant_name="milho", farm=create_farm)
    response = api_client.delete(f"/api/planting/{plant_type.id}", headers=headers, format="json")
    assert response.status_code == 204


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload, expected",
    [
        ({"plant_name": "soja"}, 200),
    ],
)
def test_update_planting(api_client, payload, create_token, create_farm, expected) -> None:
    """_Unit test for validate endpoint to update planting type"""
    headers = {"Authorization": f"Bearer {str(create_token.access_token)}"}
    payload["farm"] = str(create_farm.id)
    plant_type = PlantingType.objects.create(plant_name="milho", farm=create_farm)
    response = api_client.put(f"/api/planting/{plant_type.id}", data=payload, headers=headers, format="json")
    logger.info(f"Show example: {response.data}")
    assert response.status_code == expected


@pytest.mark.django_db
def test_chart_cultivation_by_name(api_client, create_token) -> None:
    """_Unit test for validate endpoint for chart cultivation by name"""
    headers = {"Authorization": f"Bearer {str(create_token.access_token)}"}
    response = api_client.get("/api/planting/stats/chart/cultivation-by-name", headers=headers, format="json")
    logger.info(f"Show example: {response.data}")
    assert response.status_code == 200
