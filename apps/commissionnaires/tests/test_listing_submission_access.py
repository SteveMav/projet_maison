from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.commissionnaires.models import CommissionnaireProfile
from apps.listings.models import Listing


class ListingSubmissionAccessTests(TestCase):
    def create_user(self, email="pro@example.com", whatsapp_phone="+243990000000"):
        return get_user_model().objects.create_user(
            email=email,
            password="StrongPass123!",
            whatsapp_phone=whatsapp_phone,
        )

    def test_listing_submission_requires_authentication(self):
        response = self.client.get(reverse("commissionnaires:listing_submit"))
        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('commissionnaires:listing_submit')}",
        )

    def test_user_without_whatsapp_phone_routed_to_phone_completion(self):
        user = self.create_user(whatsapp_phone="")
        self.client.force_login(user)

        response = self.client.get(reverse("commissionnaires:listing_submit"))
        self.assertRedirects(
            response,
            f"{reverse('accounts:phone_complete')}?next={reverse('commissionnaires:listing_submit')}",
            fetch_redirect_response=False,
        )

    def test_user_without_commissionnaire_profile_redirects_to_profile_create(self):
        user = self.create_user()
        self.client.force_login(user)

        response = self.client.get(reverse("commissionnaires:listing_submit"))
        self.assertRedirects(
            response,
            f"{reverse('commissionnaires:profile_create')}?next={reverse('commissionnaires:listing_submit')}",
        )

    def test_user_with_ineligible_profile_redirects_to_profile_edit(self):
        user = self.create_user()
        self.client.force_login(user)
        # Create an ineligible profile with display name empty after trimming
        profile = CommissionnaireProfile.objects.create(
            user=user,
            display_name="  ",
            whatsapp_phone="+243990000000",
        )
        self.assertFalse(profile.is_publication_eligible)

        response = self.client.get(reverse("commissionnaires:listing_submit"))
        self.assertRedirects(
            response,
            f"{reverse('commissionnaires:profile_edit', args=[profile.pk])}?next={reverse('commissionnaires:listing_submit')}",
            fetch_redirect_response=False,
        )

    def test_eligible_commissionnaire_can_access_form(self):
        user = self.create_user()
        self.client.force_login(user)
        CommissionnaireProfile.objects.create(
            user=user,
            display_name="Maison Pro",
            whatsapp_phone="+243990000000",
        )

        response = self.client.get(reverse("commissionnaires:listing_submit"))
        self.assertEqual(response.status_code, 200)

    def test_cannot_access_submitted_page_of_another_commissionnaire_listing(self):
        owner = self.create_user(email="owner@example.com")
        owner_profile = CommissionnaireProfile.objects.create(
            user=owner,
            display_name="Owner Pro",
            whatsapp_phone="+243990000000",
        )
        listing = Listing.objects.create(
            commissionnaire_profile=owner_profile,
            monthly_price_amount=1000,
            commune="Gombe",
            bedroom_count=2,
            description="Superbe appartement",
        )

        intruder = self.create_user(email="intruder@example.com")
        self.client.force_login(intruder)

        # Intruder has no profile
        response = self.client.get(reverse("commissionnaires:listing_submitted", args=[listing.pk]))
        self.assertEqual(response.status_code, 404)

        # Intruder has a profile, but listing does not belong to them
        CommissionnaireProfile.objects.create(
            user=intruder,
            display_name="Intruder Pro",
            whatsapp_phone="+243990000001",
        )
        response = self.client.get(reverse("commissionnaires:listing_submitted", args=[listing.pk]))
        self.assertEqual(response.status_code, 404)
