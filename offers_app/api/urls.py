from django.urls import path
from .views import OfferViewSet, OfferDetailView
from rest_framework.routers import DefaultRouter


custom_urls = [
    path("offers/<int:pk>/", OfferDetailView.as_view(), name="offer-detail-view"),
]


router = DefaultRouter()
router.register(r'offers', OfferViewSet, basename='offer')

urlpatterns = custom_urls + router.urls

# urlpatterns = [
#     path("offers/", OfferView.as_view(), name="offer-list"),

# ]
