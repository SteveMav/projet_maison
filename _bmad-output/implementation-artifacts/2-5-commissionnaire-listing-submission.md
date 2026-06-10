---
baseline_commit: 83de0f8f0b1584d8b991f06922f9a3af5385d75b
---

# Story 2.5: Commissionnaire Listing Submission

Status: review

<!-- Validation: created from bmad-create-story workflow on 2026-06-06. -->

## Story

As a Commissionnaire,
I want to submit a rental Listing from my phone,
so that I can contribute useful inventory without a heavy administrative process.

## Acceptance Criteria

1. Given a signed-in Commissionnaire has a valid Commissionnaire Profile, when they open the publication flow, then Maison presents a mobile-friendly form or stepper for monthly price, Commune, bedroom count, description, Availability Status, and photos and the flow uses visible labels, concise French copy, and 44px touch targets.
2. Given the Commissionnaire submits the required Listing fields and at least three usable real photos, when the submission is processed, then Maison stores the Listing with submission time and last update time and associates it with exactly one Commissionnaire Profile.
3. Given required fields are missing, when the form is submitted, then Maison blocks submission and identifies the exact fields to correct.
4. Given uploaded media is unsupported or unusable, when validation runs, then Maison rejects the affected media and explains what the Commissionnaire must correct without accepting the invalid photo.
5. Given a user without a valid Commissionnaire Profile attempts publication, when the request is processed, then Maison denies or redirects server-side to the required profile setup and no Listing is created.

## Tasks / Subtasks

- [x] Verify prerequisites and current implementation state (AC: 1, 2, 3, 4, 5)
  - [x] Confirm Stories 1.1 through 2.4 are implemented before coding this story.
  - [x] Confirm `CommissionnaireProfile` exists, belongs to the signed-in user, and exposes a publication eligibility check from Story 1.5.
  - [x] Confirm Story 2.1 `Listing` and `ListingPhoto` models, local media settings, validators, primary photo behavior, and minimum-photo readiness helper exist.
  - [x] Confirm Stories 2.2 through 2.4 did not introduce public visibility for `under_review` Listings.
  - [x] Read existing `apps/accounts`, `apps/commissionnaires`, `apps/listings`, `templates`, `static_src`, `config/urls.py`, and tests before editing.
  - [x] Preserve unrelated sprint status changes already present, including any story currently marked `review` or `in-progress`.

- [x] Add protected Commissionnaire publication route (AC: 1, 5)
  - [x] Add or update a pro route such as `/pro/listings/new/`.
  - [x] Place the route under the existing Commissionnaire/pro URL namespace if Story 1.5 created one; otherwise add a minimal `apps/commissionnaires/urls.py` include from `config/urls.py`.
  - [x] Require authentication server-side.
  - [x] Require the Story 1.4 WhatsApp phone gate before publication.
  - [x] Require an eligible `CommissionnaireProfile`; redirect to profile setup with safe `next` preservation if missing or incomplete.
  - [x] Do not allow a user to pass another user's profile id or create a Listing for another Commissionnaire.
  - [x] Do not expose private Listing, Lead, moderation, or profile data when access is denied.

- [x] Add Listing submission form and photo field (AC: 1, 2, 3, 4)
  - [x] Add or update `apps/listings/forms.py`.
  - [x] Use a Django `ModelForm` or plain `Form` for Listing fields, matching the implemented Story 2.1 model.
  - [x] Validate monthly USD price as a positive integer amount; do not use floats.
  - [x] Validate `commune`, `bedroom_count`, and `description` as required and non-blank after trimming.
  - [x] Include the required availability/submission state in the flow without allowing accidental public publication before moderation.
  - [x] If the model has only `availability_status`, submit new Listings as `under_review` and explain the next state as `Envoyée pour modération`.
  - [x] If the model already has separate moderation/requested-availability fields, store the Commissionnaire's intended availability there and still prevent public visibility until moderation allows it.
  - [x] Add a multiple-photo upload field using a validated Django multiple file field pattern.
  - [x] Require at least three uploaded usable photos for submission.
  - [x] Preserve entered form values on invalid submission.
  - [x] Surface field-level French errors for each missing/invalid field.

