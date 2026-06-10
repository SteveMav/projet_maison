---
baseline_commit: 83de0f8f0b1584d8b991f06922f9a3af5385d75b
---

# Story 2.6: Listing Preview And Submission Validation

Status: review

<!-- Validation: created from bmad-create-story workflow on 2026-06-06. -->

## Story

As a Commissionnaire,
I want to preview my Listing before submission,
so that I can catch missing or misleading information before it enters moderation or public inventory.

## Acceptance Criteria

1. Given a Commissionnaire has entered draft Listing information, when they open the preview step, then Maison renders a preview of the future Listing Card using the current price, Commune, bedroom count, primary photo, and availability/freshness display, and the preview never shows a Verification Badge before moderation.
2. Given the draft Listing lacks required publication data, when the Commissionnaire attempts final submission, then Maison blocks submission and shows precise correction guidance for missing fields, insufficient photos, or unusable media.
3. Given the draft Listing meets the publication standard, when the Commissionnaire submits it, then Maison moves it into the correct initial moderation or publication state defined for MVP and shows a confirmation explaining the next operational state.
4. Given publication flow states render on mobile, when the Commissionnaire moves between entry, preview, correction, and confirmation, then Maison preserves entered values and avoids full-page spinners, oversized dashboard cards, or decorative UI that slows the task.

## Tasks / Subtasks

- [x] Verify prerequisites and current implementation state (AC: 1, 2, 3, 4)
  - [x] Confirm Stories 1.1 through 2.5 are implemented or work from a branch where they are complete.
  - [x] Confirm Story 1.4 phone completion gate is enforced before Commissionnaire publication.
  - [x] Confirm Story 1.5 `CommissionnaireProfile` exists, belongs to the signed-in user, and exposes an eligibility check.
  - [x] Confirm Story 2.1 `Listing`, `ListingPhoto`, media validation, deterministic primary photo/order, and safe availability/moderation fields exist.
  - [x] Confirm Story 2.2 Listing Card rendering exists as a reusable include or extract it before adding a preview-specific duplicate.
  - [x] Confirm Story 2.5 publication form/service exists; extend it instead of creating a parallel submit path.
  - [x] Read current `apps/accounts`, `apps/listings`, `apps/commissionnaires`, `templates/listings`, `templates/commissionnaires`, `static_src`, `config/urls.py`, and tests before editing.
  - [x] Preserve unrelated sprint status changes already present, including stories marked `review` or `in-progress`.

- [x] Add preview-aware publication flow states (AC: 1, 4)
  - [x] Keep the Commissionnaire publication route protected by login, phone gate, and profile eligibility.
  - [x] Extend the existing `/pro/listings/new/` or established Story 2.5 route to support at least `entry`, `preview`, `correction`, and `confirmation`.
  - [x] Prefer explicit POST intents such as `action=preview`, `action=edit`, and `action=submit` over route guessing or JavaScript-only state.
  - [x] Render the entry state with the same form fields from Story 2.5: monthly price, Commune, bedroom count, description, intended availability, and photos.
  - [x] Render preview only after submitted form data is normalized enough to create an accurate card preview.
  - [x] Keep the preview state server-authoritative; JavaScript may improve transitions but cannot be the only path.
  - [x] Keep all state-changing requests CSRF-protected.
  - [x] Do not expose another Commissionnaire's draft, temp media, Listing, profile, or moderation data.

- [x] Implement safe draft or preview persistence (AC: 1, 2, 3, 4)
  - [x] Preserve text/select field values across entry, preview, correction, and final submit.
  - [x] Do not store raw uploaded file objects or file bytes in the session.
  - [x] Do not move uploaded photo content through hidden inputs, base64 fields, query strings, or unsigned client data.
  - [x] Preferred implementation: create a short-lived, owner-scoped preview draft bundle for validated uploaded photos and normalized listing fields, then consume it on final submit.
  - [x] Bind any draft token to the signed-in user and their `CommissionnaireProfile`; reject tokens owned by another user/profile.
  - [x] Give preview drafts an expiry timestamp and a cleanup path for expired temp media.
  - [x] Delete or invalidate the preview draft after successful final submit so browser refresh/back cannot create duplicate Listings.
  - [x] If a prior story already implemented a durable `draft` state, reuse it only if it remains non-public, owner-scoped, and excluded from moderation/public browse until final submit.
  - [x] Re-run all required validation on final submit; do not trust a previously rendered preview, hidden fields, or stale draft token as proof of validity.
  - [x] If temp file persistence is not implemented, keep the preview inside a single browser-held form state and clearly test that final upload still submits the original `File` objects; do not claim server-side preservation that does not exist.

