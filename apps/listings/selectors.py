from django.db.models import Prefetch
from django.db.models.functions import Coalesce

from apps.commissionnaires.models import CommissionnaireProfile
from apps.listings.models import Listing, ListingPhoto


def get_listing_primary_photo(listing):
    public_card_photos = getattr(listing, "public_card_photos", None)
    if public_card_photos is not None:
        if not public_card_photos:
            return None
        return public_card_photos[0]
    return listing.get_primary_photo()


def get_listing_for_commissionnaire(commissionnaire_profile, listing_id):
    if not isinstance(commissionnaire_profile, CommissionnaireProfile):
        raise TypeError("commissionnaire_profile must be a CommissionnaireProfile.")
    return Listing.objects.get(
        pk=listing_id,
        commissionnaire_profile=commissionnaire_profile,
    )


def get_public_browse_listings():
    ordered_photos = ListingPhoto.objects.order_by("-is_primary", "position", "id")
    return (
        Listing.objects.filter(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
        )
        .select_related("commissionnaire_profile")
        .prefetch_related(
            Prefetch("photos", queryset=ordered_photos, to_attr="public_card_photos")
        )
        .annotate(public_recency_at=Coalesce("submitted_at", "updated_at", "created_at"))
        .order_by("-public_recency_at", "-id")
    )


def filter_public_listings(filters):
    queryset = get_public_browse_listings()

    commune = filters.get("commune")
    if commune:
        queryset = queryset.filter(commune__iexact=commune)

    budget_min = filters.get("budget_min")
    if budget_min is not None:
        queryset = queryset.filter(monthly_price_amount__gte=budget_min)

    budget_max = filters.get("budget_max")
    if budget_max is not None:
        queryset = queryset.filter(monthly_price_amount__lte=budget_max)

    bedrooms_min = filters.get("bedrooms_min")
    if bedrooms_min is not None:
        queryset = queryset.filter(bedroom_count__gte=bedrooms_min)

    return queryset


def get_listing_detail_queryset():
    ordered_photos = ListingPhoto.objects.order_by("-is_primary", "position", "id")
    return (
        Listing.objects.exclude(
            availability_status=Listing.AvailabilityStatus.UNDER_REVIEW,
        )
        .select_related("commissionnaire_profile")
        .prefetch_related(Prefetch("photos", queryset=ordered_photos))
    )


def get_commissionnaire_inventory(profile):
    if not isinstance(profile, CommissionnaireProfile):
        raise TypeError("profile must be a CommissionnaireProfile.")
    ordered_photos = ListingPhoto.objects.order_by("-is_primary", "position", "id")
    return (
        Listing.objects.filter(commissionnaire_profile=profile)
        .select_related("commissionnaire_profile")
        .prefetch_related(
            Prefetch("photos", queryset=ordered_photos, to_attr="inventory_photos")
        )
        .order_by("-updated_at", "-id")
    )


def get_availability_freshness_state(listing, now=None):
    from django.conf import settings
    from django.utils import timezone
    from datetime import timedelta

    if now is None:
        now = timezone.now()

    if listing.availability_status != Listing.AvailabilityStatus.AVAILABLE:
        return "normal"

    days = getattr(settings, "LISTING_AVAILABILITY_FRESHNESS_DAYS", 14)
    threshold = now - timedelta(days=days)

    reconfirmed_at = listing.availability_reconfirmed_at or listing.submitted_at or listing.created_at
    if reconfirmed_at < threshold:
        return "reconfirm_soon"
    return "normal"
