from django.db import models
from django.contrib.auth.models import User


class Offer(models.Model):
    """
    Represents a general offer created by a user (typically a business or freelancer).
    Each offer can contain multiple offer details (variants like basic, pro, premium).
    """
    # The user who created the offer
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Main title of the offer
    title = models.CharField(max_length=255)

    # Optional image associated with the offer
    image = models.ImageField(upload_to='offers/', null=True, blank=True)

    # Description of the offer's purpose or contents
    description = models.TextField()

    # Automatically calculated minimum price from associated OfferDetail entries
    min_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    # Automatically calculated minimum delivery time from associated OfferDetail entries
    min_delivery_time = models.IntegerField(default=0)

    # Timestamp when the offer was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Timestamp when the offer was last updated
    updated_at = models.DateTimeField(auto_now=True)


class OfferDetail(models.Model):
    """
    Represents a specific tier or version of an offer (e.g. basic, standard, premium).
    Contains pricing, delivery time, and included features.
    """
    # The offer to which this detail belongs
    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name="details")

    # Title of this specific offer detail (e.g. "Basic Design Package")
    title = models.CharField(max_length=255)

    # Number of revision rounds included
    revisions = models.IntegerField()

    # Estimated delivery time in days
    delivery_time_in_days = models.IntegerField()

    # Price of this offer detail
    price = models.DecimalField(max_digits=10, decimal_places=0)

    # List of features included in this package (stored as JSON array)
    features = models.JSONField()

    # Type or label of the offer detail (e.g. "basic", "pro", "premium")
    offer_type = models.CharField(max_length=50)
