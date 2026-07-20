from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone

from apps.commissionnaires.models import CommissionnaireProfile
from apps.listings.models import Listing, ListingPhoto
from apps.listings.services import create_listing


class PublicBrowseViewTests(TestCase):
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
            "submitted_at": timezone.now(),
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

    def test_anonymous_user_can_load_public_browse(self):
        response = self.client.get(reverse("listings:browse"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "listings/browse.html")

    def test_public_browse_context_contains_only_available_listings(self):
        available = self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
        )
        self.create_listing(
            availability_status=Listing.AvailabilityStatus.UNAVAILABLE,
        )
        self.create_listing(
            availability_status=Listing.AvailabilityStatus.UNDER_REVIEW,
        )

        response = self.client.get(reverse("listings:browse"))

        self.assertEqual(list(response.context["listings"]), [available])

    def test_public_browse_paginates_results(self):
        profile = self.create_profile()
        for index in range(13):
            self.create_listing(
                profile=profile,
                availability_status=Listing.AvailabilityStatus.AVAILABLE,
                submitted_at=timezone.now() + timezone.timedelta(minutes=index),
            )

        response = self.client.get(reverse("listings:browse"))

        self.assertEqual(response.context["paginator"].per_page, 12)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["listings"]), 12)

    def test_detail_route_name_is_available_for_card_navigation(self):
        listing = self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
        )

        response = self.client.get(reverse("listings:detail", kwargs={"pk": listing.pk}))

        self.assertEqual(response.status_code, 200)

    def test_public_browse_page_uses_bounded_queries_for_cards_with_photos(self):
        profile = self.create_profile()
        for index in range(12):
            listing = self.create_listing(
                profile=profile,
                availability_status=Listing.AvailabilityStatus.AVAILABLE,
                submitted_at=timezone.now() + timezone.timedelta(minutes=index),
            )
            self.add_photo(listing, position=0, is_primary=False, name=f"secondary-{index}.jpg")
            self.add_photo(listing, position=1, is_primary=True, name=f"primary-{index}.jpg")

        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("listings:browse"))

        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(queries), 4)

    def test_filtered_browse_page_uses_bounded_queries_for_cards_with_photos(self):
        profile = self.create_profile()
        for index in range(12):
            listing = self.create_listing(
                profile=profile,
                availability_status=Listing.AvailabilityStatus.AVAILABLE,
                commune="Ngaliema",
                monthly_price_amount=900,
                bedroom_count=2,
                submitted_at=timezone.now() + timezone.timedelta(minutes=index),
            )
            self.add_photo(listing, position=0, is_primary=False, name=f"secondary-{index}.jpg")
            self.add_photo(listing, position=1, is_primary=True, name=f"primary-{index}.jpg")
        self.create_listing(
            profile=profile,
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
            commune="Gombe",
            monthly_price_amount=900,
            bedroom_count=2,
        )

        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(
                reverse("listings:browse"),
                {
                    "commune": "Ngaliema",
                    "budget_min": "800",
                    "budget_max": "1200",
                    "bedrooms_min": "2",
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(queries), 4)

    def test_public_browse_applies_valid_combined_filters(self):
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
            availability_status=Listing.AvailabilityStatus.UNDER_REVIEW,
            commune="Ngaliema",
            monthly_price_amount=1000,
            bedroom_count=3,
        )

        response = self.client.get(
            reverse("listings:browse"),
            {
                "commune": "Ngaliema",
                "budget_min": "800",
                "budget_max": "1200",
                "bedrooms_min": "2",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["filter_form"].is_valid())
        self.assertEqual(list(response.context["listings"]), [matching])
        self.assertEqual(response.context["result_count"], 1)

    def test_city_alias_filter_keeps_catalogue_visible(self):
        listing = self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
            commune="Ngaliema",
        )

        response = self.client.get(reverse("listings:browse"), {"commune": "Kinshasa"})

        self.assertTrue(response.context["filter_form"].is_valid())
        self.assertEqual(response.context["active_filters"], {})
        self.assertEqual(list(response.context["listings"]), [listing])

    def test_commune_filter_also_matches_neighborhood(self):
        listing = self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
            commune="Ngaliema",
            neighborhood="Ma Campagne",
        )

        response = self.client.get(
            reverse("listings:browse"),
            {"commune": "Campagne"},
        )

        self.assertTrue(response.context["filter_form"].is_valid())
        self.assertEqual(list(response.context["listings"]), [listing])

    def test_invalid_filter_values_show_form_errors_without_crashing(self):
        available = self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
        )

        response = self.client.get(
            reverse("listings:browse"),
            {"budget_min": "cheap", "bedrooms_min": "-1"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["filter_form"].is_valid())
        self.assertIn("budget_min", response.context["filter_form"].errors)
        self.assertIn("bedrooms_min", response.context["filter_form"].errors)
        self.assertEqual(list(response.context["listings"]), [available])
        self.assertEqual(response.context["active_filters"], {})

    def test_budget_max_less_than_min_shows_form_error(self):
        response = self.client.get(
            reverse("listings:browse"),
            {"budget_min": "1500", "budget_max": "500"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["filter_form"].is_valid())
        self.assertIn("budget_max", response.context["filter_form"].errors)

    def test_active_filter_chips_remove_one_filter_and_drop_page(self):
        profile = self.create_profile()
        for index in range(25):
            self.create_listing(
                profile=profile,
                availability_status=Listing.AvailabilityStatus.AVAILABLE,
                commune="Ngaliema",
                monthly_price_amount=800,
                bedroom_count=2,
                submitted_at=timezone.now() + timezone.timedelta(minutes=index),
            )

        response = self.client.get(
            reverse("listings:browse"),
            {
                "commune": "Ngaliema",
                "budget_min": "500",
                "bedrooms_min": "2",
                "page": "3",
            },
        )

        chips = {
            chip["param"]: chip["url"]
            for chip in response.context["active_filter_chips"]
        }

        self.assertEqual(
            chips,
            {
                "commune": "/annonces/?budget_min=500&bedrooms_min=2",
                "budget_min": "/annonces/?commune=Ngaliema&bedrooms_min=2",
                "bedrooms_min": "/annonces/?commune=Ngaliema&budget_min=500",
            },
        )
        self.assertEqual(response.context["clear_filters_url"], "/annonces/")

    def test_pagination_links_preserve_active_filters(self):
        profile = self.create_profile()
        for index in range(13):
            self.create_listing(
                profile=profile,
                availability_status=Listing.AvailabilityStatus.AVAILABLE,
                commune="Ngaliema",
                submitted_at=timezone.now() + timezone.timedelta(minutes=index),
            )

        response = self.client.get(
            reverse("listings:browse"),
            {"commune": "Ngaliema"},
        )

        self.assertEqual(
            response.context["pagination_urls"]["next"],
            "/annonces/?commune=Ngaliema&page=2",
        )
        self.assertIsNone(response.context["pagination_urls"]["previous"])

    def test_filter_partial_response_uses_json_envelope(self):
        matching = self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
            commune="Ngaliema",
        )
        self.create_listing(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
            commune="Gombe",
        )

        response = self.client.get(
            reverse("listings:browse"),
            {"commune": "Ngaliema"},
            headers={"X-Maison-Partial": "filters"},
        )

        payload = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["ok"], True)
        self.assertIn("data", payload)
        self.assertIn("results_html", payload["data"])
        self.assertIn("chips_html", payload["data"])
        self.assertEqual(payload["data"]["result_count"], 1)
        self.assertEqual(payload["data"]["result_count_text"], "1 annonce trouvée")
        self.assertEqual(payload["data"]["url"], "/annonces/?commune=Ngaliema")
        self.assertIn(str(matching.pk), payload["data"]["results_html"])
        self.assertNotIn("<!doctype html>", payload["data"]["results_html"].lower())

    def test_invalid_filter_partial_response_uses_error_envelope(self):
        response = self.client.get(
            reverse("listings:browse"),
            {"budget_min": "cheap"},
            headers={"X-Maison-Partial": "filters"},
        )

        payload = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(payload["ok"], False)
        self.assertIn("error", payload)
        self.assertIn("budget_min", payload["error"]["fields"])
