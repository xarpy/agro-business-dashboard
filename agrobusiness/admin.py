from django import forms
from django.contrib import admin

from agrobusiness.models import Customer, FarmProperty, PlantingType, State


class FarmPropertyrForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["area"].required = True

    class Meta:
        model = FarmProperty
        fields = "__all__"


class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["personal_document"].required = True

    class Meta:
        model = Customer
        fields = "__all__"


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    search_fields = ["acronym", "name"]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    form = CustomerForm
    list_per_page = 25
    date_hierarchy = "created_at"
    search_fields = ["personal_document", "name"]
    readonly_fields = ["created_at", "id"]


@admin.register(FarmProperty)
class FarmPropertyrAdmin(admin.ModelAdmin):
    list_per_page = 25
    date_hierarchy = "created_at"
    search_fields = ["name", "city", "customer__name"]
    readonly_fields = ["created_at", "id"]
    form = FarmPropertyrForm


@admin.register(PlantingType)
class PlantingTypeAdmin(admin.ModelAdmin):
    list_per_page = 25
    date_hierarchy = "created_at"
    search_fields = ["plant_name", "farm__name"]
    readonly_fields = ["created_at", "id"]
    list_filter = ["plant_name"]
