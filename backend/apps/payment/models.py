from django.db import models
from apps.order.models import Order 

# Create your models here.
class Payment(models.Model):
    class Status(models.TextChoices): 
        CREATED = "CREATED", "Created"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE, 
        related_name="payment" 
        ) 

    razorpay_order_id = models.CharField(max_length=255)

    razorpay_payment_id = models.CharField(
        max_length=255, 
        blank=True 
        ) 
    
    razorpay_signature = models.CharField( 
        max_length=500, 
        blank=True 
        )
     
    status = models.CharField( 
        max_length=20, 
        choices=Status.choices, 
        default=Status.CREATED 
        ) 
    
    created_at = models.DateTimeField(auto_now_add=True)