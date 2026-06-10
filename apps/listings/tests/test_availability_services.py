from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.test import TestCase, override_settings
from django.utils import timezone
from apps.commissionnaires.models import CommissionnaireProfile
from apps.listings.models import Listing
from apps.listings.services import (
    create_listing,
    update_listing_availability,
    reconfirm_listing_availability,
)
from apps.listings.selectors import (
    get_commissionnaire_inventory,
    get_availability_freshness_state,
    get_public_browse_listings,
)
from apps.audit.models import AuditEvent


class AvailabilityServicesTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user1 = self.User.objects.create_user(
            email="comm1@maison.com", whatsapp_phone="+243990000001", password="password1"
        )
        self.user2 = self.User.objects.create_user(
            email="comm2@maison.com", whatsapp_phone="+243990000002", password="password1"
        )

        self.profile1 = CommissionnaireProfile.objects.create(
            user=self.user1, display_name="Comm 1", whatsapp_phone="+243990000001"
        )
        self.profile2 = CommissionnaireProfile.objects.create(
            user=self.user2, display_name="Comm 2", whatsapp_phone="+243990000002"
        )

        # Create listing for profile 1
        self.listing = create_listing(
            commissionnaire_profile=self.profile1,
            monthly_price_amount=1000,
            commune="Gombe",
            bedroom_count=3,
            description="Appartement spacieux a Gombe.",
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
        )

    def test_listing_availability_timestamps_exist_and_set_on_creation(self):
        self.assertIsNotNone(self.listing.availability_changed_at)
        self.assertIsNotNone(self.listing.availability_reconfirmed_at)

    def test_update_listing_availability_success(self):
        # Change status from AVAILABLE to UNAVAILABLE
        updated_listing = update_listing_availability(
            profile=self.profile1,
            listing_id=self.listing.id,
            actor=self.user1,
            new_status=Listing.AvailabilityStatus.UNAVAILABLE,
        )
        self.assertEqual(updated_listing.availability_status, Listing.AvailabilityStatus.UNAVAILABLE)
        
        # Verify AuditEvent was created
        audit = AuditEvent.objects.first()
        self.assertEqual(audit.event_type, "listing.availability_changed")
        self.assertEqual(audit.actor, self.user1)
        self.assertEqual(int(audit.target_id), self.listing.id)
        self.assertEqual(audit.metadata["previous_status"], Listing.AvailabilityStatus.AVAILABLE)
        self.assertEqual(audit.metadata["new_status"], Listing.AvailabilityStatus.UNAVAILABLE)

    def test_update_listing_availability_to_available_refreshes_reconfirmed_at(self):
        # Set availability to unavailable
        update_listing_availability(
            profile=self.profile1,
            listing_id=self.listing.id,
            actor=self.user1,
            new_status=Listing.AvailabilityStatus.UNAVAILABLE,
        )
        
        # Let's override availability_reconfirmed_at to be in past
        past_time = timezone.now() - timedelta(days=20)
        self.listing.availability_reconfirmed_at = past_time
        self.listing.save(update_fields=["availability_reconfirmed_at"])
        
        # Change back to available
        updated = update_listing_availability(
            profile=self.profile1,
            listing_id=self.listing.id,
            actor=self.user1,
            new_status=Listing.AvailabilityStatus.AVAILABLE,
        )
        self.assertGreater(updated.availability_reconfirmed_at, past_time)

    def test_reconfirm_listing_availability(self):
        past_time = timezone.now() - timedelta(days=20)
        self.listing.availability_reconfirmed_at = past_time
        self.listing.save(update_fields=["availability_reconfirmed_at"])

        reconfirmed = reconfirm_listing_availability(
            profile=self.profile1,
            listing_id=self.listing.id,
            actor=self.user1,
        )
        self.assertGreater(reconfirmed.availability_reconfirmed_at, past_time)

        # Verify AuditEvent was created
        audit = AuditEvent.objects.first()
        self.assertEqual(audit.event_type, "listing.availability_reconfirmed")
        self.assertEqual(audit.actor, self.user1)

    def test_reconfirm_unavailable_listing_is_blocked(self):
        update_listing_availability(
            profile=self.profile1,
            listing_id=self.listing.id,
            actor=self.user1,
            new_status=Listing.AvailabilityStatus.UNAVAILABLE,
        )
        with self.assertRaises(ValidationError):
            reconfirm_listing_availability(
                profile=self.profile1,
                listing_id=self.listing.id,
                actor=self.user1,
            )

    def test_update_other_commissionnaire_listing_is_denied(self):
        with self.assertRaises(PermissionDenied):
            update_listing_availability(
                profile=self.profile2,
                listing_id=self.listing.id,
                actor=self.user2,
                new_status=Listing.AvailabilityStatus.UNAVAILABLE,
            )

    def test_reconfirm_other_commissionnaire_listing_is_denied(self):
        with self.assertRaises(PermissionDenied):
            reconfirm_listing_availability(
                profile=self.profile2,
                listing_id=self.listing.id,
                actor=self.user2,
            )

    @override_settings(LISTING_AVAILABILITY_FRESHNESS_DAYS=5)
    def test_freshness_threshold(self):
        self.assertEqual(get_availability_freshness_state(self.listing), "normal")
        
        # Make reconfirmed_at older than 5 days
        self.listing.availability_reconfirmed_at = timezone.now() - timedelta(days=6)
        self.listing.save(update_fields=["availability_reconfirmed_at"])
        
        self.assertEqual(get_availability_freshness_state(self.listing), "reconfirm_soon")

    def test_public_browse_excludes_unavailable(self):
        # Available is included
        self.assertIn(self.listing, get_public_browse_listings())
        
        # Change to unavailable
        update_listing_availability(
            profile=self.profile1,
            listing_id=self.listing.id,
            actor=self.user1,
            new_status=Listing.AvailabilityStatus.UNAVAILABLE,
        )
        
        self.assertNotIn(self.listing, get_public_browse_listings())
