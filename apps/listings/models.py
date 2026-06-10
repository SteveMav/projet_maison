from pathlib import Path
from uuid import uuid4

from django.db import models
from django.db.models import Q
from django.utils import timezone

from apps.listings.validators import validate_listing_photo_upload


def listing_photo_upload_to(instance, filename):
    suffix = Path(filename).suffix.lower()
    listing_id = instance.listing_id or "unassigned"
    return f"listings/{listing_id}/{uuid4().hex}{suffix}"


class Listing(models.Model):
    class AvailabilityStatus(models.TextChoices):
        AVAILABLE = "available", "Available"
        UNAVAILABLE = "unavailable", "Unavailable"
        UNDER_REVIEW = "under_review", "Under review"

    class Currency(models.TextChoices):
        USD = "USD", "USD"

    commissionnaire_profile = models.ForeignKey(
        "commissionnaires.CommissionnaireProfile",
        on_delete=models.PROTECT,
        related_name="listings",
    )
    monthly_price_amount = models.PositiveIntegerField()
    monthly_price_currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.USD,
    )
    commune = models.CharField(max_length=120)
    bedroom_count = models.PositiveSmallIntegerField()
    description = models.TextField()
    availability_status = models.CharField(
        max_length=32,
        choices=AvailabilityStatus.choices,
        default=AvailabilityStatus.UNDER_REVIEW,
    )
    submitted_at = models.DateTimeField(default=timezone.now)
    availability_changed_at = models.DateTimeField(default=timezone.now)
    availability_reconfirmed_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "id"]
        indexes = [
            models.Index(
                fields=["availability_status", "-updated_at"],
                name="listing_status_recent_idx",
            ),
            models.Index(
                fields=["availability_status", "-availability_reconfirmed_at"],
                name="listing_status_reconfirmed_idx",
            ),
            models.Index(
                fields=["availability_status", "-availability_changed_at"],
                name="listing_status_changed_idx",
            ),
            models.Index(fields=["commune"], name="listing_commune_idx"),
            models.Index(fields=["bedroom_count"], name="listing_bedrooms_idx"),
            models.Index(fields=["monthly_price_amount"], name="listing_price_idx"),
        ]

    def __str__(self):
        return f"{self.commune} - {self.monthly_price_amount} {self.monthly_price_currency}"

    def get_primary_photo(self):
        explicit_primary = (
            self.photos.filter(is_primary=True).order_by("position", "id").first()
        )
        if explicit_primary:
            return explicit_primary
        return self.photos.order_by("position", "id").first()


class ListingPhoto(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    image = models.ImageField(
        upload_to=listing_photo_upload_to,
        validators=[validate_listing_photo_upload],
    )
    position = models.PositiveSmallIntegerField(default=0)
    is_primary = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=180, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["position", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["listing", "position"],
                name="unique_listing_photo_position",
            ),
            models.UniqueConstraint(
                fields=["listing"],
                condition=Q(is_primary=True),
                name="unique_primary_photo_per_listing",
            ),
        ]

    def __str__(self):
        return f"Photo {self.position} for listing {self.listing_id}"
