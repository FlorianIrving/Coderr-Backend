from django.urls import path
from .views import RegistrationView, LoginView, UserProfileDetailUpdateView

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="user-registration"),
    path("login/", LoginView.as_view(), name="user-login"),
    path("profile/<int:pk>/", UserProfileDetailUpdateView.as_view(), name="user-profil"),
]
