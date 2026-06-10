from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from apps.commissionnaires.models import CommissionnaireProfile
from apps.listings.models import Listing
from apps.listings.services import create_listing


class InventoryViewsTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.owner_user = self.User.objects.create_user(
            email="owner@example.com",
            password="StrongPass123!",
            whatsapp_phone="+243990000001",
        )
        self.owner_profile = CommissionnaireProfile.objects.create(
            user=self.owner_user,
            display_name="Owner Pro",
            whatsapp_phone="+243990000001",
        )

        self.other_user = self.User.objects.create_user(
            email="other@example.com",
            password="StrongPass123!",
            whatsapp_phone="+243990000002",
        )
        self.other_profile = CommissionnaireProfile.objects.create(
            user=self.other_user,
            display_name="Other Pro",
            whatsapp_phone="+243990000002",
        )

        # Create listing for owner
        self.listing = create_listing(
            commissionnaire_profile=self.owner_profile,
            monthly_price_amount=1500,
            commune="Gombe",
            bedroom_count=2,
            description="Appartement a louer.",
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
        )

    def test_listing_inventory_requires_authentication(self):
        response = self.client.get(reverse("commissionnaires:listing_inventory"))
        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('commissionnaires:listing_inventory')}",
        )

    def test_user_without_whatsapp_phone_routed_to_phone_completion(self):
        user = self.User.objects.create_user(
            email="nophone@example.com", password="StrongPass123!", whatsapp_phone=""
        )
        self.client.force_login(user)
        response = self.client.get(reverse("commissionnaires:listing_inventory"))
        self.assertRedirects(
            response,
            f"{reverse('accounts:phone_complete')}?next={reverse('commissionnaires:listing_inventory')}",
            fetch_redirect_response=False,
        )

    def test_user_without_commissionnaire_profile_redirects_to_profile_create(self):
        user = self.User.objects.create_user(
            email="noprofile@example.com", password="StrongPass123!", whatsapp_phone="+243990000003"
        )
        self.client.force_login(user)
        response = self.client.get(reverse("commissionnaires:listing_inventory"))
        self.assertRedirects(
            response,
            f"{reverse('commissionnaires:profile_create')}?next={reverse('commissionnaires:listing_inventory')}",
        )

    def test_owner_sees_only_their_listings(self):
        self.client.force_login(self.owner_user)
        
        # Create a listing for the other profile
        other_listing = create_listing(
            commissionnaire_profile=self.other_profile,
            monthly_price_amount=2000,
            commune="Ngaliema",
            bedroom_count=3,
            description="Maison chic.",
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
        )
        
        response = self.client.get(reverse("commissionnaires:listing_inventory"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.listing.commune)
        self.assertNotContains(response, other_listing.commune)

    @override_settings(LISTING_AVAILABILITY_FRESHNESS_DAYS=5)
    def test_inventory_renders_different_states(self):
        self.client.force_login(self.owner_user)
        
        # 1. AVAILABLE FRESH
        response = self.client.get(reverse("commissionnaires:listing_inventory"))
        self.assertContains(response, 'data-status-hook="available"')
        
        # 2. RECONFIRM SOON
        self.listing.availability_reconfirmed_at = timezone.now() - timedelta(days=6)
        self.listing.save()
        response = self.client.get(reverse("commissionnaires:listing_inventory"))
        self.assertContains(response, 'data-status-hook="reconfirm-soon"')

        # 3. UNAVAILABLE
        self.listing.availability_status = Listing.AvailabilityStatus.UNAVAILABLE
        self.listing.save()
        response = self.client.get(reverse("commissionnaires:listing_inventory"))
        self.assertContains(response, 'data-status-hook="unavailable"')

        # 4. UNDER REVIEW
        self.listing.availability_status = Listing.AvailabilityStatus.UNDER_REVIEW
        self.listing.save()
        response = self.client.get(reverse("commissionnaires:listing_inventory"))
        self.assertContains(response, 'data-status-hook="under-review"')

    def test_post_update_availability(self):
        self.client.force_login(self.owner_user)
        
        # Make unavailable
        url = reverse("commissionnaires:listing_availability", args=[self.listing.pk])
        response = self.client.post(url, {"availability_status": "unavailable"})
        self.assertRedirects(response, reverse("commissionnaires:listing_inventory"))
        
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.availability_status, Listing.AvailabilityStatus.UNAVAILABLE)

        # Make available
        response = self.client.post(url, {"availability_status": "available"})
        self.assertRedirects(response, reverse("commissionnaires:listing_inventory"))
        
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.availability_status, Listing.AvailabilityStatus.AVAILABLE)

    def test_post_reconfirm_availability(self):
        self.client.force_login(self.owner_user)
        past_time = timezone.now() - timedelta(days=10)
        self.listing.availability_reconfirmed_at = past_time
        self.listing.save()

        url = reverse("commissionnaires:listing_reconfirm", args=[self.listing.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse("commissionnaires:listing_inventory"))
        
        self.listing.refresh_from_db()
        self.assertGreater(self.listing.availability_reconfirmed_at, past_time)

    def test_unowned_listing_post_update_denied(self):
        self.client.force_login(self.other_user)
        url = reverse("commissionnaires:listing_availability", args=[self.listing.pk])
        response = self.client.post(url, {"availability_status": "unavailable"})
        self.assertEqual(response.status_code, 403)

    def test_unowned_listing_post_reconfirm_denied(self):
        self.client.force_login(self.other_user)
        url = reverse("commissionnaires:listing_reconfirm", args=[self.listing.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_get_requests_do_not_change_availability(self):
        self.client.force_login(self.owner_user)
        url = reverse("commissionnaires:listing_reconfirm", args=[self.listing.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)
