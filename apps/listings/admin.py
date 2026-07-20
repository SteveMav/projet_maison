from django.contrib import admin

from apps.listings.models import Listing, ListingPhoto


class ListingPhotoInline(admin.TabularInline):
    model = ListingPhoto
    extra = 0
    fields = ("image", "position", "is_primary", "alt_text")


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "commune",
        "neighborhood",
        "property_type",
        "monthly_price_amount",
        "monthly_price_currency",
        "bedroom_count",
        "bathroom_count",
        "availability_status",
        "is_verified",
        "commissionnaire_profile",
        "updated_at",
    )
    list_filter = (
        "availability_status",
        "property_type",
        "is_verified",
        "commune",
        "bedroom_count",
    )
    search_fields = (
        "commune",
        "neighborhood",
        "description",
        "commissionnaire_profile__display_name",
    )
    readonly_fields = ("created_at", "updated_at")
    inlines = [ListingPhotoInline]
