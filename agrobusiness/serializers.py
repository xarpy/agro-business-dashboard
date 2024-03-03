from typing import Any, Dict

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from agrobusiness.models import Customer, FarmProperty, PlantingType, State


class StateSerializer(serializers.ModelSerializer):
    """State Serializer class"""

    class Meta:
        model = State
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    """Customer Serializer class"""

    class Meta:
        model = Customer
        fields = "__all__"

    def _clean_fields(self, validated_data: Dict[Any, Any]) -> None:
        """Private function created to use field validation, based on the model's business rule.
        Args:
            validated_data (Dict): Receives the data validated by the serializer.
        Raises:
            ValidationError: Raise the validation, using the same value by Model class validation message.
        """
        instance = self.Meta.model(**validated_data)
        try:
            instance.clean()
        except DjangoValidationError as error:
            raise ValidationError(error.message)

    def create(self, validated_data: Dict[Any, Any]) -> Customer:
        """Create method overridden, to use the model's business rule validation.
        Args:
            validated_data (Dict[Any, Any]): Receives the data validated by the serializer.
        Returns:
            Customer: Return an customer instance
        """
        self._clean_fields(validated_data)
        return super().create(validated_data)

    def update(self, instance: Customer, validated_data: Dict[Any, Any]) -> Customer:
        """Update method overridden, to use the model's business rule validation.
        Args:
            instance (Customer): Receives the Customer instance
            validated_data (Dict[Any, Any]): Receives the data validated by the serializer.
        Returns:
             Customer: Return the same customer instance, now updated.
        """
        self._clean_fields(validated_data)
        return super().update(instance, validated_data)


class FarmPropertySerializer(serializers.ModelSerializer):
    """FarmProperty Serializer class"""

    state = serializers.SlugRelatedField(queryset=State.objects.all(), slug_field="acronym")
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = FarmProperty
        fields = ["id", "customer", "state", "name", "area", "farming_area", "plant_area", "created_at", "updated_at"]

    def _clean_fields(self, validated_data: Dict[Any, Any]) -> None:
        """Private function created to use field validation, based on the model's business rule.
        Args:
            validated_data (Dict): Receives the data validated by the serializer.
        Raises:
            ValidationError: Raise the validation, using the same value by Model class validation message.
        """
        instance = self.Meta.model(**validated_data)
        try:
            instance.clean()
        except DjangoValidationError as error:
            raise ValidationError(error.message)

    def create(self, validated_data: Dict[Any, Any]) -> FarmProperty:
        """Create method overridden, to use the model's business rule validation.
        Args:
            validated_data (Dict[Any, Any]): Receives the data validated by the serializer.
        Returns:
            FarmProperty: Return an customer instance
        """
        self._clean_fields(validated_data)
        return super().create(validated_data)

    def update(self, instance: FarmProperty, validated_data: Dict[Any, Any]) -> FarmProperty:
        """Update method overridden, to use the model's business rule validation.
        Args:
            instance (FarmProperty): Receives the FarmProperty instance
            validated_data (Dict[Any, Any]): Receives the data validated by the serializer.
        Returns:
             FarmProperty: Return the same farm instance, now updated.
        """
        self._clean_fields(validated_data)
        return super().update(instance, validated_data)


class PlantingTypeSerializer(serializers.ModelSerializer):
    """PlantingType Serializer class"""

    farm = serializers.PrimaryKeyRelatedField(queryset=FarmProperty.objects.all())

    class Meta:
        model = PlantingType
        fields = ["id", "plant_name", "farm", "created_at", "updated_at"]