- [x] Render a future Listing Card preview without trust overclaiming (AC: 1)
  - [x] Reuse the Listing Card include/component from Story 2.2 if it exists.
  - [x] If the public card include assumes a persisted `Listing`, add a small adapter/view model rather than duplicating card markup.
  - [x] Display current monthly price, Commune, bedroom count, primary photo, intended availability, and freshness/last-update style copy.
  - [x] For unsaved drafts, use preview-specific freshness copy such as `Brouillon - aujourd'hui` or `Aperçu non publié`; do not imply real-time availability.
  - [x] Use the first valid uploaded photo as the default primary preview unless a prior story added explicit primary selection.
  - [x] Keep the preview card image-first and scannable on mobile.
  - [x] Remove, hide, or inert any public-only card actions that do not make sense in preview, including favorite and public navigation.
  - [x] Never render `Annonce vérifiée`, a Verification Badge, a verification icon, or verification explanation in preview.
  - [x] Do not link the preview to a public Listing Detail Page before moderation/publication allows it.

- [x] Block invalid final submission with precise correction guidance (AC: 2, 4)
  - [x] Reuse Story 2.5 form and media validators for final submission.
  - [x] Require monthly price, Commune, bedroom count, description, intended availability, and at least three usable real photos.
  - [x] Validate price as a positive integer USD amount; do not use floats.
  - [x] Validate field content after trimming whitespace.
  - [x] Reject insufficient photos after invalid/unusable media are removed from the accepted set.
  - [x] Identify missing fields near the field that needs correction.
  - [x] Identify media corrections near the upload/accepted-photo list, including unsupported, corrupt, empty, oversized, SVG, or unusable files.
  - [x] Preserve accepted draft data when final validation fails and return to a correction state.
  - [x] Preserve valid text/select field values even when media corrections are required.
  - [x] Do not silently drop invalid files while creating a Listing.
  - [x] Do not create a Listing when required data or required usable media are missing.

- [x] Submit valid preview data into the correct initial state (AC: 3)
  - [x] Final submit must call the same Story 2.5 state-changing service or refactor that service so preview and direct validation share one path.
  - [x] Use `transaction.atomic()` around Listing and ListingPhoto creation.
  - [x] Associate the Listing with exactly one `CommissionnaireProfile` derived from the authenticated user, never from POST data.
  - [x] Store `submitted_at` on successful submission and rely on `updated_at` or equivalent for last update time.
  - [x] Save accepted photos in deterministic order and set the primary photo consistently.
  - [x] Start submitted Listings in the safe MVP initial state, normally `under_review` / awaiting moderation unless a prior story explicitly defines another non-public initial state.
  - [x] Ensure public browse, search, and detail surfaces still exclude submitted Listings until publication rules allow visibility.
  - [x] Show a confirmation such as `Envoyée pour modération` and explain the next operational state without claiming the Listing is public or verified.
  - [x] Avoid duplicate Listing creation on refresh, back/forward resubmit, or repeated final submit with the same draft token.

- [x] Build mobile-first preview/correction UI (AC: 1, 2, 3, 4)
  - [x] Use a short publication stepper with quiet inactive steps and an accent active step.
  - [x] Keep compact operational rows and hairline dividers; avoid nested dashboard cards and oversized hero metrics.
  - [x] Use visible French labels and concise Maison copy.
  - [x] Keep controls at least 44px tappable; primary actions at least 48px high.
  - [x] Show local loading/disabled state near the action being submitted.
  - [x] Avoid full-page spinners.
  - [x] Announce form-level failures through an appropriate live region or equivalent accessible error summary.
  - [x] Use text plus icon/status cues where status is shown; do not rely on color alone.
  - [x] Preserve keyboard reachability and visible focus.

