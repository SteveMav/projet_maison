from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from apps.commissionnaires.models import CommissionnaireProfile
from apps.listings.models import Listing, ListingPhoto
from apps.listings.selectors import (
    filter_public_listings,
    get_listing_primary_photo,
    get_public_browse_listings,
)
from apps.listings.services import create_listing


class PublicBrowseListingSelectorTests(TestCase):
    def create_profile(self, email=None):
        if email is None:
            email = f"pro{get_user_model().objects.count() + 1}@example.com"
        user = get_user_model().objects.create_user(
            email=email,
            password="StrongPass123!",
            whatsapp_phone="+243990000000",
        )
        return CommissionnaireProfile.objects.create(
            user=user,
            display_name="Maison Pro",
            whatsapp_phone="+243990000000",
        )

    def create_listing(self, *, profile=None, **overrides):
        data = {
            "commissionnaire_profile": profile or self.create_profile(),
            "monthly_price_amount": 1200,
            "commune": "Gombe",
            "bedroom_count": 2,
            "description": "Appartement lumineux proche des services.",
        }
        data.update(overrides)
        return create_listing(**data)

    def add_photo(self, listing, *, position=0, is_primary=False, name="photo.jpg"):
        return ListingPhoto.objects.create(
            listing=listing,
            image=f"listings/{listing.pk}/{name}",
            position=position,
            is_primary=is_primary,
            alt_text=f"Photo {position}",
        )

    def test_public_browse_returns_only_available_listings(self):
        available = self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
        )
        self.create_listing(
            availability_status=Listing.AvailabilityStatus.UNAVAILABLE,
        )
        self.create_listing(
            availability_status=Listing.AvailabilityStatus.UNDER_REVIEW,
        )

        listings = list(get_public_browse_listings())

        self.assertEqual(listings, [available])

    def test_public_browse_orders_by_recency_then_id_descending(self):
        submitted_at = timezone.now()
        older = self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
            submitted_at=submitted_at - timezone.timedelta(days=1),
        )
        first_tie = self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
            submitted_at=submitted_at,
        )
        second_tie = self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
            submitted_at=submitted_at,
        )

        listings = list(get_public_browse_listings())

        self.assertEqual(listings, [second_tie, first_tie, older])

    def test_public_browse_prefetches_card_photo_and_profile_data(self):
        profile = self.create_profile()
        for index in range(3):
            listing = self.create_listing(
                profile=profile,
                availability_status=Listing.AvailabilityStatus.AVAILABLE,
                submitted_at=timezone.now() + timezone.timedelta(minutes=index),
            )
            self.add_photo(
                listing,
                position=1,
                is_primary=False,
                name=f"secondary-{index}.jpg",
            )
            self.add_photo(
                listing,
                position=2,
                is_primary=True,
                name=f"primary-{index}.jpg",
            )

        with self.assertNumQueries(2):
            listings = list(get_public_browse_listings())

        with self.assertNumQueries(0):
            primary_photos = [get_listing_primary_photo(listing) for listing in listings]
            display_names = [
                listing.commissionnaire_profile.display_name for listing in listings
            ]

        self.assertEqual(display_names, ["Maison Pro", "Maison Pro", "Maison Pro"])
        self.assertTrue(all(photo.is_primary for photo in primary_photos))

    def test_filter_public_listings_without_filters_returns_available_listings(self):
        available = self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
        )
        self.create_listing(
            availability_status=Listing.AvailabilityStatus.UNAVAILABLE,
        )

        listings = list(filter_public_listings({}))

        self.assertEqual(listings, [available])

    def test_filter_public_listings_filters_by_commune_case_insensitively(self):
        matching = self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
            commune="Ngaliema",
        )
        self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
            commune="Gombe",
        )

        listings = list(filter_public_listings({"commune": "ngaliema"}))

        self.assertEqual(listings, [matching])

    def test_filter_public_listings_filters_by_budget_range(self):
        within_range = self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
            monthly_price_amount=900,
        )
        self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
            monthly_price_amount=400,
        )
        self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
            monthly_price_amount=1600,
        )

        listings = list(
            filter_public_listings({"budget_min": 500, "budget_max": 1500})
        )

        self.assertEqual(listings, [within_range])

    def test_filter_public_listings_filters_by_bedroom_minimum(self):
        matching = self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
            bedroom_count=3,
        )
        self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
            bedroom_count=1,
        )

        listings = list(filter_public_listings({"bedrooms_min": 2}))

        self.assertEqual(listings, [matching])

    def test_filter_public_listings_combines_filters_with_and_semantics(self):
        matching = self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
            commune="Ngaliema",
            monthly_price_amount=1000,
            bedroom_count=3,
        )
        self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
            commune="Ngaliema",
            monthly_price_amount=1800,
            bedroom_count=3,
        )
        self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
            commune="Gombe",
            monthly_price_amount=1000,
            bedroom_count=3,
        )
        self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
            commune="Ngaliema",
            monthly_price_amount=1000,
            bedroom_count=1,
        )

        listings = list(
            filter_public_listings(
                {
                    "commune": "Ngaliema",
                    "budget_min": 800,
                    "budget_max": 1200,
                    "bedrooms_min": 2,
                }
            )
        )

        self.assertEqual(listings, [matching])

    def test_filter_public_listings_keeps_unavailable_and_under_review_excluded(self):
        available = self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
            commune="Ngaliema",
            monthly_price_amount=1000,
            bedroom_count=2,
        )
        self.create_listing(
            availability_status=Listing.AvailabilityStatus.UNAVAILABLE,
            commune="Ngaliema",
            monthly_price_amount=1000,
            bedroom_count=2,
        )
        self.create_listing(
            availability_status=Listing.AvailabilityStatus.UNDER_REVIEW,
            commune="Ngaliema",
            monthly_price_amount=1000,
            bedroom_count=2,
        )

        listings = list(
            filter_public_listings(
                {
                    "commune": "Ngaliema",
                    "budget_min": 800,
                    "budget_max": 1200,
                    "bedrooms_min": 2,
                }
            )
        )

        self.assertEqual(listings, [available])
