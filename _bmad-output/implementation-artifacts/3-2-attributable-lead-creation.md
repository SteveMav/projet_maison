---
baseline_commit: 83de0f8f0b1584d8b991f06922f9a3af5385d75b
---

# Story 3.2: Attributable Lead Creation

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As Maison,
I want to create a Lead before any WhatsApp handoff,
so that tenant intent is attributable to the selected Listing and Commissionnaire.

## Acceptance Criteria

1. **Given** a Tenant has completed Lightweight Identification with consent, **when** they confirm the WhatsApp Contact Action for an available Listing, **then** Maison creates a Lead before opening or returning any WhatsApp URL.
2. **Given** a Lead is created, **then** the Lead records Tenant identifier, Listing, Commissionnaire Profile, creation timestamp, and acquisition context available to Maison.
3. **Given** the same Tenant contacts the same Listing more than once, **when** each contact attempt is confirmed, **then** Maison preserves distinguishable event history and repeated attempts do not overwrite the original Lead provenance.
4. **Given** the selected Listing is no longer available before Lead creation, **when** the contact action is processed, **then** Maison does not create a handoff-ready Lead and **shows** a recoverable state explaining that the Listing is unavailable.
5. **Given** Lead creation is implemented, **when** tests run, **then** they verify Lead ownership, Listing-to-Commissionnaire provenance, consent presence, timestamp creation, and the invariant that Lead creation precedes WhatsApp URL generation.

## Tasks / Subtasks

- [x] Verify prerequisites and current implementation state (AC: 1, 2, 3, 4, 5)
  - [x] Confirm Story 3.1 is implemented.
  - [x] Inspect `apps/accounts/models.py`, `apps/listings/models.py`, `apps/commissionnaires/models.py`, and `apps/audit/models.py`.
  - [x] Ensure all existing tests run and pass using `python manage.py test`.

- [x] Implement Lead and LeadStatusEvent models (AC: 1, 2, 3)
  - [x] Define the `Lead` model in `apps/leads/models.py`:
    - `tenant` (ForeignKey to settings.AUTH_USER_MODEL, related_name="leads", on_delete=models.CASCADE)
    - `listing` (ForeignKey to listings.Listing, related_name="leads", on_delete=models.CASCADE)
    - `commissionnaire_profile` (ForeignKey to commissionnaires.CommissionnaireProfile, related_name="leads", on_delete=models.CASCADE)
    - `created_at` (DateTimeField, auto_now_add=True)
    - `acquisition_context` (JSONField, default=dict, blank=True)
  - [x] Define the `LeadStatusEvent` model in `apps/leads/models.py`:
    - `lead` (ForeignKey to `Lead`, related_name="status_events", on_delete=models.CASCADE)
    - `status` (CharField, max_length=32, default="new", choices=[("new", "Nouveau"), ("contacted", "Contacté"), ("closed", "Fermé")])
    - `changed_at` (DateTimeField, auto_now_add=True)
  - [x] Add `ordering = ["-created_at"]` and database indexes on `created_at` in the Meta class of `Lead`.
  - [x] Generate database migrations: `python manage.py makemigrations leads`
  - [x] Apply database migrations: `python manage.py migrate`

- [x] Implement Lead Creation Service (AC: 1, 2, 3, 4, 5)
  - [x] Create `create_lead_for_listing(*, tenant, listing, acquisition_context=None)` in `apps/leads/services.py`:
    - [x] Check if `listing.availability_status` equals `available` (`Listing.AvailabilityStatus.AVAILABLE`). If not, raise a `django.core.exceptions.ValidationError` with French error message "Cette annonce n'est plus disponible."
    - [x] Verify that user is authenticated and has provided whatsapp consent (raise `ValidationError` if not).
    - [x] Save a `Lead` record referencing the tenant, listing, and commissionnaire profile.
    - [x] Create the initial `LeadStatusEvent` with status `new`.
    - [x] Create a business `AuditEvent` of type `lead.created` using `apps.audit.services.create_audit_event`.
    - [x] Return the created `Lead` instance.

- [x] Implement Lead Creation Endpoint (AC: 1, 2, 3, 4)
  - [x] Create a POST JSON endpoint view `create_lead_endpoint` in `apps/leads/views.py`:
    - [x] Require user to be authenticated (use `@login_required` or similar).
    - [x] If request method is not POST, return HTTP 405.
    - [x] Call the service `create_lead_for_listing`.
    - [x] If successful, return JSON `{"success": true, "lead_id": lead.id}`.
    - [x] If ValidationError raised: return HTTP 400 with `{"success": false, "error": error_message}` (with localized French error copy).
  - [x] Register URL pattern in `apps/leads/urls.py` matching `/listings/<int:listing_id>/create-lead/` (name `create_lead`).
  - [x] Ensure `apps.leads.urls` is included in `config/urls.py` with app_name namespace `leads`.