- [x] Add tests for preview, validation, submission, and state preservation (AC: 1, 2, 3, 4)
  - [x] Test anonymous users are redirected to login with `next`.
  - [x] Test authenticated users without WhatsApp phone are routed through the phone gate.
  - [x] Test authenticated users without eligible `CommissionnaireProfile` cannot preview or submit.
  - [x] Test a Commissionnaire cannot preview or submit another Commissionnaire's draft token/temp media.
  - [x] Test preview renders price, Commune, bedroom count, primary photo, availability/freshness display, and no Verification Badge.
  - [x] Test preview uses the same card include/view-model shape as public Listing Cards where practical.
  - [x] Test missing required fields block final submit and return precise errors.
  - [x] Test fewer than three usable photos blocks final submit.
  - [x] Test corrupt, empty, unsupported, SVG, oversized, or unusable images are rejected and not accepted into the final Listing.
  - [x] Test invalid final submit preserves text/select values and accepted draft photos or clearly preserves the same browser-held file state if that implementation pattern is chosen.
  - [x] Test valid final submit creates exactly one Listing and the expected ListingPhoto records.
  - [x] Test valid final submit sets owner, timestamps, initial non-public state, photo order, and primary photo.
  - [x] Test public browse/detail do not expose the submitted under-review Listing.
  - [x] Test repeated final submit or refresh does not create duplicate Listings.
  - [x] Test expired or consumed draft tokens are rejected cleanly.
  - [x] Test temp media cleanup where temp persistence is implemented.

- [x] Run required checks (AC: 1, 2, 3, 4)
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

- Story source: `_bmad-output/planning-artifacts/epics.md`, Epic 2, Story 2.6.
- Requirements: FR-5; UX-DR10, UX-DR24, UX-DR27, UX-DR34.
- FR-5 requires monthly price, Commune, bedroom count, description, Availability Status, at least three photos, media rejection with correction guidance, submission/update timestamps, and association with exactly one Commissionnaire Profile.
- UX-DR10 defines Listing Card content: image-first layout, Commune, price, bedroom count, freshness, and optional verified label only when applicable.
- UX-DR24 requires Commissionnaire operational states such as draft, awaiting moderation, and correction required.
- UX-DR27 requires a short mobile-friendly publication flow with precise correction messages, at least three real photos, and a Listing Card preview before submission.
- UX-DR34 requires concise French copy and trust language that avoids inflated claims.

### Dependency On Previous Stories

This story depends on Stories 1.1 through 2.5.

Required previous foundations:

- Story 1.4: WhatsApp phone completion gate.
- Story 1.5: eligible `CommissionnaireProfile` linked to exactly one user.
- Story 2.1: `Listing`, `ListingPhoto`, local media storage, image validators, primary photo behavior, and safe availability/moderation values.
- Story 2.2: reusable Listing Card rendering and public browse exclusion for non-available Listings.
- Story 2.3: filter/query behavior continues excluding under-review or unavailable Listings.
- Story 2.4: detail surfaces avoid verification overclaims and hide non-public Listings.
- Story 2.5: protected Commissionnaire publication route, form validation, media validation, atomic final submission service, and confirmation surface.

If any prerequisite is missing, implement it first or work from the branch where it exists. Do not create a second profile, listing, media, card, or submission system in this story.

### Current Workspace Snapshot

Targeted file inspection during story creation found the following current state:

