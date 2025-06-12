from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from reviews_app.models import ReviewGetPostModel
from .serializers import ReviewGetPostSerializer


# Create your views here.



class ReviewGetPostView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        queryset = ReviewGetPostModel.objects.filter(user=user)
        serializer = ReviewGetPostSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = ReviewGetPostSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        response_serializer = ReviewGetPostSerializer(review)
        return Response(response_serializer.data, status=201)