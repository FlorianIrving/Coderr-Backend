from .serializers import OfferPostSerializer, OfferGetSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from offers_app.models import Offer, OfferDetail
from django_filters.rest_framework import FilterSet, NumberFilter
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from offers_app.api.serializers import OfferGetDetailSerializer, OfferDetailOneSerializer, OfferPatchDetailSerializer


class OfferFilter(FilterSet):
    """
    FilterSet for filtering offers based on price, delivery time, and creator ID.
    """
    min_price = NumberFilter(field_name='details__price', lookup_expr='gte')
    max_delivery_time = NumberFilter(
        field_name='details__delivery_time_in_days', lookup_expr='lte')
    creator_id = NumberFilter(field_name='user_id', lookup_expr='exact')


class OfferView(APIView):
    """
    API view for listing and creating offers.
    Supports filtering, searching, ordering, and pagination on GET.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieves a list of offers with optional filtering, searching, and ordering.
        Supports:
        - creator_id: Filter by creator's user ID
        - min_price: Minimum offer detail price
        - max_delivery_time: Maximum delivery time in days
        - search: Case-insensitive title or description match
        - ordering: Sort results (default: updated_at descending)
        """
        offers = Offer.objects.all()

        # Filter by creator ID
        creator_id = request.query_params.get("creator_id")
        if creator_id:
            offers = offers.filter(user_id=creator_id)

        # Filter by minimum price
        min_price = request.query_params.get("min_price")
        if min_price:
            offers = offers.filter(details__price__gte=min_price)

        # Filter by maximum delivery time
        max_delivery_time = request.query_params.get("max_delivery_time")
        if max_delivery_time:
            offers = offers.filter(
                details__delivery_time_in_days__lte=max_delivery_time)

        # Search in title or description
        search = request.query_params.get("search")
        if search:
            offers = offers.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        # Ordering by specified field or default to updated_at
        ordering = request.query_params.get("ordering", "-updated_at")
        offers = offers.order_by(ordering)

        # Paginate and serialize the queryset
        paginator = PageNumberPagination()
        paginated_offers = paginator.paginate_queryset(
            offers.distinct(), request)
        serializer = OfferGetSerializer(
            paginated_offers, many=True, context={"request": request})

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Creates a new offer with nested offer details.
        """
        serializer = OfferPostSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            offer = serializer.save()
            return Response(OfferPostSerializer(offer).data, status=201)
        return Response(serializer.errors, status=400)


class OfferDetailView(APIView):
    """
    API view for retrieving, updating or deleting a specific offer.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        Retrieves a single offer by ID with detailed information.
        """
        offer = get_object_or_404(Offer, pk=pk)
        serializer = OfferGetDetailSerializer(
            offer, context={"request": request})
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        """
        Partially updates a specific offer and its nested details.
        """
        offer = get_object_or_404(Offer, pk=pk)
        serializer = OfferPatchDetailSerializer(
            offer,
            data=request.data,
            partial=True,
            context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            offer_data = serializer.data
            return Response({
                "id": offer_data["id"],
                "title": offer_data["title"],
                "image": offer_data["image"],
                "description": offer_data["description"],
                "details": offer_data["details"]
            }, status=200)
        return Response({
            "message": "Update failed.",
            "errors": serializer.errors
        }, status=400)

    def delete(self, request, pk):
        """
        Deletes a specific offer by ID.
        """
        offer = get_object_or_404(Offer, pk=pk)
        offer.delete()
        return Response(status=204)


class OfferDetailOneView(APIView):
    """
    API view for retrieving a single OfferDetail entry by ID.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        Returns one specific OfferDetail object.
        """
        offer_detail = get_object_or_404(OfferDetail, pk=pk)
        serializer = OfferDetailOneSerializer(
            offer_detail, context={"request": request})
        return Response(serializer.data, status=200)
