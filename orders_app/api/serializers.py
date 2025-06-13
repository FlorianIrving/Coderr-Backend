from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from orders_app.models import OrderMainModel, OfferDetail


class OrderPostSerializer(serializers.Serializer):
    offer_detail_id = serializers.IntegerField()

    def validate_offer_detail_id(self, value):
        try:
            offer_detail = OfferDetail.objects.select_related(
                "offer").get(pk=value)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError("OfferDetail not found.")
        return offer_detail

    def create(self, validated_data):
        request = self.context["request"]
        offer_detail = validated_data["offer_detail_id"]
        offer = offer_detail.offer
        if request.user.profile.type != "customer":
            raise PermissionDenied("Only customers can place orders.")
        return OrderMainModel.objects.create(
            customer_user=request.user,
            business_user=offer.user,
            offer_detail=offer_detail,
            status="in_progress"
        )


class OrderGetResponseSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="offer_detail.title", read_only=True)
    revisions = serializers.IntegerField(
        source="offer_detail.revisions", read_only=True)
    delivery_time_in_days = serializers.IntegerField(
        source="offer_detail.delivery_time_in_days", read_only=True)
    price = serializers.DecimalField(
        source="offer_detail.price", max_digits=10, decimal_places=2, read_only=True)
    features = serializers.ListField(
        source="offer_detail.features", read_only=True)
    offer_type = serializers.CharField(
        source="offer_detail.offer_type", read_only=True)

    class Meta:
        model = OrderMainModel
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at"
        ]


class OrderPostResponseSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="offer_detail.title", read_only=True)
    revisions = serializers.IntegerField(
        source="offer_detail.revisions", read_only=True)
    delivery_time_in_days = serializers.IntegerField(
        source="offer_detail.delivery_time_in_days", read_only=True)
    price = serializers.DecimalField(
        source="offer_detail.price", read_only=True, max_digits=10, decimal_places=2)
    features = serializers.ListField(
        source="offer_detail.features", read_only=True)
    offer_type = serializers.CharField(
        source="offer_detail.offer_type", read_only=True)

    class Meta:
        model = OrderMainModel
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at"
        ]