- [x] Reuse Story 2.1 media validation (AC: 2, 4)
  - [x] Use existing `apps/listings/validators.py` or service validation for image content.
  - [x] Validate uploaded files through Django/Pillow-backed image checks before saving.
  - [x] Reject unsupported extensions, corrupt images, empty files, SVG, oversized files, and files that are not usable raster property photos.
  - [x] Do not trust original filenames, file extensions, or browser-provided MIME type alone.
  - [x] Identify invalid files in correction copy without accepting the invalid photo.
  - [x] Do not use AI-generated villas, luxury-only placeholders, or architectural renders as silent production media.
  - [x] Do not add cloud storage, client-side upload widgets, direct-to-S3 uploads, or background image processing in this story.

- [x] Add atomic submission service (AC: 2, 3, 4, 5)
  - [x] Add or update `apps/listings/services.py`.
  - [x] Implement `submit_listing_for_commissionnaire(profile, listing_data, uploaded_photos)` or equivalent.
  - [x] Accept a `CommissionnaireProfile` object as owner, never a raw user id or profile id from the request body.
  - [x] Validate all listing fields and all uploaded photos before creating public-persistent objects.
  - [x] Use `transaction.atomic()` around Listing and ListingPhoto creation.
  - [x] Set `commissionnaire_profile` exactly once from the authenticated user's profile.
  - [x] Set `submitted_at` to `timezone.now()` on successful submission.
  - [x] Rely on `updated_at`/model save for last update timestamp.
  - [x] Set the initial non-public state safely, preferably `availability_status = under_review` unless a separate moderation state already exists.
  - [x] Save photos in deterministic upload order, with positions starting at 0 or 1 according to Story 2.1 convention.
  - [x] Mark the first valid uploaded photo as primary unless the form allows an explicit primary selection.
  - [x] If file storage succeeds but database work fails, clean up orphaned files where practical.
  - [x] Return structured validation errors for the view/form to render; do not swallow failures.

- [x] Build mobile-friendly publication UI (AC: 1, 3, 4)
  - [x] Add `templates/commissionnaires/listing_submission.html` or the established pro-surface template path.
  - [x] Use a short mobile-friendly stepper or sectioned form: rental details, photos, submit.
  - [x] Keep the stepper lightweight; do not implement the full preview step from Story 2.6.
  - [x] Use visible labels above controls.
  - [x] Use concise French copy and Maison design tokens.
  - [x] Keep all controls at least 44px tappable; primary action remains at least 48px high.
  - [x] Show field-level errors near the relevant input.
  - [x] Show photo correction errors near the upload control.
  - [x] Show guidance that photos must be real property photos for the represented home.
  - [x] Avoid nested cards, oversized dashboard metrics, decorative hero sections, or full-page spinners.
  - [x] Use compact operational rows and hairline dividers where state or submitted-summary content appears.

- [x] Add confirmation and safe next operational state (AC: 2)
  - [x] After successful submission, redirect to a confirmation or own-listing status surface.
  - [x] Use narrow French confirmation copy such as `Envoyée pour modération`.
  - [x] Explain that Maison will review or process the submitted Listing without claiming it is public or verified.
  - [x] Do not display a Verification Badge or public trust claim on the confirmation.
  - [x] Do not create a public Listing card route for an `under_review` Listing.
  - [x] If a full inventory dashboard is not implemented yet, provide a minimal confirmation page and stable future hook.

- [x] Preserve scope boundaries with Story 2.6 and Epic 4 (AC: 1, 2, 3, 4)
  - [x] Do not implement the full Listing Card preview step; Story 2.6 owns preview.
  - [x] Do not implement final preview validation beyond the required submission validation in this story.
  - [x] Do not implement moderation queue, moderation decisions, correction workflow, rejection/removal, or Verification Checklist.
  - [x] Do not implement public publication/publishing decision unless a prior story already defined that MVP state.
  - [x] Do not create Leads, Reports, WhatsApp handoff, availability reconfirmation, favorites, view counts, analytics, or audit event tables in this story unless already present and required by existing contracts.

