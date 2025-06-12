from reviews_app.models import ReviewGetPostModel
from rest_framework import serializers


class ReviewGetPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewGetPostModel
        fields = "__all__"