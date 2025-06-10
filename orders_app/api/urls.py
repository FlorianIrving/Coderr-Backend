from django.urls import path
from .views import OrderCombinedView, OrderPatchDeleteView

urlpatterns = [
    path("orders/", OrderCombinedView.as_view(), name="orders"),
    path("orders/<int:pk>/", OrderPatchDeleteView.as_view(), name="order-detail"),
]