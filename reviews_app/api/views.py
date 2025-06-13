from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from reviews_app.models import ReviewGetModel, ReviewPatchDeleteModel, ReviewPostModel
from .serializers import ReviewGetSerializer, ReviewPostSerializer, ReviewPostResponseSerializer, ReviewPatchSerializer
from django.db.models import Avg
from django.contrib.auth.models import User
from offers_app.models import Offer

# Create your views here.


class ReviewGetPostView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        queryset = ReviewGetModel.objects.filter(user=user)
        serializer = ReviewGetSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = ReviewPostSerializer(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        review = serializer.save(reviewer=request.user)
        response_serializer = ReviewPostResponseSerializer(review)
        return Response(response_serializer.data, status=201)


class ReviewPatchDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            review = ReviewPatchDeleteModel.objects.get(pk=pk, reviewer=request.user)
        except ReviewPatchDeleteModel.DoesNotExist:
            return Response({"detail": "Review not found."}, status=404)

        serializer = ReviewPatchSerializer(review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_review = serializer.save()

        response_serializer = ReviewPostResponseSerializer(updated_review)
        return Response(response_serializer.data, status=200)

    def delete(self, request, pk):
        try:
            review = ReviewPatchDeleteModel.objects.get(pk=pk, reviewer=request.user)
            review.delete()
            return Response(status=204)
        except ReviewPatchDeleteModel.DoesNotExist:
            return Response({"detail": "Review not found."}, status=404)
        
class BaseInfoView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        review_count = ReviewPostModel.objects.count()
        average_rating = ReviewPostModel.objects.aggregate(Avg("rating"))["rating__avg"] or 0.0
        business_profile_count = User.objects.filter(profile__type="business").count()
        offer_count = Offer.objects.count()

        return Response({
            "review_count": review_count,
            "average_rating": round(average_rating, 1),
            "business_profile_count": business_profile_count,
            "offer_count": offer_count
        }, status=200)
