from django.urls import path
from .views import OfferDetailView, OfferDetailOneView, OfferView
from rest_framework.routers import DefaultRouter


custom_urls = [
    path("offers/<int:pk>/", OfferDetailView.as_view(), name="offer-detail-view"),
    path("offerdetails/<int:pk>/", OfferDetailOneView.as_view(), name="offer-one-view"),
    path("offers/", OfferView.as_view(), name="offer-list"),


]


router = DefaultRouter()
# router.register(r'offers', OfferViewSet, basename='offer')

urlpatterns = custom_urls + router.urls

# urlpatterns = [
#     path("offers/", OfferView.as_view(), name="offer-list"),

# ]
