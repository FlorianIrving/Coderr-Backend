from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class ReviewGetModel(models.Model):
    """
    Read-only model used to return review data including author and timestamps.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # The review content written by the user
    review = models.TextField()
    # Timestamp when the review was created
    created_at = models.DateTimeField(auto_now_add=True)
    # Timestamp when the review was last updated
    updated_at = models.DateTimeField(auto_now=True)


class ReviewPostModel(models.Model):
    """
    Write-only model used to create reviews for business users.
    """
    # The user who is being reviewed (typically a business profile)
    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='business_reviews'
    )
    # Optional rating score (1 to 5)
    rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    # Optional written description of the review
    description = models.TextField(null=True, blank=True)
    # The user who wrote the review
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    # Timestamp when the review was created
    created_at = models.DateTimeField(auto_now_add=True)
    # Timestamp when the review was last updated
    updated_at = models.DateTimeField(auto_now=True)


class ReviewPatchDeleteModel(ReviewPostModel):
    """
    Proxy model used specifically for PATCH and DELETE operations on reviews.
    Inherits from ReviewPostModel but allows separation in serializers/views.
    """
    class Meta:
        proxy = True
