---
baseline_commit: 83de0f8f0b1584d8b991f06922f9a3af5385d75b
---

# Story 3.4: Recoverable Handoff Failure States

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Tenant,
I want clear recovery options when Lead creation or WhatsApp opening fails,
so that my intent is not lost and I understand what happened.

## Acceptance Criteria

1. **Given** Lead creation fails, **when** the Tenant confirms contact, **then** Maison keeps the identification flow open, **and** preserves entered values, shows a recoverable French error, offers retry, and does not open WhatsApp.
2. **Given** Lead creation succeeds but WhatsApp opening fails, **when** the Tenant remains on Maison, **then** Maison explains that the Lead exists, **and** provides a retry action or fallback link for the WhatsApp handoff.
3. **Given** the contact CTA is processing, **when** the Lead or handoff request is in progress, **then** Maison disables duplicate submission, **and** shows a localized loading state near the action rather than a full-page spinner.
4. **Given** failure states are rendered, **when** they are tested for accessibility, **then** errors are announced through appropriate semantics or live-region behavior, **and** color is not the only signal for error, warning, or success.

## Tasks / Subtasks

- [x] Enhance Frontend Error Handling and State Preservation (AC: 1, 4)
  - [x] Update `static_src/js/lead-handoff.js`:
    - [x] On lead creation failure (HTTP status code other than 2xx), keep the modal open and do not reset input values.
    - [x] Display an inline, clear French error message (e.g. "Échec de la création du contact. Veuillez réessayer.") inside the modal or near the button.
    - [x] Ensure the error container has `role="alert"` and `aria-live="polite"` so it is announced to screen readers.
    - [x] Avoid using color as the sole indicator of failure (e.g. include an warning icon or text prefix "Erreur :").
- [x] Implement Fallback Redirection Link and Success State (AC: 2, 4)
  - [x] Add a visual success/retry container in the template or detail page when lead creation succeeds.
  - [x] Update `static_src/js/lead-handoff.js` to handle lead creation success:
    - [x] In addition to attempting `window.location.href` redirection, display a clean fallback message in the UI: "Votre demande de contact a été enregistrée. Si vous n'êtes pas redirigé automatiquement, [cliquez ici pour ouvrir WhatsApp](url)."
    - [x] Ensure this fallback link is highly visible and keyboard-focusable.
    - [x] Ensure the announcement is made accessibly via `aria-live`.
- [x] Prevent Duplicate Submissions and Show Processing State (AC: 3)
  - [x] Ensure all contact buttons (`data-contact-whatsapp`) are disabled as soon as lead creation starts.
  - [x] Replace text or show a inline loading indicator (e.g. dynamic dot animation or spinner next to text) instead of blocking the entire screen.
  - [x] Ensure buttons are re-enabled and loading indicators are hidden if the request fails, permitting a retry.
- [x] Write Integration and Accessibility Tests (AC: 4)
  - [x] Add unit/view tests in `apps/leads/tests/test_views.py` verifying that failures return appropriate 400 error codes with French copy.
  - [x] Write frontend assertion guidelines or tests to verify accessibility markup (`role="alert"`, `aria-live`, non-color signals).
- [x] Run Validation Checks (AC: 1, 2, 3, 4)
  - [x] Run `python manage.py test` to verify no regressions.
  - [x] Compile CSS assets: `npm run css:build`.

## Dev Notes

- Frontend containers: Create/ensure there is a dedicated error container in the DOM (e.g., `#handoff-error`) with `role="alert"` and `aria-live="assertive"`.
- Loading indicator: Use CSS micro-animations on the button itself (e.g., `.loading` class or tailwind inline spin loader) rather than full-page overlays.
- File paths to touch:
  - [static_src/js/lead-handoff.js](file:///C:/dev/maison/static_src/js/lead-handoff.js)
  - [templates/listings/detail.html](file:///C:/dev/maison/templates/listings/detail.html) (or wherever the contact button lives)
  - [apps/leads/tests/test_views.py](file:///C:/dev/maison/apps/leads/tests/test_views.py)

### Project Structure Notes

- Keep all asynchronous handoff logic centralized in `static_src/js/lead-handoff.js`.

### References

- [architecture.md](file:///C:/dev/maison/_bmad-output/planning-artifacts/architecture.md#L348-L353)
- [epics.md](file:///C:/dev/maison/_bmad-output/planning-artifacts/epics.md#L700-L729)

## Dev Agent Record

### Agent Model Used

Gemini 3.5 Flash (High)

### Debug Log References

- None.

### Completion Notes List

- Implemented inline French error messages inside the identification modal (`#handoff-error-modal`) and near the contact CTA button (`#handoff-error-cta`) when lead creation fails.
- Configured accessible error announcements using `role="alert"` and `aria-live="polite"`, with a text prefix and warning icon (`⚠️`) as non-color signals.
- Preserved user inputs inside the modal upon lead creation failure by keeping the modal open.
- Implemented a fallback redirection container (`#handoff-success-cta`) on success to allow users to click a visible and focusable link to manually open WhatsApp if the auto-redirect fails.
- Disabled duplicate submissions by disabling all contact buttons (`[data-contact-whatsapp]`) and showing an animated loading dot state (`Envoi en cours...`) during lead creation, re-enabling them upon failure to permit retries.
- Added unit tests in `apps/leads/tests/test_views.py` to assert that validation failures (such as missing WhatsApp consent) return 400 responses with localized French error copy.
- Added integration tests in `apps/leads/tests/test_views.py` to verify the existence and structure of frontend accessibility markup (`role="alert"`, `aria-live="polite"`, non-color signals).
- Re-run all Django tests successfully and rebuilt Tailwind CSS assets.

### File List

- [static_src/js/lead-handoff.js](file:///C:/dev/maison/static_src/js/lead-handoff.js)
- [templates/listings/includes/contact_cta.html](file:///C:/dev/maison/templates/listings/includes/contact_cta.html)
- [templates/listings/includes/identification_modal.html](file:///C:/dev/maison/templates/listings/includes/identification_modal.html)
- [apps/leads/tests/test_views.py](file:///C:/dev/maison/apps/leads/tests/test_views.py)

### Change Log

- 2026-06-10: Implemented recoverable handoff failure states, frontend error/success message containers, duplicate submission prevention, accessibility attributes, and added unit/integration tests.
