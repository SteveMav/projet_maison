---
baseline_commit: 83de0f8f0b1584d8b991f06922f9a3af5385d75b
---

# Story 3.1: Lightweight Identification And Consent

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Tenant,
I want to provide the minimum identity information and consent before contacting a Commissionnaire,
so that Maison can create an attributable enquiry without forcing a heavy account journey.

## Acceptance Criteria

1. Given a signed-in Tenant opens the WhatsApp Contact Action for an available Listing, when Lightweight Identification is required, then Maison presents a modal, sheet, or page that collects the required Tenant identity fields (Name, Phone Number, Consent) and explains that the information is used to connect the Tenant with the Commissionnaire and attribute the enquiry.
2. Given Lightweight Identification is displayed, when the Tenant reviews the form, then Maison requires explicit consent before continuing and includes the privacy reassurance `Maison ne lit pas vos conversations WhatsApp.`.
3. Given required identity fields or consent are missing, when the Tenant attempts to continue, then Maison blocks progression and shows field-level French error copy without opening WhatsApp.
4. Given the identification UI appears on mobile or desktop, when a keyboard, touch, or screen-reader user interacts with it, then controls have visible labels, visible focus, 44px touch targets, and accessible error feedback and the CTA exposes loading and disabled states for later Lead creation.

## Tasks / Subtasks

- [x] Verify prerequisites and current implementation state (AC: 1, 2, 3, 4)
  - [x] Confirm Stories 1.1 through 2.7 are implemented.
  - [x] Inspect existing `apps/accounts/models.py`, `apps/accounts/forms.py`, `apps/accounts/views.py`, `templates/listings/detail.html`, `templates/listings/includes/contact_cta.html`, and `static_src/js/listing-detail.js`.
  - [x] Ensure all existing tests run and pass using `python manage.py test`.

- [x] Update Account Models for Consent Tracking (AC: 1, 2)
  - [x] Update `CustomUser` in `apps/accounts/models.py` to add `whatsapp_consent` (`models.BooleanField(default=False)`) and `whatsapp_consent_given_at` (`models.DateTimeField(null=True, blank=True)`).
  - [x] Generate database migration: `python manage.py makemigrations accounts`
  - [x] Apply migration: `python manage.py migrate`

- [x] Implement Lightweight Identification Form and Endpoint (AC: 1, 2, 3)
  - [x] Create `LightweightIdentificationForm` in `apps/accounts/forms.py`. It should collect:
    - `first_name` (required, CharField, label="Prénom")
    - `last_name` (required, CharField, label="Nom de famille")
    - `whatsapp_phone` (required, CharField, label="Numéro WhatsApp")
    - `consent` (required, BooleanField, label="J'accepte de partager mes coordonnées avec le Commissionnaire")
  - [x] Implement validation in `LightweightIdentificationForm`:
    - Use `normalize_whatsapp_phone` validator on the `whatsapp_phone` field.
    - Add a clean method to ensure `consent` is checked; return French error copy if unchecked (e.g., "Vous devez cocher cette case pour continuer.").
  - [x] Create a POST JSON endpoint view `identify_tenant` in `apps/accounts/views.py`:
    - Require user to be authenticated (use `LoginRequiredMixin` or `@login_required`).
    - If form is valid: update `request.user` fields (`first_name`, `last_name`, `whatsapp_phone`, `whatsapp_consent = True`, `whatsapp_consent_given_at = timezone.now()`), save, and return `{"success": true}` JSON.
    - If form is invalid: return HTTP 400 with `{"success": false, "errors": form.errors.get_json_data()}` (with localized French error copy).
  - [x] Register URL pattern in `apps/accounts/urls.py` matching `/accounts/identify/` (name `identify`).

- [x] Build Modal UI Template and Frontend JavaScript (AC: 1, 2, 3, 4)
  - [x] Create a modal template `templates/listings/includes/identification_modal.html` with:
    - Explanatory copy: "Ces informations sont utilisées pour vous mettre en relation avec le Commissionnaire et attribuer votre demande."
    - Inputs for `first_name`, `last_name`, `whatsapp_phone`, and a consent checkbox.
    - Reassurance message: `Maison ne lit pas vos conversations WhatsApp.`
    - Inline error elements associated via `aria-describedby` (e.g., `<span class="error-msg" id="error-whatsapp_phone" role="alert"></span>`).
    - Touch targets of at least 44px/48px for all inputs and buttons.
    - Active focus rings for better visibility.
  - [x] Include this modal inside the listing detail rendering flow (e.g., inside `templates/listings/detail.html`).
  - [x] Create/update frontend script `static_src/js/lead-handoff.js`:
    - Bind event listener to `[data-contact-whatsapp]` buttons.
    - If clicked and user has not yet consented or filled in details:
      - Intercept the action, open the modal, trap keyboard focus, and set initial focus on the `first_name` input.
    - Submit the form asynchronously via `fetch` POST to `/accounts/identify/` with appropriate CSRF headers:
      - Set the submit button to a disabled/loading state (e.g., "Envoi en cours...").
      - Clear previous errors before sending.
      - On error (400 response): render the French field-level errors inline under the inputs, restore the button state, and focus the first erroneous input or announce via `aria-live`.
      - On success: close the modal, restore focus to the trigger button, and execute success callback (mocking the handoff/console log for this story).
    - Handle keyboard events: close on Escape, trap focus within the modal boundaries (Tab and Shift+Tab cycling).
  - [x] Build CSS for the modal inside `static_src/css/input.css` using Maison design standards (warm neutrals, green for primary actions, generous padding).
  - [x] Build compiled assets by running `npm run css:build`.

