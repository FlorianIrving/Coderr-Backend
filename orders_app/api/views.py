from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_204_NO_CONTENT
from orders_app.models import OrderMainModel
from .serializers import OrderGetResponseSerializer, OrderPostSerializer, OrderPostResponseSerializer
from django.contrib.auth.models import User


class OrderCombinedView(APIView):
    """
    Handles order listing and creation.
    - GET: Returns all orders where the user is either the customer or the business.
    - POST: Allows a customer to create a new order.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns all orders for the current user (as customer or business).
        """
        user = request.user
        queryset = OrderMainModel.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        ).distinct()
        serializer = OrderGetResponseSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        """
        Creates a new order. Only users with type 'customer' are allowed to post.
        """
        serializer = OrderPostSerializer(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        if request.user.profile.type != "customer":
            raise PermissionDenied("Nur Kunden dürfen Bestellungen aufgeben.")

        order = serializer.save()
        response_serializer = OrderPostResponseSerializer(order)
        return Response(response_serializer.data, status=201)


class OrderPatchDeleteView(APIView):
    """
    Handles partial updates and deletion of orders.
    - PATCH: Only business users can update the status of their orders.
    - DELETE: Only admins are allowed to delete orders.
    """

    def get_permissions(self):
        """
        Requires both IsAuthenticated and IsAdminUser for DELETE;
        only IsAuthenticated for PATCH.
        """
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

    def patch(self, request, pk):
        """
        Updates the 'status' of an order (only allowed by the assigned business user).
        Allowed status values: in_progress, completed, cancelled.
        """
        try:
            order = OrderMainModel.objects.select_related(
                "offer_detail__offer").get(pk=pk)
        except OrderMainModel.DoesNotExist:
            return Response({"detail": "Order not found."}, status=404)

        if request.user.id != order.business_user.id:
            return Response({"detail": "You are not authorized to update this order."}, status=401)

        allowed_fields = ["status"]
        if any(field not in allowed_fields for field in request.data):
            return Response({"detail": "Only 'status' field can be updated."}, status=400)

        new_status = request.data.get("status")
        if new_status not in ["in_progress", "completed", "cancelled"]:
            return Response({"detail": "Invalid status value."}, status=400)

        order.status = new_status
        order.save()
        response_serializer = OrderPostResponseSerializer(order)
        return Response(response_serializer.data, status=200)

    def delete(self, request, pk):
        """
        Deletes an order. Only allowed for admin users.
        """
        order = get_object_or_404(OrderMainModel, id=pk)
        order.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class OrderCountView(APIView):
    """
    Returns the count of 'in_progress' orders for a given business user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "Business user not found."}, status=404)

        if not hasattr(user, 'profile') or user.profile.type != "business":
            return Response({"detail": "User exists but is not a business profile."}, status=400)

        count = OrderMainModel.objects.filter(
            business_user=user,
            status="in_progress"
        ).count()

        return Response({"order_count": count}, status=200)


class OrderCompletedCountView(APIView):
    """
    Returns the count of completed orders for a specific business user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "Business user not found."}, status=404)

        if not hasattr(user, 'profile') or user.profile.type != "business":
            return Response({"detail": "User is not a business profile."}, status=400)

        count = OrderMainModel.objects.filter(
            business_user=user,
            status="completed"
        ).count()

        return Response({"completed_order_count": count}, status=200)
