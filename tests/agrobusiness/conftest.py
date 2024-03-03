from decimal import Decimal

import pytest
from django.contrib.auth.models import User
from django.core.management import call_command
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken, Token

from agrobusiness.models import Customer, FarmProperty, State


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker) -> None:
    """_Fixture to provide inject all data from fixtures extracted manually by django."""
    with django_db_blocker.unblock():
        call_command("loaddata", "test_data.json")


@pytest.fixture(scope="function")
def api_client() -> APIClient:
    """Fixture to provide an API client
    Returns:
        APIClient: Return a APIClient instance for testing
    """
    yield APIClient()


@pytest.fixture(scope="function")
def create_user() -> User:
    """Fixture to provide an User for testing
    Returns:
        User: Return a User instance
    """
    user = User.objects.create_user("Test", "test@testando.com", "12345", **{"is_staff": True, "is_superuser": False})
    return user


@pytest.fixture(scope="function")
def create_customer() -> Customer:
    """Fixture to provide an Customer for testing
    Returns:
        User: Return a Customer instance
    """
    customer = Customer.objects.create(personal_document="61526731002", name="John Doe")
    return customer


@pytest.fixture(scope="function")
def create_state() -> State:
    """Fixture to provide an State for testing
    Returns:
        User: Return a State instance
    """
    state = State.objects.create(acronym="PB", name="Paraiba")
    return state


@pytest.fixture(scope="function")
def create_farm(create_state, create_customer) -> FarmProperty:
    """Fixture to provide an FarmProperty for testing
    Returns:
        User: Return a FarmProperty instance
    """
    data = {
        "name": "Mantegeira Fazenda",
        "customer": create_customer,
        "state": create_state,
        "city": "Joao Pessoa",
        "area": Decimal(10),
        "farming_area": Decimal(1),
        "plant_area": Decimal(2),
    }
    farm = FarmProperty.objects.create(**data)
    return farm


@pytest.fixture(scope="function")
def create_token(create_user) -> Token:
    """Fixture to provide an Token, based on user instance
    Args:
        create_user (function): Received the fixture function to create a user instance
    Returns:
        str: Return a access token
    """
    user = create_user
    refresh = RefreshToken.for_user(user)
    return refresh
