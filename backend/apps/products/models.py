from django.db import models
from apps.categories.models import Category
from django.utils.text import slugify
import uuid

# Create your models here.

class Brand(models.Model):

    name=models.CharField(
        max_length=100,
        unique=True,
        help_text="Brand name (eg., Nike , Adidas)"
    )

    slug=models.SlugField(
        unique=True,
        blank=True,
        db_index=True,
        help_text="Auto-generated URL slug"
    )

    logo=models.ImageField(
        upload_to="brands/",
        blank=True,
        null=True,
        help_text="Brand logo image"
    )

    def save(self , *args , **kwargs):
        if not self.slug and self.name:
            self.slug=slugify(self.name)
        super().save(*args , **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    brand=models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="products"
    )

    name = models.CharField(
        max_length=255
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    description = models.TextField()


    is_active = models.BooleanField(
        default=True
    )



    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    def save(self, *args, **kwargs):
     if not self.slug:
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
        
       
        while Product.objects.filter(slug=slug).exclude(id=self.id).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
            
        self.slug = slug

     super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductVariant(models.Model):

    class Size(models.TextChoices):
        SMALL = "S", "Small"
        MEDIUM = "M", "Medium"
        LARGE = "L", "Large"
        XL = "XL", "Extra Large"

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
    )

    sku = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        db_index=True,
        help_text="Stock Keeping Unit - Auto-generated if left blank"
    )

    color = models.CharField(
        max_length=20   
    )

    size = models.CharField(
        max_length=2,
        choices=Size.choices,
    )

    price=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        constraints = [

            models.UniqueConstraint(

                fields=[
                    "product",
                    "color",
                    "size",
                ],

                name="unique_product_variant"

            )

        ]

    def save(self , *args ,**kwargs):
        if not self.sku:
            prod_code=slugify(self.product.name)[:3].upper()
            color_code=slugify(self.color)[:3].upper()
            size_code=slugify(self.size).upper()
            unique_suffix = str(uuid.uuid4().hex[:4].upper())

            self.sku=f"{prod_code}-{color_code}-{size_code}-{unique_suffix}"
        super().save(*args , **kwargs)

    def __str__(self):

        return f"{self.product.name} ({self.color} - {self.size})"

class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )

    alt_text = models.CharField(
    max_length=255,
    blank=True
    )

    image = models.ImageField(
        upload_to="products/"
    )

    is_primary = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.product.name} Image"
    
