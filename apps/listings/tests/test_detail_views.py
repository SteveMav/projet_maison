from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.commissionnaires.models import CommissionnaireProfile
from apps.listings.models import Listing
from apps.listings.services import create_listing


class DetailViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="pro@example.com",
            password="StrongPass123!",
            whatsapp_phone="+243990000000",
        )
        self.profile = CommissionnaireProfile.objects.create(
            user=self.user,
            display_name="Maison Pro",
            whatsapp_phone="+243990000000",
        )

    def create_listing(self, **overrides):
        data = {
            "commissionnaire_profile": self.profile,
            "monthly_price_amount": 1200,
            "commune": "Gombe",
            "bedroom_count": 2,
            "description": "Appartement lumineux proche des services.",
            "availability_status": Listing.AvailabilityStatus.AVAILABLE,
        }
        data.update(overrides)
        return create_listing(**data)

    def test_available_listing_detail_returns_200(self):
        listing = self.create_listing(availability_status=Listing.AvailabilityStatus.AVAILABLE)
        url = reverse("listings:detail", kwargs={"pk": listing.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "listings/detail.html")
        self.assertTemplateUsed(response, "listings/includes/detail_panel.html")

    def test_missing_listing_returns_404(self):
        url = reverse("listings:detail", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_under_review_listing_detail_returns_404(self):
        listing = self.create_listing(availability_status=Listing.AvailabilityStatus.UNDER_REVIEW)
        url = reverse("listings:detail", kwargs={"pk": listing.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_partial_response_uses_panel_only(self):
        listing = self.create_listing(availability_status=Listing.AvailabilityStatus.AVAILABLE)
        url = reverse("listings:detail", kwargs={"pk": listing.pk})
        response = self.client.get(url, HTTP_X_MAISON_PARTIAL="listing-detail")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "listings/includes/detail_panel.html")
        self.assertTemplateNotUsed(response, "listings/detail.html")
        self.assertEqual(response["Content-Type"].split(";")[0], "text/html")
