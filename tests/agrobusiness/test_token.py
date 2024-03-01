import logging

import pytest
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload, expected",
    [
        ({"username": "admin", "password": "12345"}, 200),
    ],
)
def test_get_token(api_client, payload, expected) -> None:
    """_Unit test for validate endpoint to get token"""
    User.objects.create_user("admin", "admin@admin.com", "12345", **{"is_staff": True, "is_superuser": True})
    response = api_client.post("/api/token/", data=payload, format="json")
    logger.info(f"Show example: {response.data}")
    assert response.status_code == expected


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload, expected",
    [
        ({"refresh": ""}, 200),
    ],
)
def test_refresh_token(api_client, create_token, payload, expected) -> None:
    """_Unit test for validate endpoint to refresh token"""
    payload["refresh"] = str(create_token)
    response = api_client.post("/api/token/refresh/", data=payload, format="json")
    logger.info(f"Show example: {response.data}")
    assert response.status_code == expected
