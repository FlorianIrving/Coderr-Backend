from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    RegistrationSerializer,
    LoginSerializer,
    UserProfileSerializer,
    UserProfilePatchSerializer,
    BusinessListSerializer,
    CustomerListSerializer
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from auth_app.models import UserProfile


class RegistrationView(APIView):
    """
    API endpoint for registering a new user.
    Returns auth token and basic user information upon success.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "token": user.auth_token.key,
                    "username": user.username,
                    "email": user.email,
                    "user_id": user.id
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API endpoint for logging in a user.
    Returns auth token and basic user information.
    """
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "token": user.auth_token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    API endpoint for retrieving and updating a user profile.
    GET: Retrieve profile by user ID.
    PATCH: Update profile (only allowed for the owner).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        Retrieves the profile for a specific user ID.
        """
        try:
            profile = UserProfile.objects.get(user__id=pk)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        """
        Partially updates a user profile.
        Only the owner of the profile is allowed to update it.
        """
        try:
            profile = UserProfile.objects.get(user__id=pk)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

        if request.user.id != profile.user.id:
            return Response({"detail": "Not authorized."}, status=403)

        serializer = UserProfilePatchSerializer(
            profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class BusinessListView(APIView):
    """
    API endpoint for listing all users with profile type 'business'.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = UserProfile.objects.filter(type="business")
        serializer = BusinessListSerializer(profiles, many=True)
        return Response(serializer.data, status=200)


class CustomerListView(APIView):
    """
    API endpoint for listing all users with profile type 'customer'.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = UserProfile.objects.filter(type="customer")
        serializer = CustomerListSerializer(profiles, many=True)
        return Response(serializer.data, status=200)
