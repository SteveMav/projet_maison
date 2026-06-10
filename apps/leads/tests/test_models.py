from django.contrib.auth import get_user_model
from django.test import TestCase
from apps.commissionnaires.models import CommissionnaireProfile
from apps.listings.models import Listing
from apps.leads.models import Lead, LeadStatusEvent

class LeadModelTests(TestCase):
    def setUp(self):
        self.tenant = get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!"
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

    def test_create_lead_with_default_values(self):
        lead = Lead.objects.create(
            tenant=self.tenant,
            listing=self.listing,
            commissionnaire_profile=self.profile,
            acquisition_context={"source": "direct"}
        )
        self.assertEqual(lead.tenant, self.tenant)
        self.assertEqual(lead.listing, self.listing)
        self.assertEqual(lead.commissionnaire_profile, self.profile)
        self.assertEqual(lead.acquisition_context, {"source": "direct"})
        self.assertIsNotNone(lead.created_at)

    def test_create_lead_status_event(self):
        lead = Lead.objects.create(
            tenant=self.tenant,
            listing=self.listing,
            commissionnaire_profile=self.profile
        )
        event = LeadStatusEvent.objects.create(
            lead=lead,
            status="new"
        )
        self.assertEqual(event.lead, lead)
        self.assertEqual(event.status, "new")
        self.assertIsNotNone(event.changed_at)

    def test_create_whatsapp_handoff_attempt(self):
        lead = Lead.objects.create(
            tenant=self.tenant,
            listing=self.listing,
            commissionnaire_profile=self.profile
        )
        from apps.leads.models import WhatsAppHandoffAttempt
        attempt = WhatsAppHandoffAttempt.objects.create(
            lead=lead
        )
        self.assertEqual(attempt.lead, lead)
        self.assertIsNotNone(attempt.attempted_at)
        self.assertEqual(lead.handoff_attempts.count(), 1)

