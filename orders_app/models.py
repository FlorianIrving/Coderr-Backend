from django.db import models
from django.contrib.auth.models import User
from offers_app.models import OfferDetail

class OrderMainModel(models.Model):
    customer_user = models.ForeignKey(
        User, related_name="orders_as_customer", on_delete=models.CASCADE)
    business_user = models.ForeignKey(
        User, related_name="orders_as_business", on_delete=models.CASCADE)
    offer_detail = models.ForeignKey(OfferDetail, on_delete=models.CASCADE)

    status = models.CharField(max_length=50, default="in_progress")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
