from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.commissionnaires.models import CommissionnaireProfile
from apps.listings.models import Listing, ListingPhoto
from apps.listings.services import create_listing


class DetailAccessibilityTests(TestCase):
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

    def test_accessibility_hooks_and_attributes(self):
        listing = self.create_listing()
        ListingPhoto.objects.create(listing=listing, image="p1.jpg", position=0)
        ListingPhoto.objects.create(listing=listing, image="p2.jpg", position=1)

        url = reverse("listings:detail", kwargs={"pk": listing.pk})
        response = self.client.get(url)

        self.assertContains(response, 'data-close-drawer')
        self.assertContains(response, 'aria-label="Fermer"')

        self.assertContains(response, 'type="button"')
        self.assertContains(response, 'data-gallery-thumb')
        self.assertContains(response, 'aria-label="Afficher la photo 1 de 2"')
        self.assertContains(response, 'aria-label="Afficher la photo 2 de 2"')

        browse_url = reverse("listings:browse")
        browse_response = self.client.get(browse_url)
        self.assertContains(browse_response, 'id="detail-drawer"')
        self.assertContains(browse_response, 'class="detail-drawer"')
        self.assertContains(browse_response, 'aria-label="Détail de l\'annonce"')
