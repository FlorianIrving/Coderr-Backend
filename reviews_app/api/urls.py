from django.urls import path
from .views import ReviewGetPostView, ReviewPatchDeleteView, BaseInfoView

urlpatterns = [
    path("reviews/", ReviewGetPostView.as_view(), name="reviews"),
    path("reviews/<int:pk>/", ReviewPatchDeleteView.as_view(), name="review-detail"),
    path("base-info/", BaseInfoView.as_view(), name="reviews-base-info"),
]
