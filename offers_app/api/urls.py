from django.urls import path
from .views import OfferDetailView, OfferDetailOneView, OfferView
from rest_framework.routers import DefaultRouter

# Custom API endpoints for offer-related operations
custom_urls = [
    # Endpoint for retrieving, updating or deleting a specific offer by ID
    path("offers/<int:pk>/", OfferDetailView.as_view(), name="offer-detail-view"),

    # Endpoint for retrieving a single OfferDetail entry by ID
    path("offerdetails/<int:pk>/",
         OfferDetailOneView.as_view(), name="offer-one-view"),

    # Endpoint for listing all offers or creating a new one
    path("offers/", OfferView.as_view(), name="offer-list"),
]

# Default router (currently unused but included for future extensibility)
router = DefaultRouter()

# Combine custom URLs with any router-based viewsets
urlpatterns = custom_urls + router.urls