- [x] Add tests for access, form validation, media validation, and service behavior (AC: 1, 2, 3, 4, 5)
  - [x] Test anonymous users are redirected to login with `next`.
  - [x] Test authenticated users without WhatsApp phone are routed through the phone gate.
  - [x] Test authenticated users without an eligible Commissionnaire Profile are redirected to profile setup and no Listing is created.
  - [x] Test a valid Commissionnaire can open the publication flow.
  - [x] Test valid required fields plus at least three usable photos create exactly one Listing and associated `ListingPhoto` records.
  - [x] Test created Listing references the signed-in user's `CommissionnaireProfile`, not a supplied request id.
  - [x] Test `submitted_at` and `updated_at` behavior.
  - [x] Test successful submission starts in non-public `under_review`/awaiting-moderation state.
  - [x] Test missing price, Commune, bedroom count, description, status/state, or photos blocks submission and creates no Listing.
  - [x] Test fewer than three usable photos blocks submission and creates no Listing.
  - [x] Test corrupt, empty, unsupported, SVG, and oversized uploads are rejected and not saved as accepted photos.
  - [x] Test first valid uploaded photo becomes primary and photo ordering is deterministic.
  - [x] Test one user cannot create a Listing for another Commissionnaire Profile.
  - [x] Test invalid POST preserves safe form values and renders field-level errors.

- [x] Run required checks (AC: 1, 2, 3, 4, 5)
  - [x] `python manage.py makemigrations --check --dry-run`
  - [x] `python manage.py migrate --check`
  - [x] `python manage.py check`
  - [x] `python manage.py test apps.listings`
  - [x] `python manage.py test apps.commissionnaires`
  - [x] `python manage.py test`
  - [x] `npm run css:build`
  - [x] `python manage.py collectstatic --noinput --dry-run`

## Dev Notes

### Source Context

- Story source: `_bmad-output/planning-artifacts/epics.md`, Epic 2, Story 2.5.
- Requirements: FR-5; NFR-1, NFR-3; UX-DR24, UX-DR26, UX-DR27, UX-DR35, UX-DR36.
- FR-5 requires monthly price, Commune, bedroom count, description, Availability Status, at least three photos before submission, rejection of unsupported/unusable media with correction guidance, submission/update timestamps, and association with exactly one Commissionnaire Profile.
- NFR-3 requires data minimization and server-side access control.
- UX-DR24 requires clear Commissionnaire operational states such as draft, awaiting moderation, correction required, visible, and unavailable.
- UX-DR26 requires compact operational rows and hairline dividers instead of nested dashboard cards.
- UX-DR27 requires a short mobile-friendly publication flow with precise correction messages and at least three real photos.
- UX-DR35/UX-DR36 make property photography part of the trust model and prohibit silent AI/generated/luxury-only production media.

### Dependency On Previous Stories

This story depends on Stories 1.1 through 2.4.

Required previous foundations:

- Story 1.4: WhatsApp phone completion gate.
- Story 1.5: eligible `CommissionnaireProfile` linked to exactly one user.
- Story 2.1: `Listing`, `ListingPhoto`, image validation, local media storage, minimum photo readiness, and deterministic photo ordering.
- Story 2.2: public browse excludes non-available Listings.
- Story 2.3: filter/browse route state remains URL-owned.
- Story 2.4: detail and public surfaces do not expose `under_review` Listings.

If any prerequisite is missing, implement it first. Do not create a parallel profile, listing, media, or access-control system inside this story.

### Current Workspace Snapshot

Targeted file inspection during story creation found a Django scaffold in place, but not the prerequisite Listing/Profile implementation required by this story:

- `apps/listings/apps.py` exists with `ListingsConfig`.
- `apps/commissionnaires/apps.py` exists with `CommissionnairesConfig`.
- `apps/listings/models.py`, `forms.py`, `selectors.py`, `services.py`, `views.py`, and `urls.py` do not exist yet.
- `apps/commissionnaires/models.py`, `forms.py`, `views.py`, and `urls.py` do not exist yet.
- `templates/listings/` and `templates/commissionnaires/` do not exist yet.
- `config/settings.py` includes `apps.listings`, `apps.commissionnaires`, SQLite settings, `MEDIA_URL`, and `MEDIA_ROOT`.
- `config/urls.py` includes core, accounts, admin, and debug media serving; it does not yet include Listing or Commissionnaire URLs.
- `requirements.txt` currently pins only `Django==5.2.14`; Pillow is not present in the current file, so Story 2.1's image validation dependency must be added before this story can validate `ImageField` uploads.
- `static_src/css/input.css` already contains Maison design tokens, form controls, button styles, visible focus styles, and a `max-width: 700px` mobile breakpoint.

