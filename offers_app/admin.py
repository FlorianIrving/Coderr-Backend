from django.contrib import admin
from offers_app.models import Offer, OfferDetail


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "min_price",
                    "min_delivery_time", "created_at")
    search_fields = ("title", "user__username")
    list_filter = ("created_at",)


@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    list_display = ("title", "offer", "price",
                    "delivery_time_in_days", "offer_type")
    search_fields = ("title",)
    list_filter = ("offer_type",)
