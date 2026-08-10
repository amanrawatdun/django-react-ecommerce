from django.contrib import admin
from .models import Address
# Register your models here.
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "city",
        "state",
        "is_default",
    )

    list_filter = (
        "city",
        "state",
        "is_default",
    )

    search_fields = (
        "full_name",
        "phone_number",
    )
    