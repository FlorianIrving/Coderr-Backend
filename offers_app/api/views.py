from .serializers import OfferPostSerializer, OfferGetSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from offers_app.models import Offer, OfferDetail
from django_filters.rest_framework import FilterSet, NumberFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from offers_app.api.serializers import OfferGetDetailSerializer, OfferDetailOneSerializer, OfferPatchDetailSerializer


class OfferFilter(FilterSet):
    min_price = NumberFilter(field_name='details__price', lookup_expr='gte')
    max_delivery_time = NumberFilter(
        field_name='details__delivery_time_in_days', lookup_expr='lte')
    creator_id = NumberFilter(field_name='user_id', lookup_expr='exact')


class OfferViewSet(ModelViewSet):
    queryset = Offer.objects.all().prefetch_related('details')
    serializer_class = OfferGetSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']


class OfferView(APIView):
    def get(self, request):
        queryset = Offer.objects.all().order_by('-updated_at')
        offers = Offer.objects.all()
        serializer = OfferGetSerializer(offers, many=True)
        response_data = {
            "count": len(serializer.data),
            "next": None,
            "previous": None,
            "results": serializer.data
        }
        return Response(response_data, status=200)

    def post(self, request):
        serializer = OfferPostSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            offer = serializer.save()
            return Response(OfferPostSerializer(offer).data, status=201)
        return Response(serializer.errors, status=400)


class OfferDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        offer = get_object_or_404(Offer, pk=pk)
        serializer = OfferGetDetailSerializer(
            offer, context={"request": request})
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
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
        offer = get_object_or_404(Offer, pk=pk)
        offer.delete()
        return Response(status=204)


class OfferDetailOneView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        offer_detail = get_object_or_404(OfferDetail, pk=pk)
        serializer = OfferDetailOneSerializer(
            offer_detail, context={"request": request})
        return Response(serializer.data, status=200)
