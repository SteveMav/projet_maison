from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from apps.accounts.forms import LightweightIdentificationForm

class LightweightIdentificationFormTests(TestCase):
    def test_form_validation_valid_data(self):
        form = LightweightIdentificationForm(data={
            "first_name": "Jean",
            "last_name": "Dupont",
            "whatsapp_phone": "0990000000",
            "consent": True
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["whatsapp_phone"], "+243990000000")

    def test_form_validation_missing_fields(self):
        form = LightweightIdentificationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)
        self.assertIn("last_name", form.errors)
        self.assertIn("whatsapp_phone", form.errors)
        self.assertIn("consent", form.errors)

    def test_form_validation_invalid_phone(self):
        form = LightweightIdentificationForm(data={
            "first_name": "Jean",
            "last_name": "Dupont",
            "whatsapp_phone": "not-a-phone",
            "consent": True
        })
        self.assertFalse(form.is_valid())
        self.assertIn("whatsapp_phone", form.errors)

    def test_form_validation_missing_consent(self):
        form = LightweightIdentificationForm(data={
            "first_name": "Jean",
            "last_name": "Dupont",
            "whatsapp_phone": "0990000000",
            "consent": False
        })
        self.assertFalse(form.is_valid())
        self.assertIn("consent", form.errors)
        self.assertEqual(form.errors["consent"][0], "Vous devez cocher cette case pour continuer.")

class LightweightIdentificationEndpointTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!"
        )
        self.url = reverse("accounts:identify")

    def test_endpoint_requires_authentication(self):
        response = self.client.post(self.url, {
            "first_name": "Jean",
            "last_name": "Dupont",
            "whatsapp_phone": "0990000000",
            "consent": True
        })
        # LoginRequiredMixin redirects to settings.LOGIN_URL (which has login page)
        self.assertEqual(response.status_code, 302)

    def test_valid_post_updates_user_and_returns_success_json(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {
            "first_name": "Jean",
            "last_name": "Dupont",
            "whatsapp_phone": "0990000000",
            "consent": True
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True})
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Jean")
        self.assertEqual(self.user.last_name, "Dupont")
        self.assertEqual(self.user.whatsapp_phone, "+243990000000")
        self.assertTrue(self.user.whatsapp_consent)
        self.assertIsNotNone(self.user.whatsapp_consent_given_at)

    def test_invalid_post_returns_bad_request_with_errors_json(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {
            "first_name": "",
            "last_name": "",
            "whatsapp_phone": "not-a-phone",
            "consent": False
        })
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertIn("errors", data)
        self.assertIn("first_name", data["errors"])
        self.assertIn("last_name", data["errors"])
        self.assertIn("whatsapp_phone", data["errors"])
        self.assertIn("consent", data["errors"])


from apps.listings.models import Listing
from apps.commissionnaires.models import CommissionnaireProfile

class LightweightIdentificationPageTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!"
        )
        self.owner = get_user_model().objects.create_user(
            email="owner@example.com",
            password="StrongPass123!"
        )
        self.profile = CommissionnaireProfile.objects.create(
            user=self.owner,
            display_name="Maison Owner",
            whatsapp_phone="+243990000000",
        )
        self.listing = Listing.objects.create(
            commissionnaire_profile=self.profile,
            monthly_price_amount=1000,
            commune="Gombe",
            bedroom_count=2,
            description="Beau log.",
            availability_status=Listing.AvailabilityStatus.AVAILABLE
        )
        self.url = reverse("listings:detail", kwargs={"pk": self.listing.pk})

    def test_detail_page_contains_modal_and_cta_attributes_for_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-contact-whatsapp')
        self.assertContains(response, 'data-user-authenticated="false"')
        self.assertContains(response, 'data-id-required="false"')
        self.assertContains(response, 'id="identification-modal"')

    def test_detail_page_contains_modal_and_cta_attributes_for_authenticated_non_consented_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-contact-whatsapp')
        self.assertContains(response, 'data-user-authenticated="true"')
        self.assertContains(response, 'data-id-required="true"')
        self.assertContains(response, 'id="identification-modal"')

    def test_detail_page_contains_modal_and_cta_attributes_for_authenticated_consented_user(self):
        self.user.whatsapp_consent = True
        self.user.save()
        
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-contact-whatsapp')
        self.assertContains(response, 'data-user-authenticated="true"')
        self.assertContains(response, 'data-id-required="false"')
        self.assertContains(response, 'id="identification-modal"')
