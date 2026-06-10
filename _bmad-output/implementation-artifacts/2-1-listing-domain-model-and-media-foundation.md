---
baseline_commit: 83de0f8f0b1584d8b991f06922f9a3af5385d75b
---

# Story 2.1: Listing Domain Model And Media Foundation

Status: review

<!-- Validation: created from bmad-create-story workflow on 2026-06-05. -->

## Story

As a product team,
I want the Listing and ListingPhoto foundation modeled around rental inventory,
so that Tenant discovery and Commissionnaire publication can share a consistent source of truth.

## Acceptance Criteria

1. Given the account and Commissionnaire Profile foundation exists, when the listing domain is implemented, then Maison can store a rental Listing linked to exactly one Commissionnaire Profile and the Listing stores monthly USD price, Commune, bedroom count, description, Availability Status, submission timestamp, and last update timestamp.
2. Given listing media is implemented, when photos are attached to a Listing, then Maison stores ListingPhoto records through local media storage and uploaded files are validated as usable images before being accepted.
3. Given a Listing has multiple photos, when the Listing is rendered later on card or detail surfaces, then one primary photo can be identified and photo ordering is deterministic.
4. Given a developer validates the domain foundation, when model and service tests run, then they verify Commissionnaire ownership, required Listing fields, image validation behavior, and valid Availability Status values.

## Tasks / Subtasks

- [x] Verify prerequisites and existing implementation state (AC: 1, 4)
  - [x] Confirm Stories 1.1 through 1.5 are implemented before coding this story.
  - [x] Confirm `apps.commissionnaires.models.CommissionnaireProfile` exists and exposes the profile eligibility invariant from Story 1.5.
  - [x] Read existing `apps/accounts`, `apps/commissionnaires`, project settings, URL config, and existing tests before editing.
  - [x] If no Django implementation exists yet, implement the prerequisite stories first rather than creating isolated Listing code.

- [x] Add the `listings` app domain models (AC: 1, 3, 4)
  - [x] Create or update `apps/listings/models.py`.
  - [x] Implement `Listing` linked to exactly one `CommissionnaireProfile` with `ForeignKey(..., related_name="listings", on_delete=models.PROTECT)`.
  - [x] Store monthly USD price without floats, using integer monthly amount plus explicit USD currency, or the existing project money field if one already exists.
  - [x] Store required `commune`, `bedroom_count`, `description`, `availability_status`, `submitted_at`, `created_at`, and `updated_at` fields.
  - [x] Use `models.TextChoices` for valid Availability Status values: `available`, `unavailable`, and `under_review`.
  - [x] Default new persisted Listings to `under_review` unless an existing submission workflow already sets a safer explicit value.
  - [x] Add indexes needed by later browse/filter stories: status plus recency, Commune, bedroom count, and price amount.
  - [x] Register `Listing` in Django admin with safe list display, filters, and search fields.

- [x] Add `ListingPhoto` and deterministic media ordering (AC: 2, 3, 4)
  - [x] Create `ListingPhoto` linked to `Listing` with `ForeignKey(..., related_name="photos", on_delete=models.CASCADE)`.
  - [x] Store the image with `ImageField(upload_to=...)` under local media storage.
  - [x] Add `position`, `is_primary`, optional `alt_text`, `created_at`, and `updated_at`.
  - [x] Set model ordering to `position`, then `id` for deterministic card/detail rendering.
  - [x] Enforce unique photo position per Listing.
  - [x] Enforce at most one explicit primary photo per Listing, using a conditional database constraint where supported and service-level enforcement regardless.
  - [x] Implement a selector or model helper that returns the explicit primary photo, otherwise the first ordered photo.
  - [x] Register photos in admin, preferably as an inline under Listing if the existing admin pattern supports it.