- `apps/accounts` exists with `CustomUser`, email login/registration forms, account views, account URLs, and tests.
- `CustomUser` has `email` and `whatsapp_phone`; phone completion behavior must still come from Story 1.4.
- `config/settings.py` includes `apps.listings`, `apps.commissionnaires`, `apps.leads`, `apps.moderation`, `apps.audit`, and `apps.pwa`.
- `config/settings.py` includes SQLite, `MEDIA_URL`, `MEDIA_ROOT`, `AUTH_USER_MODEL`, static settings, and Africa/Kinshasa timezone.
- `config/urls.py` includes core, accounts, admin, and debug media serving only.
- `apps/listings` currently has app config, migrations package, and test package only; no models, forms, selectors, services, views, or URLs are present in this workspace snapshot.
- `apps/commissionnaires` currently has app config, migrations package, and test package only; no models, forms, views, or URLs are present in this workspace snapshot.
- `templates/base.html`, `templates/core/home.html`, and account templates exist; `templates/listings/` and `templates/commissionnaires/` do not exist yet.
- `requirements.txt` currently pins only `Django==5.2.14`; Pillow is not present in the current file, so Story 2.1's image validation dependency must be added before media validation can be implemented robustly.
- `package.json` has Tailwind CSS `4.3.0` and scripts `css:build` and `css:watch`.
- `static_src/css/input.css` contains Maison tokens, form/button styles, visible focus styles, and a `max-width: 700px` mobile breakpoint.

This means the dev agent must not assume Listing/Profile implementation is present in the current workspace unless earlier stories have been implemented after this story was created.

### Previous Story Intelligence

- Story 2.5 owns protected publication access, required field collection, media upload validation, atomic Listing + ListingPhoto creation, and safe confirmation.
- Story 2.5 explicitly left the full Listing Card preview and final preview-state correction flow for this story.
- Story 2.5 recommends `under_review` as the safe initial state when no separate moderation state exists.
- Story 2.5 requires ownership to come from the authenticated user's `CommissionnaireProfile`, not from raw POST ids.
- Story 2.1 requires media validation to inspect actual image content, not just filename, extension, or browser-provided MIME type.
- Stories 2.2 and 2.4 protect public surfaces by excluding `under_review` Listings and avoiding unearned verification claims.
- This story should refactor Story 2.5 only as much as needed to insert preview and final validation; it must not expand into moderation, availability reconfirmation, Leads, reports, or verification.

### Architecture Compliance

- Use Django 5.2.14 LTS with server-rendered views and templates.
- Use Django forms for validation and form state preservation.
- Use small service functions for state-changing workflows.
- Keep business logic out of templates.
- Keep POST forms CSRF-protected.
- Keep Commissionnaire/pro routes authenticated and server-authorized.
- Use local media storage through `MEDIA_ROOT` and `MEDIA_URL`.
- Use Tailwind CLI and existing Maison CSS tokens; no Tailwind CDN.
- Keep JavaScript modular and progressive; no inline JavaScript for business behavior.
- No public `/api/` namespace and no Django REST Framework.
- Do not introduce React, Vue, SPA routing, Redis, PostgreSQL, object storage, direct-to-S3 uploads, background workers, or payments.

### Recommended Flow Contract

Recommended URL shape, adapting to the actual Story 2.5 route names:

```python
app_name = "commissionnaires"

urlpatterns = [
    path("listings/new/", views.ListingPublicationView.as_view(), name="listing_submit"),
    path("listings/<int:pk>/submitted/", views.ListingSubmittedView.as_view(), name="listing_submitted"),
]
```

Recommended request behavior:

- `GET`: render entry step for an eligible Commissionnaire.
- `POST action=preview`: bind `request.POST` and `request.FILES`, validate enough to create or refresh an owner-scoped preview draft, and render preview.
- `POST action=edit`: return to entry/correction with preserved draft values.
- `POST action=submit`: revalidate current draft/form/media server-side, create the Listing atomically, consume draft/temp media, and redirect to confirmation.
- invalid `POST`: render correction state with field-level/media-specific errors and preserved safe values.

Recommended service boundaries:

```python
def build_listing_preview_context(*, profile, form_data, uploaded_photos):
    # Validate and normalize draft data.
    # Persist or adapt temp photos safely if the flow spans multiple requests.
    # Return a card-shaped view model, not a public Listing.

@transaction.atomic
def submit_listing_for_commissionnaire(*, profile, draft_or_cleaned_data):
    # Re-run final validation.
    # Create Listing and ListingPhoto rows once.
    # Set submitted_at and safe initial moderation/publication state.
    # Consume draft token/temp media.
    # Return the submitted Listing.
```

