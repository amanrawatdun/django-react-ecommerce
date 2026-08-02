from django.db import models
from apps.categories.models import Category
from django.utils.text import slugify

# Create your models here.


class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
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

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

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