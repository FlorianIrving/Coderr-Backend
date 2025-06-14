from django.db import models
from django.contrib.auth.models import User
from offers_app.models import OfferDetail


class OrderMainModel(models.Model):
    """
    Represents an order placed by a customer for a specific offer detail provided by a business user.
    """

    # The user who placed the order (the customer)
    customer_user = models.ForeignKey(
        User, related_name="orders_as_customer", on_delete=models.CASCADE
    )

    # The user who receives the order (the business/freelancer)
    business_user = models.ForeignKey(
        User, related_name="orders_as_business", on_delete=models.CASCADE
    )

    # The specific offer detail that was ordered
    offer_detail = models.ForeignKey(OfferDetail, on_delete=models.CASCADE)

    # The current status of the order (e.g., in_progress, completed, cancelled)
    status = models.CharField(max_length=50, default="in_progress")

    # Timestamp when the order was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Timestamp when the order was last updated
    updated_at = models.DateTimeField(auto_now=True)
