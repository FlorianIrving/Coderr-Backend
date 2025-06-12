from django.urls import path
from .views import ReviewGetPostView

urlpatterns = [
    path("reviews/", ReviewGetPostView.as_view(), name="reviews"),
]
