from reviews_app.models import ReviewGetModel, ReviewPostModel, ReviewPatchDeleteModel
from rest_framework import serializers


class ReviewGetSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving reviews including metadata and references
    to both business user and reviewer.
    """
    class Meta:
        model = ReviewGetModel
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at"
        ]


class ReviewPostSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new review.
    Only includes fields required during submission.
    """
    class Meta:
        model = ReviewPostModel
        fields = ["business_user", "rating", "description"]


class ReviewPostResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for returning a complete review after creation or update,
    including ID, timestamps, and related users.
    """
    class Meta:
        model = ReviewPostModel
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at"
        ]


class ReviewPatchSerializer(serializers.ModelSerializer):
    """
    Serializer for partial updates to a review (PATCH),
    allowing rating and description to be modified.
    """
    class Meta:
        model = ReviewPatchDeleteModel
        fields = ["rating", "description"]
