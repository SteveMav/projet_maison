---
baseline_commit: 83de0f8f0b1584d8b991f06922f9a3af5385d75b
---

# Story 3.3: WhatsApp Handoff With Listing Context

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Tenant,
I want Maison to open WhatsApp with the right Commissionnaire and Listing context,
so that the conversation starts clearly and the Commissionnaire can identify my enquiry.

## Acceptance Criteria

1. **Given** a Lead has been created successfully, **when** Maison prepares the WhatsApp Handoff, **then** the handoff targets the WhatsApp phone number associated with the Listing's Commissionnaire Profile, **and** the generated message includes a Listing identifier and a human-readable Lead reference.
2. **Given** a Tenant confirms contact, **when** the handoff succeeds, **then** Maison opens or returns the WhatsApp deep link only after Lead creation, **and** records a handoff-attempt event separately from the Lead record.
3. **Given** the handoff message is rendered, **when** its text is inspected, **then** it does not claim Maison can track WhatsApp conversation contents, visits, negotiation, payment, or contract execution, **and** it stays concise enough for a practical WhatsApp opening message.
4. **Given** a developer validates the handoff service, **when** tests run, **then** they verify correct Commissionnaire phone targeting, Listing reference, Lead reference, URL encoding, and no handoff URL when Lead creation has failed.

## Tasks / Subtasks

- [x] Implement WhatsApp Handoff Attempt model (AC: 2)
  - [x] Add `WhatsAppHandoffAttempt` model in `apps/leads/models.py`:
    - `lead` = `ForeignKey(Lead, on_delete=models.CASCADE, related_name="handoff_attempts")`
    - `attempted_at` = `DateTimeField(auto_now_add=True)`
  - [x] Create and apply migrations: `python manage.py makemigrations leads && python manage.py migrate`
- [x] Implement WhatsApp Handoff service (AC: 1, 2, 3, 4)
  - [x] Create `generate_whatsapp_handoff_url(*, lead)` in `apps/leads/services.py`:
    - [x] Retrieve target phone number from `lead.commissionnaire_profile.whatsapp_phone`.
    - [x] Format phone number: strip '+' prefix using `.lstrip('+')` and ensure all non-digit characters are removed to conform to the `wa.me` digits-only API format.
    - [x] Generate the prefilled French message containing the listing ID and the lead reference (e.g. `Réf Annonce: {lead.listing.id}, Réf Contact: {lead.id}`).
    - [x] Ensure the message copy makes no claims of tracking the actual conversation content, visits, negotiations, payments, or contracts, and remains concise (e.g., "Bonjour, je souhaite vous contacter au sujet de votre annonce sur Maison. Réf Annonce: {listing_id}, Réf Contact: {lead_id}.").
    - [x] Create a `WhatsAppHandoffAttempt` record for the lead.
    - [x] Write a business `AuditEvent` of type `whatsapp.handoff` using `apps.audit.services.create_audit_event`.
    - [x] URL-encode the text query parameter and return the full deep link: `https://wa.me/{phone}?text={encoded_message}`.
- [x] Integrate Handoff URL in Lead Creation Endpoint (AC: 1, 2, 4)
  - [x] Update `create_lead_endpoint` in `apps/leads/views.py`:
    - [x] Call `generate_whatsapp_handoff_url(lead=lead)` after lead creation.
    - [x] Return the handoff URL in the JSON response: `{"success": true, "lead_id": lead.id, "whatsapp_url": whatsapp_url}`.
- [x] Update Frontend JavaScript Integration (AC: 2)
  - [x] Update `static_src/js/lead-handoff.js`:
    - [x] In `triggerLeadCreation`, if `data.success` is true, verify `data.whatsapp_url` is present and valid.
    - [x] Set `window.location.href = data.whatsapp_url` to redirect to WhatsApp.
    - [x] If `data.whatsapp_url` is missing or invalid, display a French recovery message to the tenant and do not redirect.
  - [x] Rebuild tailwind CSS to ensure clean assets: `npm run css:build`.
