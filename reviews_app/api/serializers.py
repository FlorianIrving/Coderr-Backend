from reviews_app.models import ReviewGetModel, ReviewPostModel, ReviewPatchDeleteModel
from rest_framework import serializers


class ReviewGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewGetModel
        fields = ["id", "business_user", "reviewer", "rating",
                  "description", "created_at", "updated_at"]


class ReviewPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewPostModel
        fields = ["business_user", "rating", "description"]


class ReviewPostResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewPostModel
        fields = ["id", "business_user", "reviewer", "rating",
                  "description", "created_at", "updated_at"]


class ReviewPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewPatchDeleteModel
        fields = ["rating", "description"]
