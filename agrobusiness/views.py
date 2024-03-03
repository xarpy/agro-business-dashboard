from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema, inline_serializer
from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from agrobusiness.serializers import (
    Customer,
    CustomerSerializer,
    FarmProperty,
    FarmPropertySerializer,
    PlantingType,
    PlantingTypeSerializer,
    State,
    StateSerializer,
)


class StatesViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    """State Viewset class"""

    serializer_class = StateSerializer
    queryset = State.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description="Method to return values for the pie chart of farms in each state.",
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="ChartStateFarm",
                    fields={
                        "state": serializers.CharField(),
                        "farm_percentage": serializers.DecimalField(max_digits=4, decimal_places=2),
                    },
                ),
                examples=[
                    OpenApiExample(
                        "Case success",
                        value=[{"state": "string", "farm_percentage": 0.0}],
                        status_codes=[200],
                        response_only=True,
                    )
                ],
            )
        },
    )
    @action(detail=False, methods=["get"], url_path="stats/chart/state-farms")
    def farms_by_state(self, request, *args, **kwargs) -> Response:
        """Function responsible to return values for the pie chart of farms in each state.
        Args:
            request (django.HttpRequest): Receives django resquest instance
        Returns:
            Response: Returns the processed value to the graph.
        """
        result = []
        total_farms = FarmProperty.objects.all().count()
        for state in self.queryset:
            farm_by_state = state.state_farms.all().count()
            percentage = 0
            if farm_by_state and total_farms:
                percentage = farm_by_state / total_farms
            result.append({"state": state.acronym, "farm_percentage": percentage})
        return Response(result, status=status.HTTP_200_OK)


class CustomerViewset(viewsets.ModelViewSet):
    """Customer Viewset class"""

    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class FarmPropertyViewset(viewsets.ModelViewSet):
    """FarmProperty Viewset class"""

    serializer_class = FarmPropertySerializer
    queryset = FarmProperty.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description="Method that returns the total number of registered properties",
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="TotalFarms",
                    fields={
                        "farms_total": serializers.IntegerField(),
                    },
                ),
                examples=[
                    OpenApiExample(
                        "Case success",
                        value={"farms_total": 0},
                        status_codes=[200],
                        response_only=True,
                    )
                ],
            )
        },
    )
    @action(detail=False, methods=["get"], url_path="stats/total-farms")
    def total_farms(self, request, *args, **kwargs):
        """Function responsible to returns the total number of registered properties
        Args:
            request (django.HttpRequest): Receives django resquest instance
        Returns:
            Response: Returns the processed value
        """
        data = {"farms_total": self.queryset.count()}
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Method that returns the total area in hectares of the properties",
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="TotalArea",
                    fields={
                        "farms_area_total": serializers.IntegerField(),
                    },
                ),
                examples=[
                    OpenApiExample(
                        "Case success",
                        value={"farms_area_total": 0},
                        status_codes=[200],
                        response_only=True,
                    )
                ],
            )
        },
    )
    @action(detail=False, methods=["get"], url_path="stats/total-areas")
    def total_farm_areas(self, request, *args, **kwargs) -> Response:
        """Function responsible to returns the total area in hectares of the properties
        Args:
            request (django.HttpRequest): Receives django resquest instance
        Returns:
            Response: Returns the processed value
        """
        total = 0
        for item in self.queryset:
            total += item.area
        data = {"farms_area_total": total}
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Method that returns pie chart values by agricultural land use.",
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="ChartAgriculturalLandFarm",
                    fields={
                        "farm_name": serializers.CharField(),
                        "agricultural_land_percentage": serializers.DecimalField(max_digits=4, decimal_places=2),
                    },
                ),
                examples=[
                    OpenApiExample(
                        "Case success",
                        value=[{"farm_name": "string", "agricultural_land_percentage": 0.0}],
                        status_codes=[200],
                        response_only=True,
                    )
                ],
            )
        },
    )
    @action(detail=False, methods=["get"], url_path="stats/chart/agricultural-land")
    def farms_agricultural_land(self, request, *args, **kwargs) -> Response:
        """Function responsible to returns pie chart values by agricultural land use.
        Args:
            request (django.HttpRequest): Receives django resquest instance
        Returns:
            Response: Returns the processed value to the graph.
        """
        result = []
        total_land_used = sum([farm.agricultal_land for farm in self.queryset])
        for farm in self.queryset:
            agricultural_land = farm.agricultal_land
            percentage = 0
            if agricultural_land and total_land_used:
                percentage = agricultural_land / total_land_used
            result.append({"farm_name": farm.name, "agricultural_land_percentage": percentage})
        return Response(result, status=status.HTTP_200_OK)


class PlantingTypeViewset(viewsets.ModelViewSet):
    """PlantingType Viewset class"""

    serializer_class = PlantingTypeSerializer
    queryset = PlantingType.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description="Method to return values for the pie chart of cultivation plant types by quantities",
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="ChartCultivationName",
                    fields={
                        "plant_name": serializers.CharField(),
                        "cultivation_percentage": serializers.DecimalField(max_digits=4, decimal_places=2),
                    },
                ),
                examples=[
                    OpenApiExample(
                        "Case success",
                        value=[{"plant_name": "string", "cultivation_percentage": 0.0}],
                        status_codes=[200],
                        response_only=True,
                    )
                ],
            )
        },
    )
    @action(detail=False, methods=["get"], url_path="stats/chart/cultivation-by-name")
    def planting_type_by_name(self, request, *args, **kwargs) -> Response:
        """Function responsible to return values for the pie chart of cultivation plant types by quantities
        Args:
            request (django.HttpRequest): Receives django resquest instance
        Returns:
            Response: Returns the processed value to the graph.
        """
        result = []
        reference_types = set([item.plant_name for item in self.queryset])
        total_cultivation = self.queryset.count()
        for tyoe_value in reference_types:
            items = self.queryset.filter(plant_name=tyoe_value)
            items_count = items.count()
            percentage = 0
            if items_count and total_cultivation:
                percentage = items_count / total_cultivation
            result.append({"plant_name": tyoe_value, "cultivation_percentage": percentage})
        return Response(result, status=status.HTTP_200_OK)
