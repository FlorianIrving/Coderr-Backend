from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_204_NO_CONTENT
from orders_app.models import OrderMainModel
from .serializers import OrderGetResponseSerializer, OrderPostSerializer, OrderPostResponseSerializer


class OrderCombinedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        queryset = OrderMainModel.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        ).distinct()
        serializer = OrderGetResponseSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = OrderPostSerializer(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        if request.user.profile.type != "customer":
            raise PermissionDenied("Nur Kunden dürfen Bestellungen aufgeben.")

        order = serializer.save()
        response_serializer = OrderPostResponseSerializer(order)
        return Response(response_serializer.data, status=201)


class OrderPatchDeleteView(APIView):
    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

    def patch(self, request, pk):
        try:
            order = OrderMainModel.objects.select_related(
                "offer_detail__offer").get(pk=pk)
        except OrderMainModel.DoesNotExist:
            return Response({"detail": "Order not found."}, status=404)
        if request.user.id != order.business_user.id:
            return Response({"detail": "You are not authorized to update this order."}, status=403)
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
        order = get_object_or_404(OrderMainModel, id=pk)
        order.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class OrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        try:
            order = OrderMainModel.objects.get(pk=pk)
        except OrderMainModel.DoesNotExist:
            return Response({"detail": "Order not found."}, status=404)
        queryset = OrderMainModel.objects.filter(
            Q(customer_user=user) | Q(business_user=user),
            status=order.status
        ).distinct()
        count = queryset.count()
        return Response({"order_count": count}, status=200)
    
class OrderCompletedCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        queryset = OrderMainModel.objects.filter(
            Q(customer_user=user) | Q(business_user=user),
            status="completed"
        ).distinct()
        count = queryset.count()
        return Response({"order_count": count}, status=200)