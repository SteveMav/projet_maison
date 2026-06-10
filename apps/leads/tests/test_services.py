from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from apps.commissionnaires.models import CommissionnaireProfile
from apps.listings.models import Listing
from apps.audit.models import AuditEvent
from apps.leads.models import Lead, LeadStatusEvent
from apps.leads.services import create_lead_for_listing

class LeadServiceTests(TestCase):
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

    def test_create_lead_success(self):
        lead = create_lead_for_listing(
            tenant=self.tenant,
            listing=self.listing,
            acquisition_context={"source": "test"}
        )
        self.assertEqual(lead.tenant, self.tenant)
        self.assertEqual(lead.listing, self.listing)
        self.assertEqual(lead.commissionnaire_profile, self.profile)
        self.assertEqual(lead.acquisition_context, {"source": "test"})
        
        # Verify initial status event
        self.assertEqual(lead.status_events.count(), 1)
        self.assertEqual(lead.status_events.first().status, "new")

        # Verify audit event
        self.assertEqual(AuditEvent.objects.filter(event_type="lead.created").count(), 1)
        audit = AuditEvent.objects.get(event_type="lead.created")
        self.assertEqual(audit.actor, self.tenant)
        self.assertEqual(audit.target_id, str(lead.id))

    def test_create_lead_fails_if_listing_unavailable(self):
        self.listing.availability_status = Listing.AvailabilityStatus.UNAVAILABLE
        self.listing.save()

        with self.assertRaises(ValidationError) as ctx:
            create_lead_for_listing(tenant=self.tenant, listing=self.listing)
        self.assertIn("Cette annonce n'est plus disponible.", ctx.exception.messages)

    def test_create_lead_fails_if_tenant_not_consented(self):
        self.tenant.whatsapp_consent = False
        self.tenant.save()

        with self.assertRaises(ValidationError):
            create_lead_for_listing(tenant=self.tenant, listing=self.listing)

    def test_multiple_leads_are_distinguishable(self):
        lead1 = create_lead_for_listing(tenant=self.tenant, listing=self.listing)
        lead2 = create_lead_for_listing(tenant=self.tenant, listing=self.listing)
        
        self.assertNotEqual(lead1.id, lead2.id)
        self.assertEqual(Lead.objects.count(), 2)

    def test_generate_whatsapp_handoff_url(self):
        lead = create_lead_for_listing(tenant=self.tenant, listing=self.listing)
        
        from apps.leads.services import generate_whatsapp_handoff_url
        from apps.leads.models import WhatsAppHandoffAttempt
        
        self.profile.whatsapp_phone = "+243 990 000 000"
        self.profile.save()
        
        url = generate_whatsapp_handoff_url(lead=lead)
        
        self.assertTrue(url.startswith("https://wa.me/243990000000"))
        self.assertIn(f"R%C3%A9f%20Annonce%3A%20{self.listing.id}", url)
        self.assertIn(f"R%C3%A9f%20Contact%3A%20{lead.id}", url)
        
        import urllib.parse
        parsed = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(parsed.query)
        message = query.get("text", [""])[0]
        
        self.assertNotIn("suivi", message.lower())
        self.assertNotIn("track", message.lower())
        
        self.assertEqual(WhatsAppHandoffAttempt.objects.filter(lead=lead).count(), 1)
        
        self.assertEqual(AuditEvent.objects.filter(event_type="whatsapp.handoff").count(), 1)
        audit = AuditEvent.objects.get(event_type="whatsapp.handoff")
        self.assertEqual(audit.actor, self.tenant)
        self.assertEqual(audit.target_id, str(lead.id))