- [x] Implement media validation helpers (AC: 2, 4)
  - [x] Add `apps/listings/validators.py` or equivalent local helper.
  - [x] Require real raster images validated by Django/Pillow, not file names or client-provided MIME type alone.
  - [x] Allow only formats needed for mobile property photos, initially JPEG, PNG, and WebP unless the project already chose a narrower list.
  - [x] Reject unsupported extensions, empty files, corrupt images, SVG, and files above the configured maximum upload size.
  - [x] Keep validation constants in one place, for example `ALLOWED_LISTING_IMAGE_EXTENSIONS`, `ALLOWED_LISTING_IMAGE_FORMATS`, and `MAX_LISTING_PHOTO_BYTES`.
  - [x] Add user-facing validation messages that later forms can display as precise correction guidance.
  - [x] Do not attempt automated AI-image detection in this story; later moderation and copy guardrails handle the "real property photo" trust requirement.

- [x] Add listing services/selectors for safe state changes (AC: 1, 2, 3, 4)
  - [x] Add `apps/listings/services.py`.
  - [x] Implement a creation helper that requires a valid `CommissionnaireProfile`, persists required Listing fields, and never accepts a raw user id as the owner.
  - [x] Implement `add_listing_photo(listing, uploaded_file, position=None, is_primary=False, alt_text="")` or equivalent.
  - [x] Validate images before saving files.
  - [x] Ensure the first photo can become primary when no primary exists, or document and test the fallback primary selector.
  - [x] Implement `set_primary_photo(photo)` or equivalent so changing primary status clears any previous primary for the same Listing.
  - [x] Implement a publication-readiness helper that verifies required Listing fields and the minimum of three usable photos, without building the full submission UI from Story 2.5.
  - [x] Keep public browse selectors, detail rendering, publication forms, moderation decisions, Leads, Reports, and audit event tables out of this story unless prerequisite code already requires a minimal integration point.

- [x] Configure local media support if missing (AC: 2)
  - [x] Confirm project settings define `MEDIA_ROOT` and `MEDIA_URL` for local development.
  - [x] Confirm development URL config serves media only in `DEBUG` using Django's documented pattern.
  - [x] Confirm uploaded files are stored under a predictable `listings/...` media path and not under static assets.
  - [x] Do not introduce S3, cloud object storage, image CDN, or background processing in this story.

- [x] Add migrations and dependency pins (AC: 1, 2, 3, 4)
  - [x] Add the `listings` app migration for `Listing` and `ListingPhoto`.
  - [x] Add `Pillow==12.2.0` if `ImageField` support is not already pinned.
  - [x] Keep Django pinned to the architecture-selected `5.2.14` line unless a project-level dependency update has already changed it.
  - [x] Do not add Django REST Framework, PostgreSQL, Redis, Celery, or a JavaScript image uploader for this foundation.

- [x] Add model, service, and validation tests (AC: 1, 2, 3, 4)
  - [x] Test a Listing must reference exactly one `CommissionnaireProfile`.
  - [x] Test required price, Commune, bedroom count, description, status, submitted timestamp, and update timestamp behavior.
  - [x] Test valid Availability Status values and reject invalid values through model/form validation.
  - [x] Test monthly price is stored as an integer USD value, not a float.
  - [x] Test `on_delete=PROTECT` prevents accidental Commissionnaire Profile deletion while Listings exist.
  - [x] Test valid JPEG, PNG, and WebP uploads are accepted if supported by Pillow in the environment.
  - [x] Test corrupt, empty, unsupported, SVG, and oversized files are rejected before save.
  - [x] Test photo ordering is deterministic.
  - [x] Test at most one primary photo exists per Listing.
  - [x] Test primary photo fallback when no photo is explicitly marked primary.
  - [x] Test service helpers do not allow one Commissionnaire to mutate another Commissionnaire's Listing by passing forged identifiers.
  - [x] Use temporary `MEDIA_ROOT` in tests and clean uploaded files after tests.