Names can differ, but the separation must remain: preview builds a non-public card model; final submit performs the authoritative state transition.

### Draft And Temp Media Guardrails

The tricky part of this story is preserving photos across preview and correction. Browsers cannot safely repopulate a file input after a server round trip, and Django sessions are not the right place for raw file content.

Allowed patterns:

- Preferred: short-lived server-side preview draft with temp photo files bound to the authenticated Commissionnaire Profile.
- Acceptable if already implemented: a durable draft state that is owner-scoped, non-public, excluded from browse/detail/moderation queues until final submit, and revalidated before submit.
- Acceptable for a lightweight no-temp implementation only if preview stays in the same browser-held form state and final submission still sends the original `File` objects in the same page flow.

Rejected patterns:

- Raw file bytes in `request.session`.
- Base64 image content in hidden fields.
- Unsigned draft ids or profile ids accepted from POST.
- Creating a public or moderation-visible Listing before final submit.
- Treating a preview-rendered card as proof that final validation has passed.

If using temp files:

- Store them under a clearly temporary path such as `listing-preview-drafts/<profile_id>/<token>/`.
- Never expose filesystem paths to users.
- Store only sanitized metadata needed for correction display, such as original display name and validation status.
- Reopen/revalidate image content on final submit.
- Delete invalid, expired, consumed, or abandoned temp media where practical.
- Test cleanup with a temporary `MEDIA_ROOT`.

### Preview Card Guardrails

The preview card should represent the future public card without becoming a public card.

Required preview fields:

- monthly price
- Commune
- bedroom count
- primary/first accepted photo
- intended availability or submitted availability label
- freshness/last-update style copy

Preview-only behavior:

- no public detail link
- no active favorite action
- no Verification Badge
- no verified explanation
- no claim that Maison has reviewed, published, or guaranteed the Listing
- no implication that availability has been independently confirmed

Recommended French copy:

- `Aperçu de l'annonce`
- `Brouillon - aujourd'hui`
- `Aperçu non publié`
- `Vérifiez les informations avant envoi.`
- `Modifier`
- `Envoyer pour modération`

### Final State Guardrails

Maison separates three ideas:

- draft/preview: the Commissionnaire is still editing and nothing should be public
- awaiting moderation / under review: the Listing was submitted and is not public yet unless MVP rules explicitly publish it
- verified: a later Moderator-only trust state, never earned during submission

If the implementation has only `Listing.availability_status` with `available`, `unavailable`, and `under_review`, final submit should use:

```python
listing.availability_status = Listing.AvailabilityStatus.UNDER_REVIEW
```

If the implementation has separate moderation and availability fields:

- set moderation state to awaiting moderation / submitted
- store the Commissionnaire's intended availability separately
- keep the Listing excluded from public browse/detail until moderation publishes it

Confirmation should say `Envoyée pour modération` unless a prior accepted MVP decision says ordinary publication happens immediately. Even then, the story must never show a Verification Badge or imply verification.

### UX And Copy Guardrails

Use concise French UI copy:

- `Publier un bien`
- `Informations du logement`
- `Photos du logement`
- `Aperçu`
- `Correction requise`
- `Ce champ est obligatoire.`
- `Ajoutez au moins 3 photos réelles du logement.`
- `Photo inutilisable. Ajoutez une image JPG, PNG ou WebP nette du logement.`
- `Cette annonce n'est pas encore publiée.`
- `Envoyer pour modération`
- `Envoyée pour modération`

Avoid:

- `100% garanti`
- `Toujours disponible`
- `Annonce vérifiée` in preview or submitted state
- vague `Une erreur est survenue` without recovery
- decorative dashboard copy, motivational banners, or oversized metrics

### Scope Boundaries

Implement now:

- Preview step in the Commissionnaire publication flow.
- Safe preservation of entered values and accepted preview media according to the chosen pattern.
- Listing Card preview using current draft values.
- Final validation that blocks missing fields, insufficient photos, and unusable media.
- Final submit into the safe MVP initial state.
- Confirmation explaining the next operational state.
- Tests for preview, correction, submission, ownership, public exclusion, and duplicate prevention.