- [x] Add Tests for Identification Flow (AC: 1, 2, 3, 4)
  - [x] Test form validation in `apps/accounts/forms.py` with missing fields, invalid phone numbers, and unchecked consent.
  - [x] Test the `/accounts/identify/` endpoint:
    - Assert that unauthenticated users are blocked/redirected.
    - Assert that valid POST updates user fields and sets `whatsapp_consent` to True.
    - Assert that invalid POST returns status 400 with French JSON error messages.
  - [x] Test detail page structure contains the identification modal placeholders and buttons.

- [x] Run Validation Checks (AC: 1, 2, 3, 4)
  - [x] Run `python manage.py check` to ensure clean Django setup.
  - [x] Run `python manage.py makemigrations --check --dry-run` to verify migrations are up-to-date.
  - [x] Run `python manage.py test` to verify all tests (new and existing) pass.
  - [x] Verify tailwind compiles successfully: `npm run css:build`.

## Dev Notes

### Source Context
- Story source: `_bmad-output/planning-artifacts/epics.md`, Epic 3, Story 3.1.
- Requirements: FR-7; NFR-3; UX-DR20, UX-DR22, UX-DR32, UX-DR34.
- FR-7 requires Lightweight Identification before handoff, explaining the purpose of collected info, explicit consent, and blocking handoff until fields are valid.
- NFR-3 requires protecting user data and establishing clear boundaries for personal info.
- UX-DR20 specifies Lightweight Identification details (Name, phone number, consent, explanation).
- UX-DR22 specifies that the modal is raised with a privacy reassurance: `Maison ne lit pas vos conversations WhatsApp.`.
- UX-DR32 and UX-DR34 define error copy in French, inline error feedback, and accessible touch target sizes (at least 44px).

### Django and Frontend Patterns
- Reuse `normalize_whatsapp_phone` validator located in `apps/accounts/validators.py`.
- Authenticated user identification data should be persisted directly on the `CustomUser` model.
- Static assets compilation relies on `static_src/` directory which Django resolves through `STATICFILES_DIRS`. Keep JS in `static_src/js/lead-handoff.js`.

### What NOT to implement in this story
- Lead record creation in the database (`apps/leads/models.py` schema changes belong to Story 3.2).
- True WhatsApp external redirects and actual message composition (belongs to Story 3.3).
- Moderation access or Listing verification checks.

## Dev Agent Record

### Agent Model Used
Gemini 3.5 Flash (High)

### Debug Log References
- Aucun incident ou erreur de debug rencontrés lors de l'implémentation.

### Completion Notes List
- Ajout des champs `whatsapp_consent` (Boolean) et `whatsapp_consent_given_at` (DateTimeField) au modèle `CustomUser`.
- Création et application des migrations pour la base de données.
- Création du formulaire `LightweightIdentificationForm` dans `apps/accounts/forms.py` avec validation du numéro de téléphone et vérification explicite du consentement.
- Implémentation de la vue d'API `identify_tenant` renvoyant du JSON (HTTP 200 en cas de succès, HTTP 400 en cas d'erreur avec messages localisés en français).
- Création du template de modal `templates/listings/includes/identification_modal.html`.
- Intégration de la modal dans le cycle de rendu de la page détail et du drawer.
- Création du script JavaScript `static_src/js/lead-handoff.js` gérant l'interception de clic, la soumission AJAX du formulaire, la gestion des erreurs inline, le focus-trap pour l'accessibilité, et la restauration de focus.
- Ajout des règles de style pour la modal dans `static_src/css/input.css` et compilation finale des assets CSS.
- Écriture d'une suite complète de tests unitaires et d'intégration dans `apps/accounts/tests/test_lightweight_identification.py` couvrant le formulaire, l'endpoint, et le rendu de la page détail.

### File List
- [apps/accounts/models.py](file:///C:/dev/maison/apps/accounts/models.py)
- [apps/accounts/forms.py](file:///C:/dev/maison/apps/accounts/forms.py)
- [apps/accounts/views.py](file:///C:/dev/maison/apps/accounts/views.py)
- [apps/accounts/urls.py](file:///C:/dev/maison/apps/accounts/urls.py)
- [apps/accounts/tests/test_custom_user.py](file:///C:/dev/maison/apps/accounts/tests/test_custom_user.py)
- [apps/accounts/tests/test_lightweight_identification.py](file:///C:/dev/maison/apps/accounts/tests/test_lightweight_identification.py)
- [templates/listings/includes/detail_panel.html](file:///C:/dev/maison/templates/listings/includes/detail_panel.html)
- [templates/listings/includes/contact_cta.html](file:///C:/dev/maison/templates/listings/includes/contact_cta.html)
- [templates/listings/includes/identification_modal.html](file:///C:/dev/maison/templates/listings/includes/identification_modal.html)
- [templates/listings/browse.html](file:///C:/dev/maison/templates/listings/browse.html)
- [templates/listings/detail.html](file:///C:/dev/maison/templates/listings/detail.html)
- [static_src/js/lead-handoff.js](file:///C:/dev/maison/static_src/js/lead-handoff.js)
- [static_src/css/input.css](file:///C:/dev/maison/static_src/css/input.css)
- [static/css/app.css](file:///C:/dev/maison/static/css/app.css)
- [apps/accounts/migrations/0002_customuser_whatsapp_consent_and_more.py](file:///C:/dev/maison/apps/accounts/migrations/0002_customuser_whatsapp_consent_and_more.py)
