import uuid
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django_cpf_cnpj.fields import CNPJ, CPF


class State(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    acronym = models.CharField(max_length=2, null=False, blank=False, help_text="Sigla do estado")
    name = models.CharField(max_length=64, null=False, blank=False, help_text="Nome do estado")

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"
        db_table = "state"
        ordering = ["acronym"]

    def __str__(self) -> str:
        return f"{self.name}/{self.acronym}"


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    personal_document = models.CharField(
        max_length=25, null=False, blank=False, help_text="Documento pessoal da usuario, podendo ser CPF ou CNPJ"
    )
    name = models.CharField(max_length=256, null=False, blank=False, help_text="Nome do produtor")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Customter"
        verbose_name_plural = "Customers"
        db_table = "customer"
        ordering = ["-created_at"]

    def clean(self) -> None:
        personal_document = getattr(self, "personal_document")
        if not CPF(personal_document).is_valid() and not CNPJ(personal_document).is_valid():
            raise ValidationError("Tipo de documento CPF/CNPJ invalido!")
        return super().clean()

    def __str__(self) -> str:
        return self.name

    def save(self, **kwargs) -> None:
        self.clean()
        return super().save(**kwargs)


class FarmProperty(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="customer_farms",
        blank=False,
        null=False,
        help_text="Campo relacional do cliente",
    )
    state = models.ForeignKey(
        State,
        on_delete=models.DO_NOTHING,
        related_name="state_farms",
        blank=False,
        null=False,
        help_text="Campo relacional do estado da fazenda",
    )
    name = models.CharField(max_length=256, null=False, blank=False, help_text="Nome da fazenda ou propriedade")
    city = models.CharField(max_length=128, null=False, blank=False, help_text="Nome da cidade")
    area = models.DecimalField(
        max_digits=5, decimal_places=2, null=False, blank=False, help_text="Área total em hectares da fazenda"
    )
    farming_area = models.DecimalField(
        max_digits=5, decimal_places=2, null=False, blank=False, help_text="Área agricultável em hectares"
    )
    plant_area = models.DecimalField(
        max_digits=5, decimal_places=2, null=False, blank=False, help_text="Área de vegetação em hectares"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def clean(self) -> None:
        area = getattr(self, "area")
        farming_area = getattr(self, "farming_area")
        plant_area = getattr(self, "plant_area")
        if not area:
            raise ValidationError("Necessario cadastrar área da propriedade.")
        elif farming_area > area:
            raise ValidationError("Área agricultavél maior que a área da propriedade.")
        elif plant_area > area:
            raise ValidationError("Área da vegetação maior que a área da propriedade.")
        elif plant_area and farming_area and (plant_area + farming_area) > area:
            raise ValidationError(
                "A área agrícultável e área de vegetação somadas, não deve ser maior que a área total da fazenda."
            )
        return super().clean()

    class Meta:
        verbose_name = "Farm Property"
        verbose_name_plural = "Farm Properties"
        db_table = "farm_property"
        ordering = ["-created_at"]

    @property
    def agricultal_land(self) -> Decimal:
        return self.farming_area + self.plant_area

    def __str__(self) -> str:
        return self.name

    def save(self, **kwargs) -> None:
        self.clean()
        return super().save(**kwargs)


class PlantingType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plant_name = models.CharField(max_length=128, null=False, blank=False, help_text="Tipo de cultivo")
    farm = models.ForeignKey(
        FarmProperty,
        on_delete=models.CASCADE,
        related_name="cultivated_fields",
        blank=False,
        null=False,
        help_text="Campo relacional de cultivo da fazenda",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Planting Type"
        verbose_name_plural = "Planting Types"
        db_table = "planting_type"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.farm.name}|{self.plant_name}"