Do not implement now:

- Moderator queue, moderation decisions, correction request workflow, rejection/removal, or verification checklist.
- Verification Badge application/removal.
- Availability reconfirmation and status-change history; Story 2.7 owns this.
- Leads, WhatsApp handoff, reports, favorites, view counts, analytics, audit timeline UI, notifications, direct cloud uploads, or background image processing.

### File Structure Requirements

Expected files to create or update, assuming prerequisites are implemented:

```text
apps/listings/
├── forms.py
├── services.py
├── selectors.py            # only if existing card/detail selectors need a preview adapter
├── models.py               # only if adding a draft/temp-media model
├── validators.py           # reuse from Story 2.1
└── tests/
    ├── test_listing_preview.py
    ├── test_submission_forms.py
    ├── test_submission_services.py
    └── test_media_validation.py
apps/commissionnaires/
├── views.py
├── urls.py
└── tests/
    ├── test_listing_preview_access.py
    └── test_listing_preview_views.py
templates/listings/
├── includes/
│   └── listing_card.html    # reuse/update if created by Story 2.2
templates/commissionnaires/
├── listing_submission.html  # entry/preview/correction states, or split if existing pattern prefers it
└── listing_submitted.html
static_src/css/
└── input.css                # preview/stepper styles only if needed
config/
└── urls.py                  # include commissionnaire URLs if missing
```

Adapt names to the actual files created by previous stories. Read every existing target file before editing.

### Testing Requirements

Minimum tests:

- Access:
  - anonymous user redirects to login with `next`
  - authenticated user without WhatsApp phone hits the phone gate
  - authenticated user without eligible profile cannot preview or submit
  - one Commissionnaire cannot access another Commissionnaire's draft token/temp media
- Preview:
  - preview card renders price, Commune, bedroom count, primary photo, availability/freshness copy
  - preview card never renders Verification Badge or verified copy
  - preview does not create a public Listing
  - preview does not expose a public detail link for an unpublished Listing
- Correction:
  - missing required fields return field-level errors
  - insufficient usable photos returns media-specific errors
  - invalid media returns precise correction messages
  - valid text/select values remain visible after correction
  - accepted draft media remains available if using temp persistence
- Final submit:
  - valid draft creates one Listing and expected ListingPhoto records
  - owner is the authenticated user's `CommissionnaireProfile`
  - `submitted_at` and `updated_at` behavior is correct
  - initial state is `under_review` / awaiting moderation or the accepted MVP equivalent
  - photo order and primary photo are deterministic
  - public browse/detail exclude the submitted Listing
  - duplicate final submit does not create duplicate Listings
  - consumed or expired draft token cannot be reused
- Template/accessibility:
  - form uses `multipart/form-data`
  - CSRF token renders for POST forms
  - visible French labels render
  - error summary or live region exists for correction failures
  - primary actions have disabled/loading states

Use Django's built-in test runner and temporary `MEDIA_ROOT` for upload/temp media tests.

### Latest Technical Notes

- Django 5.2 file uploads arrive in `request.FILES`; it is populated only for multipart POST forms with `enctype="multipart/form-data"` and posted file fields.
- Bind uploaded files to forms with both `request.POST` and `request.FILES`.
- Django 5.2 documents a custom multiple-file widget/field pattern for validating every uploaded file in one form field, while warning that multiple files cannot be stored in one model `FileField`.
- Use `UploadedFile.chunks()` when writing uploaded content so large files do not force full reads into memory.
- Django forms preserve submitted field values when a bound invalid form is re-rendered; uploaded files need a separate draft/temp strategy if they must survive a server round trip.
- Django `ModelForm` can include only safe user-editable Listing fields; keep ownership, moderation state, timestamps, and verification fields out of user-editable inputs.
- Django sessions can hold lightweight tokens/state, but not raw upload content for this flow.
- Django messages are appropriate for broad temporary confirmation/status messages; precise validation belongs next to fields/media controls.

### Anti-Patterns To Avoid

