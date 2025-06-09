from django.db import models
from django.contrib.auth.models import User


class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='offers/', null=True, blank=True)
    description = models.TextField()
    min_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    min_delivery_time = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OfferDetail(models.Model):
    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name="details")
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    features = models.JSONField()
    offer_type = models.CharField(max_length=50)