- [x] Build Frontend JavaScript and UI Integration (AC: 1, 4)
  - [x] Update `static_src/js/lead-handoff.js`:
    - [x] In the success handler of the identification form (or when user clicks and already has consent):
      - [x] Disable the CTA button and set text to "Envoi en cours...".
      - [x] Perform a POST request to `/listings/<id>/create-lead/` with appropriate CSRF headers.
      - [x] If successful: proceed to simulated handoff (alert/console log for this story).
      - [x] If unsuccessful (e.g., listing unavailable): display the returned error message on a recoverable error-soft surface inline or as an alert, and restore the button state.
  - [x] Recompile assets by running `npm run css:build`.

- [x] Add Tests for Lead Creation (AC: 5)
  - [x] Write service tests in `apps/leads/tests/test_services.py`:
    - [x] Verify lead creation saves correct relations and creates initial event + audit event.
    - [x] Verify validation fails if listing is unavailable.
    - [x] Verify multiple lead creations from the same tenant are distinguishable.
  - [x] Write view tests in `apps/leads/tests/test_views.py`:
    - [x] Verify authentication constraint.
    - [x] Verify POST to endpoint creates lead for available listing.
    - [x] Verify POST to endpoint returns 400 with error if listing is unavailable.

- [x] Run Validation Checks (AC: 1, 2, 3, 4, 5)
  - [x] Run `python manage.py check` to ensure clean Django setup.
  - [x] Run `python manage.py makemigrations --check --dry-run` to verify migrations are up-to-date.
  - [x] Run `python manage.py test` to verify all tests (new and existing) pass.
  - [x] Verify tailwind compiles successfully: `npm run css:build`.

## Dev Notes

- Reuse `apps.audit.services.create_audit_event` to write append-only business audit history.
- Endpoint naming: `/listings/<id>/create-lead/` maps to `leads:create_lead`.
- What NOT to implement: True WhatsApp external redirects and actual message composition (belongs to Story 3.3).

### Project Structure Notes

- Lead models go in `apps/leads/models.py`.
- Lead services go in `apps/leads/services.py`.
- JSON Response Format: `{"success": true, "lead_id": lead.id}` or `{"success": false, "error": "..."}`.

### References

- Cite FR-8 and NFR-2/5 from [architecture.md](file:///C:/dev/maison/_bmad-output/planning-artifacts/architecture.md).
- Cite UX-DR21 and UX-DR22 from [epics.md](file:///C:/dev/maison/_bmad-output/planning-artifacts/epics.md#L130-L132).

## Dev Agent Record

### Agent Model Used

Gemini 3.5 Flash (High)

### Debug Log References
- Aucun incident ou erreur de debug rencontrés lors de l'implémentation.

### Completion Notes List
- Création des modèles `Lead` et `LeadStatusEvent` dans `apps/leads/models.py`.
- Création et application des migrations pour la base de données.
- Création du service `create_lead_for_listing` dans `apps/leads/services.py` effectuant la validation de disponibilité et l'enregistrement de l'audit event.
- Implémentation de la vue d'API `create_lead_endpoint` dans `apps/leads/views.py`.
- Enregistrement de la route dans `apps/leads/urls.py` et liaison dans `config/urls.py`.
- Mise à jour de `static_src/js/lead-handoff.js` pour soumettre de manière asynchrone le Lead au clic sur le bouton WhatsApp et afficher les erreurs en cas de logement indisponible.
- Recompilation réussie des assets via `npm run css:build`.
- Écriture d'une suite complète de tests unitaires et d'intégration dans `apps/leads/tests/test_services.py` et `apps/leads/tests/test_views.py`.

### File List
- [apps/leads/models.py](file:///C:/dev/maison/apps/leads/models.py)
- [apps/leads/services.py](file:///C:/dev/maison/apps/leads/services.py)
- [apps/leads/views.py](file:///C:/dev/maison/apps/leads/views.py)
- [apps/leads/urls.py](file:///C:/dev/maison/apps/leads/urls.py)
- [apps/leads/tests/test_models.py](file:///C:/dev/maison/apps/leads/tests/test_models.py)
- [apps/leads/tests/test_services.py](file:///C:/dev/maison/apps/leads/tests/test_services.py)
- [apps/leads/tests/test_views.py](file:///C:/dev/maison/apps/leads/tests/test_views.py)
- [config/urls.py](file:///C:/dev/maison/config/urls.py)
- [static_src/js/lead-handoff.js](file:///C:/dev/maison/static_src/js/lead-handoff.js)
- [static/css/app.css](file:///C:/dev/maison/static/css/app.css)
- [apps/leads/migrations/0001_initial.py](file:///C:/dev/maison/apps/leads/migrations/0001_initial.py)
- [_bmad-output/implementation-artifacts/3-2-attributable-lead-creation.md](file:///C:/dev/maison/_bmad-output/implementation-artifacts/3-2-attributable-lead-creation.md)
- [_bmad-output/implementation-artifacts/sprint-status.yaml](file:///C:/dev/maison/_bmad-output/implementation-artifacts/sprint-status.yaml)
