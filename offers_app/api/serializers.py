from rest_framework import serializers
from offers_app.models import OfferDetail, Offer
from django.db.models import Min

# Offer Get


class OfferDetailListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f"/api/offerdetails/{obj.id}/")
        return f"/api/offerdetails/{obj.id}/"


class OfferGetSerializer(serializers.ModelSerializer):
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
        profile = getattr(obj.user, 'profile', None)
        if not profile:
            return {}
        return {
            "first_name": profile.first_name or "",
            "last_name": profile.last_name or "",
            "username": obj.user.username or ""
        }

# Offer Post


class OfferDetailPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days',
                  'price', 'features', 'offer_type']


class OfferPostSerializer(serializers.ModelSerializer):
    details = OfferDetailPostSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def create(self, validated_data):
        details_data = validated_data.pop("details")

        min_price = min(detail["price"] for detail in details_data)
        min_delivery_time = min(detail["delivery_time_in_days"]
                                for detail in details_data)

        offer = Offer.objects.create(
            user=self.context["request"].user,
            min_price=min_price,
            min_delivery_time=min_delivery_time,
            **validated_data
        )

        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)

        return offer


# Offer direct offer
class OfferDetailSimpleSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f"/api/offerdetails/{obj.id}/")


class OfferGetDetailSerializer(serializers.ModelSerializer):
    details = OfferDetailSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at',
            'details', 'min_price', 'min_delivery_time'
        ]


class OfferGetDetailSerializer(serializers.ModelSerializer):
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
        return int(obj.details.aggregate(Min('price'))['price__min'])

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(Min('delivery_time_in_days'))['delivery_time_in_days__min']


# Offer Patch
class OfferDetailNestedSerializer(serializers.ModelSerializer):
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
    details = OfferDetailNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "title",
            "image",
            "description",
            "details"
        ]


# Offer One View Get
class OfferDetailOneSerializer(serializers.ModelSerializer):

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

# # NEW
# class UserDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username']
#
#
# class OfferDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OfferDetail
#         fields = ['id', 'title', 'revisions',
#                   'delivery_time_in_days', 'price', 'features', 'offer_type']
#
#
#
# class OfferSerializer(serializers.ModelSerializer):
#     details = OfferDetailSerializer(many=True, read_only=True)
#     min_price = serializers.SerializerMethodField()
#     min_delivery_time = serializers.SerializerMethodField()
#     user_details = UserDetailsSerializer(source='user', read_only=True)

#     class Meta:
#         model = Offer
#         fields = [
#             'id', 'user', 'title', 'image', 'description',
#             'created_at', 'updated_at',
#             'details', 'min_price', 'min_delivery_time',
#             'user_details'
#         ]

#     def get_min_price(self, obj):
#         return obj.details.aggregate(Min('price'))['price__min']

#     def get_min_delivery_time(self, obj):
#         return obj.details.aggregate(Min('delivery_time_in_days'))['delivery_time_in_days__min']
# # NEW END