The developer must implement or work from completed Stories 1.5 and 2.1 through 2.4 before implementing this submission flow.

### Previous Story Intelligence

- Story 1.5 established that future `Listing` and `Lead` records must reference `CommissionnaireProfile`, not the raw user.
- Story 2.1 set the model foundation and recommended `under_review` as a safe initial status.
- Story 2.1 required media validation to rely on actual image validation, not filenames or browser MIME types.
- Story 2.2 and Story 2.4 protect public surfaces by excluding or hiding `under_review` Listings. This story should not accidentally publish submitted Listings.
- Story 2.4 kept WhatsApp, Lead creation, report submission, and verification out of scope. This story should keep the same boundaries.
- Story 2.6 owns the full preview step and final preview-state correction flow. This story can provide a short stepper/sections but should not build the final Listing Card preview.

### Architecture Compliance

- Use Django 5.2 LTS server-rendered views and templates.
- Use Django forms for validation.
- Use listing services for state-changing submission workflow.
- Keep business logic out of templates.
- Keep state-changing forms CSRF-protected.
- Keep Commissionnaire/pro routes authenticated and permission-checked server-side.
- Use local media storage through `MEDIA_ROOT` and `MEDIA_URL`.
- Use modular JavaScript only for progressive enhancement; no inline JavaScript for business behavior.
- No public `/api/` namespace and no DRF.
- Do not add React, Vue, SPA routing, Redis, PostgreSQL, cloud object storage, direct-to-S3 upload, or background workers.

### Recommended Submission Contract

Recommended route names:

```python
app_name = "commissionnaires"
urlpatterns = [
    path("listings/new/", views.ListingSubmissionView.as_view(), name="listing_submit"),
    path("listings/<int:pk>/submitted/", views.ListingSubmittedView.as_view(), name="listing_submitted"),
]
```

Recommended request behavior:

- `GET`: render publication form/stepper for eligible Commissionnaire.
- `POST`: bind form with `request.POST` and `request.FILES`.
- `POST` valid: create Listing and photos atomically, then redirect to confirmation.
- `POST` invalid: render the same form with field-level errors and uploaded-file correction errors.

Recommended service behavior:

```python
@transaction.atomic
def submit_listing_for_commissionnaire(*, profile, listing_data, uploaded_photos):
    # Validate profile eligibility before this service or at service boundary.
    # Validate all photo content before creating accepted ListingPhoto rows.
    # Create Listing with commissionnaire_profile=profile and submitted_at=timezone.now().
    # Set non-public initial state, usually under_review.
    # Save photos in deterministic order and make first accepted photo primary.
    # Return the submitted Listing.
```

Adapt names and fields to the actual Story 2.1 implementation.

### Availability And Moderation-State Guardrails

This story must not accidentally make submitted Listings public.

If the implementation has only `Listing.availability_status` with `available`, `unavailable`, and `under_review`, use:

```python
listing.availability_status = Listing.AvailabilityStatus.UNDER_REVIEW
```

If the implementation has separate moderation and availability fields, use the moderation field to represent `awaiting_moderation` and store the Commissionnaire's intended availability separately. In both cases:

- public browse must not show the submitted Listing until a later story explicitly publishes it
- confirmation copy should say `Envoyée pour modération`
- no Verification Badge should appear
- no trust copy should imply Maison has reviewed or verified the Listing

### Form And Media Guardrails

The form should collect:

- monthly USD price
- Commune
- bedroom count
- description
- availability/submission state
- at least three photos

Photo validation:

- Use `enctype="multipart/form-data"` on the form.
- Bind files with `request.FILES`.
- Use a multiple-file field pattern that validates every uploaded file.
- Enforce at least three usable photos after validation.
- Reject SVG and other non-raster or unsupported formats.
- Reject corrupt, empty, oversized, and unsupported files.
- Do not save any invalid photo as accepted media.
- Keep original filenames out of trusted paths and user-facing path display.

### UX And Copy Guardrails

Suggested French copy:

