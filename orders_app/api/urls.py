from django.urls import path
from .views import OrderCombinedView, OrderPatchDeleteView, OrderCountView, OrderCompletedCountView

urlpatterns = [
    path("orders/", OrderCombinedView.as_view(), name="orders"),
    path("orders/<int:pk>/", OrderPatchDeleteView.as_view(), name="order-detail"),
    path("order-count/<int:pk>/", OrderCountView.as_view(), name="order-count"),
    path("completed-order-count/<int:pk>/", OrderCompletedCountView.as_view(), name="order-count-all"),
]