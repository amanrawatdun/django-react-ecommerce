from django.urls import path
from .views import CreatePaymentView ,VerifyPaymentView

urlpatterns=[
    path( 
        "orders/<int:order_id>/create-payment/", 
         CreatePaymentView.as_view(), 
    ),
    path( 
        "orders/<int:order_id>/verify-payment/", 
         VerifyPaymentView.as_view(), 
    ),
]