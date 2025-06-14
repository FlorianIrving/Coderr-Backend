from django.urls import path
from .views import RegistrationView, LoginView, UserProfileView, BusinessListView, CustomerListView

# URL patterns for user authentication and profile-related endpoints
urlpatterns = [
    # Endpoint for user registration
    path("registration/", RegistrationView.as_view(), name="user-registration"),

    # Endpoint for user login
    path("login/", LoginView.as_view(), name="user-login"),

    # Endpoint for retrieving or updating a specific user profile by ID
    path("profile/<int:pk>/", UserProfileView.as_view(), name="user-profil"),

    # Endpoint for listing all business-type user profiles
    path("profiles/business/", BusinessListView.as_view(), name="business-list"),

    # Endpoint for listing all customer-type user profiles
    path("profiles/customer/", CustomerListView.as_view(), name="customer-list"),
]