- [x] Write Integration and Unit Tests (AC: 4)
  - [x] Add tests in `apps/leads/tests/test_services.py`:
    - [x] Test `generate_whatsapp_handoff_url` successfully creates a `WhatsAppHandoffAttempt` and returns a correctly formatted `wa.me` URL with encoded parameters.
    - [x] Verify message content doesn't claim to track conversation and contains the correct references.
    - [x] Verify target phone has no non-digit characters.
  - [x] Add tests in `apps/leads/tests/test_views.py`:
    - [x] Test that `create_lead_endpoint` returns `whatsapp_url` when successful.
    - [x] Verify that if lead creation fails, no `whatsapp_url` is returned (status 400).
- [x] Run Validation Checks (AC: 1, 2, 3, 4)
  - [x] Run `python manage.py test` to verify all tests pass.
  - [x] Run `python manage.py check` to ensure Django configurations are valid.

## Dev Notes

- Target phone format: WhatsApp wa.me API requires numbers in digits-only format. Strip the leading '+' and any other non-digit characters from `whatsapp_phone`.
- Audit logs: Event type should be `whatsapp.handoff` with the actor as `lead.tenant`, `target_id=lead.id`, and include the target phone and listing ID in metadata.
- File paths to touch:
  - [apps/leads/models.py](file:///C:/dev/maison/apps/leads/models.py)
  - [apps/leads/services.py](file:///C:/dev/maison/apps/leads/services.py)
  - [apps/leads/views.py](file:///C:/dev/maison/apps/leads/views.py)
  - [static_src/js/lead-handoff.js](file:///C:/dev/maison/static_src/js/lead-handoff.js)
  - [apps/leads/tests/test_services.py](file:///C:/dev/maison/apps/leads/tests/test_services.py)
  - [apps/leads/tests/test_views.py](file:///C:/dev/maison/apps/leads/tests/test_views.py)

### Project Structure Notes

- Follow Django modular structures: models in `models.py`, business operations in `services.py`, endpoints in `views.py`.
- No REST framework: return native `JsonResponse`.

### References

- [architecture.md](file:///C:/dev/maison/_bmad-output/planning-artifacts/architecture.md#L335-L347)
- [epics.md](file:///C:/dev/maison/_bmad-output/planning-artifacts/epics.md#L671-L699)

## Dev Agent Record

### Agent Model Used

Gemini 3.5 Flash (High)

### Debug Log References

- Aucun incident ou erreur de debug rencontrés.

### Completion Notes List

- Création du modèle `WhatsAppHandoffAttempt` dans `apps/leads/models.py` avec relation ForeignKey vers `Lead` et date de tentative.
- Génération et application des migrations pour la base de données.
- Implémentation du service `generate_whatsapp_handoff_url` dans `apps/leads/services.py` qui formate proprement le numéro WhatsApp sans le préfixe `+` (wa.me digits-only format), crée l'enregistrement de tentative, crée un `AuditEvent` du type `whatsapp.handoff` et encode le message d'ouverture en français sans mention de suivi.
- Intégration du service dans la vue `create_lead_endpoint` de `apps/leads/views.py` pour retourner le lien `whatsapp_url` dans la réponse JSON après la création avec succès du lead.
- Mise à jour du script JavaScript frontend `static_src/js/lead-handoff.js` pour rediriger l'utilisateur vers `data.whatsapp_url` en cas de succès et gérer les erreurs de redirection.
- Recompilation complète des feuilles de style via `npm run css:build`.
- Écriture et passage avec succès des tests unitaires et d'intégration couvrant le modèle, le service et les vues de leads.

### File List

- [apps/leads/models.py](file:///C:/dev/maison/apps/leads/models.py)
- [apps/leads/services.py](file:///C:/dev/maison/apps/leads/services.py)
- [apps/leads/views.py](file:///C:/dev/maison/apps/leads/views.py)
- [apps/leads/tests/test_models.py](file:///C:/dev/maison/apps/leads/tests/test_models.py)
- [apps/leads/tests/test_services.py](file:///C:/dev/maison/apps/leads/tests/test_services.py)
- [apps/leads/tests/test_views.py](file:///C:/dev/maison/apps/leads/tests/test_views.py)
- [static_src/js/lead-handoff.js](file:///C:/dev/maison/static_src/js/lead-handoff.js)
- [apps/leads/migrations/0002_whatsapphandoffattempt.py](file:///C:/dev/maison/apps/leads/migrations/0002_whatsapphandoffattempt.py)

