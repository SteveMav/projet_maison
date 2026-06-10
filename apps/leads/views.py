import json
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from apps.listings.models import Listing
from apps.leads.services import create_lead_for_listing

@login_required
def create_lead_endpoint(request, listing_id):
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "error": "Méthode non autorisée."},
            status=405
        )

    listing = get_object_or_404(Listing, id=listing_id)
    
    # Parse acquisition context if provided in POST
    acquisition_context = {}
    context_raw = request.POST.get("acquisition_context")
    if context_raw:
        try:
            acquisition_context = json.loads(context_raw)
        except json.JSONDecodeError:
            pass

    try:
        lead = create_lead_for_listing(
            tenant=request.user,
            listing=listing,
            acquisition_context=acquisition_context
        )
        from apps.leads.services import generate_whatsapp_handoff_url
        whatsapp_url = generate_whatsapp_handoff_url(lead=lead)
        return JsonResponse({
            "success": True,
            "lead_id": lead.id,
            "whatsapp_url": whatsapp_url
        })
    except ValidationError as e:
        return JsonResponse({
            "success": False,
            "error": e.messages[0] if hasattr(e, "messages") else str(e)
        }, status=400)
