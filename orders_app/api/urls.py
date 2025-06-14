from django.urls import path
from .views import OrderCombinedView, OrderPatchDeleteView, OrderCountView, OrderCompletedCountView

# URL patterns for managing and analyzing orders
urlpatterns = [
    # Endpoint to list all orders for the user or to create a new order
    path("orders/", OrderCombinedView.as_view(), name="orders"),

    # Endpoint to update the status of an order or delete it (admin only for DELETE)
    path("orders/<int:pk>/", OrderPatchDeleteView.as_view(), name="order-detail"),

    # Endpoint to get the count of orders with the same status as a specific order
    path("order-count/<int:pk>/", OrderCountView.as_view(), name="order-count"),

    # Endpoint to get the count of all completed orders for the current user
    path("completed-order-count/<int:pk>/",
         OrderCompletedCountView.as_view(), name="order-count-all"),
]