- `Publier un bien`
- `Informations du logement`
- `Prix mensuel en USD`
- `Commune`
- `Nombre de chambres`
- `Description`
- `Photos du logement`
- `Ajoutez au moins 3 photos réelles du logement.`
- `Photo inutilisable. Ajoutez une image JPG, PNG ou WebP nette du logement.`
- `Ce champ est obligatoire.`
- `Envoyer pour modération`
- `Envoyée pour modération`
- `Complétez votre profil commissionnaire pour publier.`

UI requirements:

- Mobile-first, short stepper or sectioned form.
- Visible labels above controls.
- 44px minimum touch targets; primary submit at least 48px.
- Field-level errors near inputs.
- Photo errors near upload control and associated file names where possible.
- No full-page spinner; use local loading/disabled state near submit.
- Compact operational rows and hairline dividers.
- No nested dashboard cards or oversized operational metrics.

Trust copy boundaries:

- Do not say the Listing is verified.
- Do not imply Maison guarantees availability or transaction outcome.
- Do not imply AI media is acceptable production media.
- Do not claim Maison has checked the property before moderation.

### Scope Boundaries

Implement now:

- Protected Commissionnaire publication route.
- Listing submission form/stepper.
- Required Listing field validation.
- Multi-photo upload and media validation.
- Atomic Listing + ListingPhoto creation.
- Association to exactly one authenticated `CommissionnaireProfile`.
- Safe non-public submitted state.
- Confirmation/next state copy.
- Tests for access, validation, media rejection, ownership, and no accidental public state.

Do not implement now:

- Full Listing Card preview step and final preview flow; Story 2.6 owns this.
- Availability reconfirmation or status-change history; Story 2.7 owns this.
- Moderation queue, moderation decisions, correction workflow, Verification Checklist, Report flow, Leads, WhatsApp handoff, audit events, favorites, view counts, or analytics.
- Public publishing logic unless a prior story already defined a safe moderation/publication state.

### File Structure Requirements

Expected files to create or update, assuming prerequisites are implemented:

```text
apps/listings/
├── forms.py
├── services.py
├── validators.py        # reuse from Story 2.1
└── tests/
    ├── test_submission_forms.py
    ├── test_submission_services.py
    └── test_media_validation.py
apps/commissionnaires/
├── views.py
├── urls.py
└── tests/
    ├── test_listing_submission_access.py
    └── test_listing_submission_views.py
templates/commissionnaires/
├── listing_submission.html
└── listing_submitted.html
static_src/css/
└── input.css            # publication stepper/form styles only if needed
config/
└── urls.py              # include pro/commissionnaire URLs if missing
```

Read existing files before editing. Preserve account auth, phone gate, profile management, Listing model/service contracts, public browse/detail behavior, and static asset conventions.

### Testing Requirements

Minimum tests:

- Access:
  - anonymous user redirects to login with `next`
  - authenticated user without WhatsApp phone hits phone gate
  - authenticated user without eligible profile redirects to profile setup
  - eligible Commissionnaire can GET the publication form
  - forged profile id cannot create another Commissionnaire's Listing
- Form:
  - required fields validated
  - price is positive integer USD
  - Commune and description trim whitespace
  - at least three usable photos required
  - invalid files produce photo errors
  - invalid submission preserves safe entered values
- Service:
  - valid submission creates one Listing and expected ListingPhoto count
  - Listing references the user's `CommissionnaireProfile`
  - `submitted_at` is set
  - initial status is non-public/under-review
  - first photo becomes primary
  - photo order is deterministic
  - invalid media creates no accepted ListingPhoto and preferably no Listing
  - transaction rollback avoids partial database state
- View/template:
  - form uses `multipart/form-data`
  - visible French labels render
  - field-level errors render near inputs
  - success redirects to confirmation
  - confirmation says `Envoyée pour modération`
  - no Verification Badge or public trust claim renders

Use Django's built-in test runner. Use temporary `MEDIA_ROOT` for upload tests and clean test files after execution.

### Latest Technical Notes

- Django 5.2 file upload handling places uploaded files in `request.FILES`; multipart forms must use `enctype="multipart/form-data"`.
- Django 5.2 docs recommend binding file uploads to forms with both `request.POST` and `request.FILES`.
- Django 5.2 documents a custom multiple-file field/widget pattern for validating every file in a single field, and warns that multiple files cannot be stored in one model `FileField`.
- Django 5.2 `ModelForm` is suitable for mapping Listing model fields while keeping ownership/profile fields out of user-editable inputs.
- Django 5.2 CSRF protection should remain active for POST forms; do not exempt the publication view unless a custom upload handler absolutely requires it.

