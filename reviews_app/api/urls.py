from django.urls import path
from .views import ReviewGetPostView, ReviewPatchDeleteView, BaseInfoView

# URL patterns for handling reviews and general landing page statistics
urlpatterns = [
    # Endpoint to list all reviews for the logged-in user and create new ones
    path("reviews/", ReviewGetPostView.as_view(), name="reviews"),

    # Endpoint to update or delete a specific review by ID (only by its author)
    path("reviews/<int:pk>/", ReviewPatchDeleteView.as_view(), name="review-detail"),

    # Public endpoint to retrieve aggregated platform statistics for the landing page
    path("base-info/", BaseInfoView.as_view(), name="reviews-base-info"),
]
