from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from reviews_app.models import ReviewPatchDeleteModel, ReviewPostModel
from .serializers import ReviewPostSerializer, ReviewPostResponseSerializer, ReviewPatchSerializer
from django.db.models import Avg
from django.contrib.auth.models import User
from offers_app.models import Offer


class ReviewGetPostView(APIView):
    """
    API view for retrieving the reviews for the logged-in user and posting new reviews.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns a list of all reviews. Can be filtered by business_user_id, reviewer_id and ordered by updated_at or rating.
        Only accessible to authenticated users.
        """
        # Grund-Queryset: alle Reviews aus der Datenbank
        queryset = ReviewPostModel.objects.all()

        # Optionaler Filter: Nur Bewertungen für einen bestimmten Business-Nutzer
        business_user_id = request.query_params.get("business_user_id")
        if business_user_id:
            queryset = queryset.filter(business_user__id=business_user_id)

        # Optionaler Filter: Nur Bewertungen von einem bestimmten Rezensenten
        reviewer_id = request.query_params.get("reviewer_id")
        if reviewer_id:
            queryset = queryset.filter(reviewer__id=reviewer_id)

        # Optionales Sortieren nach einem Feld ('updated_at' oder 'rating')
        ordering = request.query_params.get("ordering")
        if ordering in ["updated_at", "rating"]:
            queryset = queryset.order_by(ordering)

        # Serialisieren und Rückgabe der (ggf. gefilterten) Liste
        serializer = ReviewPostResponseSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        """
        Creates a new review written by the logged-in user.
        Only users with 'customer' profile type are allowed to post reviews.
        """
        user = request.user

        # Check if user is authenticated
        if not user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=401)

        # Check if user has a customer profile
        if not hasattr(user, "profile") or user.profile.type != "customer":
            return Response({"detail": "Only customers can write reviews."}, status=403)

        serializer = ReviewPostSerializer(
            data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
    
        # Save the review with the authenticated user as reviewer
        review = serializer.save(reviewer=user)

        # Serialize and return the newly created review
        response_serializer = ReviewPostResponseSerializer(review)
        return Response(response_serializer.data, status=201)


class ReviewPatchDeleteView(APIView):
    """
    API view for updating or deleting a review written by the logged-in user.
    """
    authentication_classes = [TokenAuthentication]
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