### Anti-Patterns To Avoid

- Allowing publication without an eligible Commissionnaire Profile.
- Accepting a profile id from POST data as the Listing owner.
- Saving a Listing for a missing/incomplete profile.
- Saving invalid photos or silently dropping them while creating the Listing.
- Creating a public `available` Listing before moderation/publication rules exist.
- Using floats for money.
- Trusting uploaded file names, extensions, or MIME type without content validation.
- Accepting SVG or generated/renders as ordinary production photos.
- Creating a separate upload API, DRF endpoint, cloud upload flow, or background processing.
- Building preview, moderation, verification, Lead, WhatsApp, Report, or availability reconfirmation flows in this story.

### References

- `_bmad-output/planning-artifacts/epics.md#Story-2.5-Commissionnaire-Listing-Submission`
- `_bmad-output/planning-artifacts/epics.md#UX-DR24`
- `_bmad-output/planning-artifacts/epics.md#UX-DR26`
- `_bmad-output/planning-artifacts/epics.md#UX-DR27`
- `_bmad-output/planning-artifacts/epics.md#UX-DR35`
- `_bmad-output/planning-artifacts/epics.md#UX-DR36`
- `_bmad-output/planning-artifacts/prds/prd-maison-2026-05-31/prd.md#FR-4-Create-a-Commissionnaire-Profile`
- `_bmad-output/planning-artifacts/prds/prd-maison-2026-05-31/prd.md#FR-5-Submit-a-valid-rental-Listing`
- `_bmad-output/planning-artifacts/architecture.md#Commissionnaire-access`
- `_bmad-output/planning-artifacts/architecture.md#Security-posture`
- `_bmad-output/planning-artifacts/architecture.md#Implementation-Patterns-and-Consistency-Rules`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/DESIGN.md#Commissionnaire-Operations`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/DESIGN.md#Photography-and-Trust`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/EXPERIENCE.md#Commissionnaire-Operations`
- `_bmad-output/implementation-artifacts/1-5-commissionnaire-profile-management.md`
- `_bmad-output/implementation-artifacts/2-4-listing-detail-surface.md`
- `https://docs.djangoproject.com/en/5.2/topics/http/file-uploads/`
- `https://docs.djangoproject.com/en/5.2/topics/forms/modelforms/`
- `https://docs.djangoproject.com/en/5.2/topics/forms/formsets/`
- `https://docs.djangoproject.com/en/5.2/ref/csrf/`

## Dev Agent Record

### Agent Model Used

Gemini 3.5 Flash (High)

### Debug Log References

- Baseline tests passed successfully.
- Implemented `submit_listing_for_commissionnaire` service in `apps/listings/services.py` with transactional security, media checking, and disk cleanup on failure.
- Implemented `ListingSubmissionForm` in `apps/listings/forms.py` using custom `MultipleFileField` and styling controls.
- Registered views and URLs in `apps/commissionnaires/views.py` and `apps/commissionnaires/urls.py` with authentication, WhatsApp phone gate, and profile eligibility checks.
- Rendered UI templates with concise French copy and proper touch targets.
- Created robust unit and integration tests covering security, form validations, service transactions, and rendering checks.

### Completion Notes List

- Implemented the complete monthly price publication flow for Commissionnaires.
- Verified that anonymous and ineligible users are correctly redirected.
- Satisfied Kent Beck's TDD practices and the Pragmatic Programmer's quality requirements.
- Completed all ACs and verification steps successfully.

### File List

- `apps/listings/forms.py`
- `apps/listings/services.py`
- `apps/listings/tests/test_submission_services.py`
- `apps/commissionnaires/views.py`
- `apps/commissionnaires/urls.py`
- `apps/commissionnaires/tests/test_listing_submission_access.py`
- `apps/commissionnaires/tests/test_listing_submission_views.py`
- `templates/commissionnaires/listing_submission.html`
- `templates/commissionnaires/listing_submitted.html`
- `_bmad-output/implementation-artifacts/2-5-commissionnaire-listing-submission.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`

### Change Log

- Add monthly rental listing submission flow for Commissionnaires with multi-photo uploads (Date: 2026-06-09).
