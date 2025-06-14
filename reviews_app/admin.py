from django.contrib import admin
from reviews_app.models import ReviewGetModel, ReviewPostModel, ReviewPatchDeleteModel


@admin.register(ReviewGetModel)
class ReviewGetAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")


@admin.register(ReviewPostModel)
class ReviewPostAdmin(admin.ModelAdmin):
    list_display = ("id", "reviewer", "business_user", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("reviewer__username", "business_user__username")


@admin.register(ReviewPatchDeleteModel)
class ReviewPatchDeleteAdmin(admin.ModelAdmin):
    list_display = ("id", "reviewer", "business_user", "rating", "created_at")