- [x] Run required checks (AC: 1, 2, 3, 4)
  - [x] `python manage.py makemigrations --check --dry-run`
  - [x] `python manage.py migrate --check`
  - [x] `python manage.py check`
  - [x] `python manage.py test apps.listings`
  - [x] `python manage.py test`
  - [x] `python manage.py collectstatic --noinput --dry-run`

## Dev Notes

### Source Context

- Story source: `_bmad-output/planning-artifacts/epics.md`, Epic 2, Story 2.1.
- Requirements: FR-1, FR-3, FR-5, FR-6; NFR-2; UX-DR35, UX-DR36.
- Epic 2 goal: Commissionnaires publish and maintain useful rental inventory while Tenants browse, filter, and inspect available Listings.
- This story creates the domain and media foundation only. Tenant browse cards, search filters, detail drawers, Commissionnaire publication UI, availability reconfirmation, moderation, verification, reports, Leads, and analytics are later stories.

### Dependency On Previous Stories

This story depends on Stories 1.1 through 1.5.

Required earlier foundations:

- Story 1.1: Django 5.2 LTS project scaffold, apps package, settings, templates, static/media conventions, and Tailwind CLI baseline.
- Story 1.2: email/password authentication and safe protected-route behavior.
- Story 1.3: Google authentication through `django-allauth` with the custom user model.
- Story 1.4: WhatsApp phone completion gate and normalized phone storage.
- Story 1.5: `CommissionnaireProfile` as the stable FK target for future Listings and Leads.

If any prerequisite is missing, implement it first. Do not create a second Commissionnaire profile model, a second phone gate, or a duplicate user/profile ownership layer.

### Previous Story Intelligence

- Story 1.5 established that future `Listing` and `Lead` models must reference `CommissionnaireProfile`, not copy current user/display name as the source of truth.
- Story 1.5 requires profile updates to preserve the same profile row so future Listings and Leads keep attribution.
- Story 1.4 established that a valid phone number is not proof of WhatsApp account ownership. Listing ownership should depend on the persisted profile, not on WhatsApp proof claims.
- Story 1.1 established no DRF, no React, no Redis, no PostgreSQL, and no payment stack for MVP foundations.
- No implemented Django code was present in the repository during story creation; the developer must read actual code before editing and adapt paths only if prerequisite implementation chose equivalent names.

### Architecture Compliance

- Use Django models, ModelForms where forms are needed, services for state-changing workflows, selectors/helpers for reads, and server-rendered templates later.
- Keep business logic out of templates.
- Keep media uploads in local filesystem storage via `MEDIA_ROOT` and `MEDIA_URL`.
- Use SQLite-compatible schema and constraints for local development.
- Use explicit timestamp names: `created_at`, `updated_at`, `submitted_at`, and optional `availability_changed_at` if implemented now for FR-6 foundation.
- Status values must be lowercase `snake_case`.
- Use Django's built-in test runner.
- Treat uploaded media as untrusted content. Do not rely on file name, extension, or browser-provided MIME type alone.
- Do not expose public REST, GraphQL, or mobile API endpoints for Listing foundations.

### Recommended Domain Model

Recommended `Listing` shape:

