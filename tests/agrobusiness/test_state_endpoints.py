import logging

import pytest

from agrobusiness.models import State

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_chart_farm_by_state(api_client, django_db_setup, create_token) -> None:
    """_Unit test for validate endpoint for chart farm by state"""
    headers = {"Authorization": f"Bearer {str(create_token.access_token)}"}
    response = api_client.get("/api/states/stats/chart/state-farms", headers=headers, format="json")
    logger.info(f"Show data: {response.data}")
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_state(api_client, django_db_setup, create_token) -> None:
    """_Unit test for validate endpoint to list all states"""
    headers = {"Authorization": f"Bearer {str(create_token.access_token)}"}
    response = api_client.get(f"/api/states", headers=headers, format="json")
    logger.info(f"Show data: {response.data}")
    assert response.status_code == 200
