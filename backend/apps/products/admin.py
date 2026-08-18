from django.contrib import admin
from .models import Product , ProductVariant ,ProductImage,Brand
# Register your models here.
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Brand)

@admin.register(ProductVariant)
class ProductVarientAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product",
        "color",
        "size",
        "price",
        "stock",
    )

    list_filter = (
        "color",
        "size",
    )

    search_fields = (
        "product__name",
    )
   