```python
class Listing(models.Model):
    class AvailabilityStatus(models.TextChoices):
        AVAILABLE = "available", "Available"
        UNAVAILABLE = "unavailable", "Unavailable"
        UNDER_REVIEW = "under_review", "Under review"

    class Currency(models.TextChoices):
        USD = "USD", "USD"

    commissionnaire_profile = models.ForeignKey(
        "commissionnaires.CommissionnaireProfile",
        on_delete=models.PROTECT,
        related_name="listings",
    )
    monthly_price_amount = models.PositiveIntegerField()
    monthly_price_currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.USD,
    )
    commune = models.CharField(max_length=120)
    bedroom_count = models.PositiveSmallIntegerField()
    description = models.TextField()
    availability_status = models.CharField(
        max_length=32,
        choices=AvailabilityStatus.choices,
        default=AvailabilityStatus.UNDER_REVIEW,
    )
    submitted_at = models.DateTimeField(null=True, blank=True)
    availability_changed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

Recommended `ListingPhoto` shape:

```python
class ListingPhoto(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    image = models.ImageField(upload_to=listing_photo_upload_to)
    position = models.PositiveSmallIntegerField(default=0)
    is_primary = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=180, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["position", "id"]
```

Model notes:

- `monthly_price_amount` stores the whole monthly USD amount as an integer. Do not use `FloatField` for money.
- `monthly_price_currency` is explicit even though USD is the only MVP currency.
- `submitted_at` may remain null for future draft flows, but submitted Listings must persist it.
- `availability_changed_at` is optional in this story but useful for FR-6; Story 2.7 owns the full availability transition workflow.
- `on_delete=models.PROTECT` prevents accidental deletion of a Commissionnaire Profile that owns Listings.
- Use `CheckConstraint` for non-negative price and bedroom count if not already guaranteed by field type.
- Use `Meta.indexes` rather than scattered `db_index=True` where practical.

### Media Validation Guardrails

Use Django `ImageField` plus explicit project validation:

- Bind uploaded files through `request.FILES` when forms are introduced.
- Validate with Pillow-backed image opening/verification before save.
- Allow only JPEG, PNG, and WebP unless the project already chose a narrower list.
- Reject SVG because it is not a raster property photo and can carry script-like content in some serving contexts.
- Enforce a maximum byte size through a project constant or setting.
- Save only after validation succeeds.
- Generate server-owned upload paths; do not trust the original filename for path or extension decisions.
- Tests should use `SimpleUploadedFile` or `ContentFile` and `override_settings(MEDIA_ROOT=temp_dir)`.

The UX requirement for real property photography cannot be fully automated. This story enforces technical usability; later publication and moderation stories enforce correction copy and human review boundaries.

### Scope Boundaries

Implement now:

- `Listing` and `ListingPhoto` models.
- Local media storage configuration if missing.
- Image validators.
- Listing/photo services and selectors needed to test ownership, validation, primary photo, ordering, and readiness.
- Migrations, admin registration, and tests.

Do not implement now:

- Public browse page, Listing cards, filters, empty states, or detail drawer.
- Commissionnaire publication stepper or preview UI.
- Availability reconfirmation workflow.
- Moderation queue, moderation decisions, Verification Badge, Reports, Leads, audit event tables, or WhatsApp handoff.
- Favorite action, view counts, neighborhood/property-type fields, bathroom counts, or SEO slugs unless an existing implemented story already introduced them.
- Cloud media storage, CDN transforms, async image processing, or client-side upload widgets.

### File Structure Requirements

Expected files to create or update, assuming the prerequisite Django scaffold exists:

```text
apps/
└── listings/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── validators.py
    ├── selectors.py
    ├── services.py
    ├── forms.py              # optional now, useful if validation is form-backed
    ├── migrations/
    │   ├── __init__.py
    │   └── 0001_initial.py
    └── tests/
        ├── __init__.py
        ├── test_models.py
        ├── test_services.py
        └── test_validators.py
config/
└── settings.py               # or settings package used by Story 1.1
```

Read existing files before editing. Preserve account auth, Google auth, WhatsApp phone gate, Commissionnaire profile behavior, base settings, and any existing app registration conventions.

### Testing Requirements

Minimum tests:

- Model:
  - Listing requires `commissionnaire_profile`.
  - Listing deletion does not delete the owning profile.
  - Profile deletion is protected while Listings exist.
  - required Listing fields validate.
  - status values are limited to `available`, `unavailable`, and `under_review`.
  - price is integer USD and rejects invalid numeric values.
  - `created_at`, `updated_at`, and submitted timestamp behavior are covered.
- Photo:
  - valid image upload persists a `ListingPhoto` under test media.
  - corrupt, empty, unsupported, SVG, and oversized files fail validation before save.
  - ordering is stable by `position`, then `id`.
  - primary photo selector returns explicit primary when present.
  - primary photo selector falls back to first ordered photo when no explicit primary exists.
  - service prevents multiple explicit primary photos for one Listing.
- Ownership/services:
  - services accept `CommissionnaireProfile` as owner, not raw users.
  - a Commissionnaire cannot mutate a Listing owned by another profile through forged ids.
  - publication-readiness helper requires required fields and at least three usable photos.

Avoid browser tests for this story unless the implementation already has a frontend test layer. This story is domain/model/media foundation work.

### Latest Technical Notes

- The project architecture intentionally selects Django `5.2.14 LTS` even though newer Django versions exist, so use Django 5.2 docs and APIs for implementation.
- Django `ImageField` validates that uploaded content is a valid image and inherits `FileField` behavior.
- Django form `ImageField` requires Pillow and file data must be bound to the form.
- Django file upload docs warn that uploaded content from untrusted users has security risks; keep upload validation strict.
- As of 2026-06-05, PyPI lists Pillow `12.2.0` published on 2026-04-01. Pin this version unless the project has already pinned a newer safe version.

### Anti-Patterns To Avoid

- Storing Listing owner as a raw user FK instead of `CommissionnaireProfile`.
- Copying Commissionnaire display name or phone into Listing as the attribution source of truth.
- Using floats for money.
- Treating `under_review` Listings as publicly searchable.
- Allowing one Listing to have two explicit primary photos.
- Depending on upload file names, extensions, or browser MIME types without content validation.
- Accepting SVG, corrupt images, or empty files as property photos.
- Writing uploaded files to static assets.
- Building public discovery, publication UI, moderation, or Leads inside this foundation story.
- Claiming Maison verifies every Listing or guarantees availability/accuracy.

### References

- `_bmad-output/planning-artifacts/epics.md#Story-2.1-Listing-Domain-Model-And-Media-Foundation`
- `_bmad-output/planning-artifacts/epics.md#Epic-2-Rental-Inventory-Marketplace`
- `_bmad-output/planning-artifacts/prds/prd-maison-2026-05-31/prd.md#FR-1-Browse-rental-Listings`
- `_bmad-output/planning-artifacts/prds/prd-maison-2026-05-31/prd.md#FR-3-Review-Listing-details`
- `_bmad-output/planning-artifacts/prds/prd-maison-2026-05-31/prd.md#FR-5-Submit-a-valid-rental-Listing`
- `_bmad-output/planning-artifacts/prds/prd-maison-2026-05-31/prd.md#FR-6-Maintain-Listing-Availability-Status`
- `_bmad-output/planning-artifacts/architecture.md#Data-Architecture-Decisions`
- `_bmad-output/planning-artifacts/architecture.md#Authentication-and-Authorization`
- `_bmad-output/planning-artifacts/architecture.md#Implementation-Patterns-and-Consistency-Rules`
- `_bmad-output/planning-artifacts/architecture.md#Project-Structure`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/DESIGN.md#Photography-and-Trust`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/EXPERIENCE.md#Commissionnaire-Operations`
- `_bmad-output/implementation-artifacts/1-5-commissionnaire-profile-management.md`
- `https://docs.djangoproject.com/en/5.2/ref/models/fields/#imagefield`
- `https://docs.djangoproject.com/en/5.2/ref/forms/fields/#imagefield`
- `https://docs.djangoproject.com/en/5.2/topics/http/file-uploads/`
- `https://docs.djangoproject.com/en/5.2/ref/validators/#fileextensionvalidator`
- `https://pypi.org/project/Pillow/`

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- Story created from BMAD epics, PRD, architecture, UX artifacts, previous Story 1.5 context, and Django/Pillow documentation.
- No implemented Django code was present in the repository during story creation.
- 2026-06-07: Verified prerequisite Django implementation exists; `apps.accounts` and `apps.commissionnaires` tests pass (`python manage.py test apps.accounts apps.commissionnaires`, 94 tests).
- 2026-06-07: Added RED/GREEN model/admin tests for `Listing` (`python manage.py test apps.listings.tests.test_models`, 7 tests).
- 2026-06-07: Extended model/admin tests for `ListingPhoto`, deterministic ordering, primary constraints, upload path, and primary service availability (`python manage.py test apps.listings.tests.test_models`, 13 tests).
- 2026-06-07: Added RED/GREEN media validation tests for JPEG, PNG, WebP, empty, corrupt, unsupported, SVG, and oversized uploads (`python manage.py test apps.listings.tests.test_models apps.listings.tests.test_validators`, 21 tests).
- 2026-06-07: Added RED/GREEN service and selector tests for listing creation, photo upload validation, primary photo behavior, ownership scoping, and publication readiness (`python manage.py test apps.listings`, 29 tests).
- 2026-06-07: Added media configuration guard tests for local media settings, DEBUG media URL serving, and `listings/...` upload paths (`python manage.py test apps.listings`, 32 tests).
- 2026-06-07: Generated and applied `listings.0001_initial`; `python manage.py makemigrations --check --dry-run`, `python manage.py check`, and `python manage.py migrate --check` pass.
- 2026-06-07: Expanded DB-backed model tests for protected ownership, persisted timestamps, required field validation, invalid status rejection, and photo constraints (`python manage.py test apps.listings`, 36 tests).
- 2026-06-07: Final validation passed: `makemigrations --check --dry-run`, `migrate --check`, `check`, `test apps.listings` (36 tests), `test` (131 tests), and `collectstatic --noinput --dry-run`.

### Completion Notes List

- Story context generated with status `ready-for-dev`.
- Sprint status updated for Story 2.1.
- Confirmed Stories 1.1 through 1.5 foundations are implemented before Listing work: custom user/auth, Google allauth config, WhatsApp phone gate, and CommissionnaireProfile eligibility invariant.
- Implemented `Listing` with protected `CommissionnaireProfile` ownership, integer USD price storage, required rental fields, availability status choices/default, browse-supporting indexes, and admin registration.
- Implemented `ListingPhoto` with local listing media paths, deterministic ordering, unique per-listing positions, one primary photo constraint, a primary-photo fallback helper, Listing admin inline, and `set_primary_photo` service enforcement.
- Implemented strict local media validation for real JPEG, PNG, and WebP raster uploads, rejecting unsupported extensions, empty files, corrupt content, SVG, and oversized uploads before save.
- Implemented Listing services/selectors for profile-owned creation, validated photo attachment, primary photo changes, profile-scoped mutation protection, and publication readiness without public browse or submission UI scope creep.
- Confirmed existing local media configuration and DEBUG URL serving; no cloud storage, CDN, or background processing added.
- Added initial listings migration and pinned Pillow 12.2.0 while keeping Django 5.2.14 and avoiding extra platform dependencies.
- Added model, service, validation, and media configuration tests covering all AC 1-4 behavior with temporary MEDIA_ROOT cleanup for uploaded files.
- Completed required validation commands with no failures.

### Change Log

- 2026-06-07: Implemented Listing and ListingPhoto domain foundation, media validation, services/selectors, migration, dependency pin, tests, and validation checks for Story 2.1.

### File List

- `_bmad-output/implementation-artifacts/2-1-listing-domain-model-and-media-foundation.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `apps/listings/admin.py`
- `apps/listings/migrations/0001_initial.py`
- `apps/listings/models.py`
- `apps/listings/selectors.py`
- `apps/listings/services.py`
- `apps/listings/tests/test_models.py`
- `apps/listings/tests/test_media_config.py`
- `apps/listings/tests/test_services.py`
- `apps/listings/tests/test_validators.py`
- `apps/listings/validators.py`
- `requirements.txt`
