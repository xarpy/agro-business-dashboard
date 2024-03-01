from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from agrobusiness.models import Customer, FarmProperty, PlantingType, State


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

    def _clean_fields(self, validated_data):
        instance = self.Meta.model(**validated_data)
        try:
            instance.clean()
        except DjangoValidationError as error:
            raise ValidationError(error.message)

    def create(self, validated_data):
        self._clean_fields(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self._clean_fields(validated_data)
        return super().update(instance, validated_data)


class FarmPropertySerializer(serializers.ModelSerializer):
    state = serializers.SlugRelatedField(queryset=State.objects.all(), slug_field="acronym")
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = FarmProperty
        fields = ["id", "customer", "state", "name", "area", "farming_area", "plant_area", "created_at", "updated_at"]

    def _clean_fields(self, validated_data):
        instance = self.Meta.model(**validated_data)
        try:
            instance.clean()
        except DjangoValidationError as error:
            raise ValidationError(error.message)

    def create(self, validated_data):
        self._clean_fields(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self._clean_fields(validated_data)
        return super().update(instance, validated_data)


class PlantingTypeSerializer(serializers.ModelSerializer):
    farm = serializers.PrimaryKeyRelatedField(queryset=FarmProperty.objects.all())

    class Meta:
        model = PlantingType
        fields = ["id", "plant_name", "farm", "created_at", "updated_at"]
