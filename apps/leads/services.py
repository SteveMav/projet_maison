from django.core.exceptions import ValidationError
from apps.leads.models import Lead, LeadStatusEvent
from apps.audit.services import create_audit_event

def create_lead_for_listing(*, tenant, listing, acquisition_context=None):
    if not tenant or not tenant.is_authenticated:
        raise ValidationError("Le locataire doit être connecté.")
    
    if not tenant.whatsapp_consent:
        raise ValidationError("Le consentement WhatsApp est requis pour cette action.")
        
    if listing.availability_status != listing.AvailabilityStatus.AVAILABLE:
        raise ValidationError("Cette annonce n'est plus disponible.")
        
    lead = Lead.objects.create(
        tenant=tenant,
        listing=listing,
        commissionnaire_profile=listing.commissionnaire_profile,
        acquisition_context=acquisition_context or {},
    )
    
    LeadStatusEvent.objects.create(
        lead=lead,
        status="new",
    )
    
    create_audit_event(
        event_type="lead.created",
        actor=tenant,
        target_id=lead.id,
        metadata={
            "listing_id": listing.id,
            "commissionnaire_profile_id": listing.commissionnaire_profile.id,
        }
    )
    
    return lead


def generate_whatsapp_handoff_url(*, lead):
    import re
    import urllib.parse
    from apps.leads.models import WhatsAppHandoffAttempt

    if not lead:
        raise ValidationError("Le lead est requis.")

    phone_raw = lead.commissionnaire_profile.whatsapp_phone
    phone = re.sub(r"\D", "", phone_raw.lstrip("+"))

    message = (
        f"Bonjour, je souhaite vous contacter au sujet de votre annonce sur Maison. "
        f"Réf Annonce: {lead.listing.id}, Réf Contact: {lead.id}."
    )

    WhatsAppHandoffAttempt.objects.create(lead=lead)

    create_audit_event(
        event_type="whatsapp.handoff",
        actor=lead.tenant,
        target_id=lead.id,
        metadata={
            "listing_id": lead.listing.id,
            "whatsapp_phone": phone_raw,
        }
    )

    encoded_message = urllib.parse.quote(message)
    return f"https://wa.me/{phone}?text={encoded_message}"

