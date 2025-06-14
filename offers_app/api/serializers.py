from rest_framework import serializers
from offers_app.models import OfferDetail, Offer
from django.db.models import Min


class OfferDetailListSerializer(serializers.ModelSerializer):
    """
    Serializer to return basic offer detail information with an absolute URL.
    Used for listing references to individual OfferDetail entries.
    """
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        """
        Returns the full URL for the offer detail endpoint.
        """
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f"/api/offerdetails/{obj.id}/")
        return f"/api/offerdetails/{obj.id}/"


class OfferGetSerializer(serializers.ModelSerializer):
    """
    Serializer to return full Offer data including details and minimal user info.
    """
    details = OfferDetailListSerializer(many=True, read_only=True)
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details',
            'min_price', 'min_delivery_time', 'user_details'
        ]

    def get_user_details(self, obj):
        """
        Returns first name, last name and username of the user who created the offer.
        """
        profile = getattr(obj.user, 'profile', None)
        if not profile:
            return {}
        return {
            "first_name": profile.first_name or "",
            "last_name": profile.last_name or "",
            "username": obj.user.username or ""
        }


class OfferDetailPostSerializer(serializers.ModelSerializer):
    """
    Serializer used for creating or editing individual OfferDetail entries.
    """
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days',
                  'price', 'features', 'offer_type']


class OfferPostSerializer(serializers.ModelSerializer):
    """
    Serializer for creating an Offer with multiple OfferDetail entries.
    Calculates min_price and min_delivery_time based on provided details.
    """
    details = OfferDetailPostSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def create(self, validated_data):
        details_data = validated_data.pop("details")

        # Calculate minimum price and delivery time across details
        min_price = min(detail["price"] for detail in details_data)
        min_delivery_time = min(detail["delivery_time_in_days"]
                                for detail in details_data)

        # Create the offer instance
        offer = Offer.objects.create(
            user=self.context["request"].user,
            min_price=min_price,
            min_delivery_time=min_delivery_time,
            **validated_data
        )

        # Create all associated details
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)

        return offer


class OfferDetailSimpleSerializer(serializers.ModelSerializer):
    """
    Minimal serializer for OfferDetail with ID and absolute URL.
    """
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        """
        Builds and returns the full URL for an offer detail.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(f"/api/offerdetails/{obj.id}/")


class OfferGetDetailSerializer(serializers.ModelSerializer):
    """
    Full detail view serializer for a single Offer, including dynamically calculated
    min_price and min_delivery_time, and a nested list of associated details.
    """
    details = OfferDetailSimpleSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at',
            'details', 'min_price', 'min_delivery_time'
        ]

    def get_min_price(self, obj):
        """
        Returns the minimum price from all associated offer details.
        """
        return int(obj.details.aggregate(Min('price'))['price__min'])

    def get_min_delivery_time(self, obj):
        """
        Returns the minimum delivery time from all associated offer details.
        """
        return obj.details.aggregate(Min('delivery_time_in_days'))['delivery_time_in_days__min']


class OfferDetailNestedSerializer(serializers.ModelSerializer):
    """
    Serializer used for nested representation of OfferDetail objects.
    """
    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type"
        ]


class OfferPatchDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for patching an offer and selectively updating associated details.
    Only updates matching OfferDetail entries based on offer_type.
    """
    details = OfferDetailPostSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = [
            "id",
            "title",
            "image",
            "description",
            "details"
        ]

    def update(self, instance, validated_data):
        details_data = validated_data.pop("details", None)

        # Update main Offer fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Conditionally update or create matching OfferDetails
        if details_data is not None:
            for detail_data in details_data:
                offer_type = detail_data.get("offer_type")
                if not offer_type:
                    continue
                detail_instance, created = OfferDetail.objects.update_or_create(
                    offer=instance,
                    offer_type=offer_type,
                    defaults=detail_data
                )

        return instance


class OfferDetailOneSerializer(serializers.ModelSerializer):
    """
    Full serializer for returning a single OfferDetail object.
    """
    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type"
        ]
