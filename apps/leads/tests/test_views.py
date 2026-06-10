from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from apps.commissionnaires.models import CommissionnaireProfile
from apps.listings.models import Listing
from apps.leads.models import Lead

class LeadViewTests(TestCase):
    def setUp(self):
        self.tenant = get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
            whatsapp_consent=True
        )
        self.owner = get_user_model().objects.create_user(
            email="owner@example.com",
            password="StrongPass123!"
        )
        self.profile = CommissionnaireProfile.objects.create(
            user=self.owner,
            display_name="Pro Owner",
            whatsapp_phone="+243990000000"
        )
        self.listing = Listing.objects.create(
            commissionnaire_profile=self.profile,
            monthly_price_amount=1200,
            commune="Gombe",
            bedroom_count=2,
            description="Appartement Gombe",
            availability_status=Listing.AvailabilityStatus.AVAILABLE
        )
        self.url = reverse("leads:create_lead", kwargs={"listing_id": self.listing.id})

    def test_endpoint_requires_authentication(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302) # redirect to login

    def test_post_success(self):
        self.client.force_login(self.tenant)
        response = self.client.post(self.url, {
            "acquisition_context": '{"source": "test"}'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("lead_id", data)
        self.assertEqual(Lead.objects.count(), 1)

    def test_invalid_method_returns_405(self):
        self.client.force_login(self.tenant)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_post_unavailable_listing_returns_400(self):
        self.listing.availability_status = Listing.AvailabilityStatus.UNAVAILABLE
        self.listing.save()

        self.client.force_login(self.tenant)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], "Cette annonce n'est plus disponible.")
        self.assertNotIn("whatsapp_url", data)


    def test_post_success_returns_whatsapp_url(self):
        self.client.force_login(self.tenant)
        response = self.client.post(self.url, {
            "acquisition_context": '{"source": "test"}'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("whatsapp_url", data)
        self.assertTrue(data["whatsapp_url"].startswith("https://wa.me/243990000000"))

    def test_post_without_consent_returns_400(self):
        self.tenant.whatsapp_consent = False
        self.tenant.save()

        self.client.force_login(self.tenant)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], "Le consentement WhatsApp est requis pour cette action.")

    def test_frontend_accessibility_markup(self):
        self.client.force_login(self.tenant)
        response = self.client.get(reverse("listings:detail", kwargs={"pk": self.listing.id}))
        self.assertEqual(response.status_code, 200)
        
        # Check error container in CTA
        self.assertContains(response, 'id="handoff-error-cta"')
        self.assertContains(response, 'role="alert"')
        self.assertContains(response, 'aria-live="polite"')
        self.assertContains(response, '⚠️')

        # Check success container in CTA
        self.assertContains(response, 'id="handoff-success-cta"')
        self.assertContains(response, '✓')

        # Check error container in modal
        self.assertContains(response, 'id="handoff-error-modal"')