- Building a second publication flow instead of extending Story 2.5.
- Duplicating Listing Card markup instead of reusing/adapting the Story 2.2 card include.
- Rendering any Verification Badge in preview or confirmation.
- Creating a public `available` Listing before moderation/publication rules allow it.
- Creating moderation queue behavior inside this story.
- Accepting a profile id, draft id, Listing id, or photo id from POST without owner checks.
- Storing uploaded file bytes in sessions, hidden inputs, or query strings.
- Trusting a preview token without revalidation on final submit.
- Dropping invalid photos silently and still submitting the Listing.
- Saving a partial Listing on invalid final submission.
- Using floats for money.
- Adding DRF, public APIs, cloud upload workflows, background processors, or frontend framework state.

### References

- `_bmad-output/planning-artifacts/epics.md#Story-2.6-Listing-Preview-And-Submission-Validation`
- `_bmad-output/planning-artifacts/epics.md#UX-DR10`
- `_bmad-output/planning-artifacts/epics.md#UX-DR24`
- `_bmad-output/planning-artifacts/epics.md#UX-DR27`
- `_bmad-output/planning-artifacts/epics.md#UX-DR34`
- `_bmad-output/planning-artifacts/prds/prd-maison-2026-05-31/prd.md#FR-5-Submit-a-valid-rental-Listing`
- `_bmad-output/planning-artifacts/architecture.md#Commissionnaire-access`
- `_bmad-output/planning-artifacts/architecture.md#Security-posture`
- `_bmad-output/planning-artifacts/architecture.md#Implementation-Patterns-and-Consistency-Rules`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/EXPERIENCE.md#Commissionnaire-Surfaces`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/EXPERIENCE.md#Trust-Contract`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/EXPERIENCE.md#UJ-2.-Patrick-publishes-a-useful-rental-Listing-from-his-phone`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/DESIGN.md#Listing-Card`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/DESIGN.md#Commissionnaire-Operations`
- `_bmad-output/implementation-artifacts/2-5-commissionnaire-listing-submission.md`
- `https://docs.djangoproject.com/en/5.2/topics/http/file-uploads/`
- `https://docs.djangoproject.com/en/5.2/ref/files/uploads/`
- `https://docs.djangoproject.com/en/5.2/topics/forms/`
- `https://docs.djangoproject.com/en/5.2/topics/forms/modelforms/`
- `https://docs.djangoproject.com/en/5.2/topics/http/sessions/`
- `https://docs.djangoproject.com/en/5.2/ref/contrib/messages/`

## Dev Agent Record

### Agent Model Used

Gemini 3.5 Flash (High)

### Debug Log References

- Verified all prerequisite listing and profile models.
- Updated `ListingSubmissionForm` in `apps/listings/forms.py` to support construction parameters (`has_draft_photos=True`) allowing optional uploads when reusing draft media.
- Refactored `ListingSubmissionView` in `apps/commissionnaires/views.py` to implement the three stepper flow phases (`entry`, `preview`, and `submit`) with server-side session-backed draft validation.
- Restructured `action == "submit"` handling to prevent file locks on Windows (closing files in `finally` before running `cleanup_draft_files`).
- Modified `listing_card.html` to support `is_preview` parameter, rendering as an inert `div` to block navigation in preview cards.
- Wrote robust tests in `test_listing_preview_views.py` for card rendering, value preservation, duplicate submission prevention, and file cleanups. All 207 tests are passing.

### Completion Notes List

- Implemented full publication flow with preview, edit/entry, correction, and final submit.
- Handled Windows file locking securely.
- Verified draft token validation, expiry (1 hour), and cleanup.
- Ensured no Verification Badges or public routes are exposed in preview.

### File List

- `apps/listings/forms.py`
- `apps/commissionnaires/views.py`
- `apps/commissionnaires/tests/test_listing_preview_views.py`
- `apps/commissionnaires/tests/test_listing_submission_views.py`
- `templates/listings/includes/listing_card.html`
- `templates/commissionnaires/listing_submission.html`
- `_bmad-output/implementation-artifacts/2-6-listing-preview-and-submission-validation.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`

### Change Log

- Add Listing Card preview step, draft session management, and preview validation (Date: 2026-06-09).
