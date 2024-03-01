from decimal import Decimal

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from agrobusiness.models import Customer, FarmProperty, PlantingType, State


@pytest.mark.django_db
def test_user_create() -> None:
    """_Unit test for validate create User record on Django Admin"""
    User.objects.create_user("Admin", "admin@admin.com", "12345")
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_state_create() -> None:
    """_Unit test for validate create State record"""
    State.objects.create(acronym="PB", name="Paraiba")
    assert State.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data, expected",
    [
        ({"personal_document": "61526731002", "name": "Test CPF valid"}, 1),
        ({"personal_document": "15076648000119", "name": "Test CNPJ valid"}, 1),
        (
            {"personal_document": "6152673100A", "name": "Test CPF invalid"},
            "Tipo de documento CPF/CNPJ invalido!",
        ),
        (
            {"personal_document": "1507C648000119", "name": "Test CNPJ invalid"},
            "Tipo de documento CPF/CNPJ invalido!",
        ),
    ],
)
def test_customer_create(data, expected) -> None:
    """_Unit test for validate create Customer record"""
    try:
        Customer.objects.create(**data)
        result = Customer.objects.count()
    except ValidationError as error:
        result = error.message
    assert result == expected


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
            1,
        ),
        (
            {
                "name": "Mantegeira Fazenda",
                "city": "Joao Pessoa",
                "area": Decimal(10),
                "farming_area": Decimal(11),
                "plant_area": Decimal(2),
            },
            "Área agricultavél maior que a área da propriedade.",
        ),
        (
            {
                "name": "Mantegeira Fazenda",
                "city": "Joao Pessoa",
                "area": Decimal(10),
                "farming_area": Decimal(1),
                "plant_area": Decimal(12),
            },
            "Área da vegetação maior que a área da propriedade.",
        ),
        (
            {
                "name": "Mantegeira Fazenda",
                "city": "Joao Pessoa",
                "area": Decimal(10),
                "farming_area": Decimal(6),
                "plant_area": Decimal(5),
            },
            "A área agrícultável e área de vegetação somadas, não deve ser maior que a área total da fazenda.",
        ),
    ],
)
def test_farm_property_create(create_customer, create_state, data, expected) -> None:
    """_Unit test for validate create FarmProperty record"""
    try:
        data.update({"state": create_state, "customer": create_customer})
        FarmProperty.objects.create(**data)
        result = FarmProperty.objects.count()
    except ValidationError as error:
        result = error.message
    assert result == expected


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data, expected",
    [
        ({"plant_name": "milho"}, 1),
    ],
)
def test_planting_type_create(create_farm, data, expected) -> None:
    """_Unit test for validate create PlantingType record"""
    data["farm"] = create_farm
    PlantingType.objects.create(**data)
    result = PlantingType.objects.count()
    assert result == expected
