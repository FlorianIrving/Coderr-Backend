from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from reviews_app.models import ReviewGetModel, ReviewPatchDeleteModel, ReviewPostModel
from .serializers import ReviewGetSerializer, ReviewPostSerializer, ReviewPostResponseSerializer, ReviewPatchSerializer
from django.db.models import Avg
from django.contrib.auth.models import User
from offers_app.models import Offer


class ReviewGetPostView(APIView):
    """
    API view for retrieving the reviews for the logged-in user and posting new reviews.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns a list of reviews where the logged-in user is the recipient.
        """
        user = request.user
        queryset = ReviewGetModel.objects.filter(user=user)
        serializer = ReviewGetSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        """
        Creates a new review written by the logged-in user.
        """
        serializer = ReviewPostSerializer(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        # Set the reviewer to the authenticated user
        review = serializer.save(reviewer=request.user)
        # Serialize the response using the response serializer
        response_serializer = ReviewPostResponseSerializer(review)
        return Response(response_serializer.data, status=201)


class ReviewPatchDeleteView(APIView):
    """
    API view for updating or deleting a review written by the logged-in user.
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        """
        Partially updates a review by ID if the user is the author.
        """
        try:
            review = ReviewPatchDeleteModel.objects.get(
                pk=pk, reviewer=request.user)
        except ReviewPatchDeleteModel.DoesNotExist:
            return Response({"detail": "Review not found."}, status=404)

        serializer = ReviewPatchSerializer(
            review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_review = serializer.save()

        response_serializer = ReviewPostResponseSerializer(updated_review)
        return Response(response_serializer.data, status=200)

    def delete(self, request, pk):
        """
        Deletes a review by ID if the user is the author.
        """
        try:
            review = ReviewPatchDeleteModel.objects.get(
                pk=pk, reviewer=request.user)
            review.delete()
            return Response(status=204)
        except ReviewPatchDeleteModel.DoesNotExist:
            return Response({"detail": "Review not found."}, status=404)


class BaseInfoView(APIView):
    """
    Public API view that returns general statistics for the landing page.
    Includes total reviews, average rating, number of business profiles, and offers.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        """
        Returns basic aggregated info for public display.
        """
        review_count = ReviewPostModel.objects.count()
        average_rating = ReviewPostModel.objects.aggregate(Avg("rating"))[
            "rating__avg"] or 0.0
        business_profile_count = User.objects.filter(
            profile__type="business").count()
        offer_count = Offer.objects.count()

        return Response({
            "review_count": review_count,
            "average_rating": round(average_rating, 1),
            "business_profile_count": business_profile_count,
            "offer_count": offer_count
        }, status=200)
