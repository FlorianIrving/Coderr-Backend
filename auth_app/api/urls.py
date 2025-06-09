from django.urls import path
from .views import RegistrationView, LoginView, UserProfileView, BusinessListView, CustomerListView

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="user-registration"),
    path("login/", LoginView.as_view(), name="user-login"),
    path("profile/<int:pk>/", UserProfileView.as_view(), name="user-profil"),
    path("profiles/business/", BusinessListView.as_view(), name="business-list"),
    path("profiles/customer/", CustomerListView.as_view(), name="customer-list"),
]
