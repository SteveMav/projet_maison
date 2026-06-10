---
baseline_commit: 83de0f8f0b1584d8b991f06922f9a3af5385d75b
---

# Story 1.5: Commissionnaire Profile Management

Status: review

<!-- Validation: created from bmad-create-story workflow on 2026-06-05. -->

## Story

As a Commissionnaire,
I want to create and update my Commissionnaire Profile,
so that Maison can attribute Listings and Leads to a reachable professional identity.

## Acceptance Criteria

1. Given a signed-in user with a valid WhatsApp phone number, when they create a Commissionnaire Profile with a display name and reachable WhatsApp phone number, then Maison stores the profile and links it to exactly one user identity and the profile becomes eligible for future Listing publication.
2. Given a Commissionnaire updates their profile information, when valid changes are saved, then existing Listings and Leads remain associated with the same Commissionnaire Profile and the updated profile identity is shown on future relevant surfaces.
3. Given a user attempts to create or edit a profile with missing required fields, when the form is submitted, then Maison shows field-level errors and no incomplete Commissionnaire Profile becomes eligible for publication.
4. Given a signed-in user tries to access another Commissionnaire's profile management surface, when the request is processed, then Maison denies access server-side and does not expose private profile, Listing, or Lead data.
5. Given the profile management UI is displayed, when it appears on mobile and desktop, then it uses compact French copy, visible labels, 44px touch targets, and the Maison design tokens established in Story 1.1.

## Tasks / Subtasks

- [x] Verify prerequisite account foundation (AC: 1, 2, 4)
  - [x] Confirm Stories 1.1 through 1.4 are implemented before coding this story.
  - [x] Confirm custom user, email/password login, Google login, and WhatsApp phone completion all work.
  - [x] Confirm phone normalization helper from Story 1.4 can be reused for the profile phone field.
  - [x] Read existing `apps/accounts`, `apps/commissionnaires`, `config/urls.py`, base templates, and auth tests before editing.

- [x] Model the Commissionnaire Profile (AC: 1, 2, 3, 4)
  - [x] Create `apps/commissionnaires/models.py` with `CommissionnaireProfile`.
  - [x] Link profile to the user through `OneToOneField(settings.AUTH_USER_MODEL, related_name="commissionnaire_profile", on_delete=models.CASCADE)`.
  - [x] Add required `display_name` and normalized `whatsapp_phone` fields.
  - [x] Add `created_at` and `updated_at` timestamps.
  - [x] Add an eligibility helper/property such as `is_publication_eligible` that is true only when required fields are valid.
  - [x] Add database constraints needed to preserve exactly one profile per user.
  - [x] Register the model in Django admin with safe list/search fields.

- [x] Implement profile creation and update workflow (AC: 1, 2, 3)
  - [x] Add `apps/commissionnaires/forms.py` with a `CommissionnaireProfileForm`.
  - [x] Validate `display_name` as required and non-blank after trimming.
  - [x] Validate and normalize `whatsapp_phone` using the same phone rules as Story 1.4.
  - [x] Initialize the profile phone from `request.user.whatsapp_phone` when available.
  - [x] Save updates on the existing profile instance; never delete/recreate a profile during edits.
  - [x] Ensure incomplete form submissions do not create an eligible profile.

- [x] Add server-side access controls (AC: 1, 4)
  - [x] Require authentication for all commissionnaire profile management routes.
  - [x] Require WhatsApp phone completion before profile creation or update, using the Story 1.4 gate.
  - [x] Ensure a user can create or edit only their own profile.
  - [x] Deny direct access to another user's profile management route without revealing whether the target profile, Listings, or Leads exist.
  - [x] Keep future commissionnaire dashboard/publication routes out of this story unless a minimal route is needed for navigation.

- [x] Add commissionnaire routes and views (AC: 1, 2, 3, 4)
  - [x] Add `apps/commissionnaires/urls.py`.
  - [x] Include commissionnaire URLs from `config/urls.py` under a stable prefix such as `/pro/`.
  - [x] Add named routes for profile view, create, and edit, or use one combined create/update route if simpler.
  - [x] Redirect users without a profile to creation when they enter the pro surface.
  - [x] Redirect users with a profile to the profile detail/edit surface.
  - [x] Preserve safe attempted destinations where this story intersects auth or phone gates.

- [x] Build compact French profile UI (AC: 3, 5)
  - [x] Add templates under `templates/commissionnaires/`.
  - [x] Use concise French labels and helper copy.
  - [x] Use Maison design tokens, compact rows, hairline dividers, visible focus, and at least 44px touch targets.
  - [x] Avoid oversized hero metrics, nested cards, decorative dashboards, or product surfaces that belong to later stories.
  - [x] Show field-level errors near `display_name` and `whatsapp_phone`.
  - [x] Explain permission-denied states without exposing another Commissionnaire's data.

- [x] Preserve future Listing and Lead attribution invariants (AC: 1, 2, 4)
  - [x] Document that future `Listing` and `Lead` models must reference `CommissionnaireProfile`, not copy the current user or display name as the source of truth.
  - [x] Ensure profile update changes `display_name` and `whatsapp_phone` on the same profile row so future Listings/Leads keep their foreign-key association.
  - [x] Do not create Listing, Lead, Report, moderation, or audit event models in this story.
  - [x] Do not add public Commissionnaire profile pages unless explicitly required by later stories.

- [x] Add tests for model, forms, views, and permissions (AC: 1, 2, 3, 4)
  - [x] Test one profile can be created for one user.
  - [x] Test duplicate profile creation for the same user is blocked.
  - [x] Test required display name and phone validation.
  - [x] Test phone normalization on the profile.
  - [x] Test valid profile creation marks the profile publication-eligible.
  - [x] Test invalid form submissions do not create an eligible profile.
  - [x] Test updating a profile preserves the same primary key.
  - [x] Test a user cannot access another user's profile edit route.
  - [x] Test unauthenticated access redirects to login with `next`.
  - [x] Test authenticated user without WhatsApp phone is routed through phone completion before profile management.

- [x] Run required checks (AC: 1, 2, 3, 4, 5)
  - [x] `python manage.py makemigrations --check --dry-run`
  - [x] `python manage.py migrate --check`
  - [x] `python manage.py check`
  - [x] `python manage.py test apps.commissionnaires`
  - [x] `python manage.py test`
  - [x] `npm run css:build`
  - [x] `python manage.py collectstatic --noinput --dry-run`

## Dev Notes

### Source Context

- Story source: `_bmad-output/planning-artifacts/epics.md`, Epic 1, Story 1.5.
- Requirements: FR-4, NFR-3, UX-DR24, UX-DR26, UX-DR30, UX-DR32.
- FR-4 requires the minimum Commissionnaire Profile needed to publish Listings: display name, reachable WhatsApp phone number, exactly one associated user identity, and updates that do not lose existing Listings or Leads.
- Architecture boundary: `commissionnaires` owns professional profile, publication dashboard, and own inventory. This story should implement the profile foundation only.
- UX boundary: operational surfaces should be compact, use hairline dividers, avoid oversized dashboard cards, and communicate access denial without exposing private data.

### Dependency On Previous Stories

This story should be implemented after Stories 1.1 through 1.4.

Required Story 1.1 foundation:

- Native Django 5.2.14 scaffold.
- Apps package including `apps/commissionnaires`.
- Tailwind CLI and base template.

Required Story 1.2 foundation:

- Email/password authentication.
- Safe `next` preservation.
- Server-side protected route patterns.

Required Story 1.3 foundation:

- Google authentication through `django-allauth`.
- Social users use the custom user model.

Required Story 1.4 foundation:

- `CustomUser.whatsapp_phone` normalization and completion flow.
- Server-side WhatsApp phone gate helpers/decorators/mixins.

If prerequisites are missing, complete them first. Do not bypass the WhatsApp phone gate or create a second phone validation system.

### Previous Story Intelligence

- Story 1.4 established that a syntactically valid phone number is not proof of WhatsApp account ownership. Reuse that product boundary here.
- Story 1.4 preferred `phonenumbers==9.0.32` and E.164 storage. Commissionnaire profile phone should follow the same canonical format.
- Story 1.2 and 1.3 require auth routes and `next` handling to remain safe. Commissionnaire profile gates must preserve those invariants.
- Story 1.1 established no DRF, no public API, no React, no Redis, no PostgreSQL, and no payments.

### Architecture Compliance

- Use Django models, ModelForms, views, and templates.
- Keep business logic out of templates.
- Use services/selectors only where they clarify workflow or ownership checks.
- Keep all state-changing forms CSRF-protected.
- Use server-side permission checks before loading or showing profile data.
- Do not introduce a public `/api/` namespace or internal JSON endpoints for profile CRUD unless a later story proves a progressive enhancement need.
- Do not create Listing, Lead, Report, audit, or moderation models in this story. This story provides the stable profile FK target for later work.

### Model Design Guardrails

Recommended model:

```python
class CommissionnaireProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="commissionnaire_profile",
    )
    display_name = models.CharField(max_length=120)
    whatsapp_phone = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

Notes:

- `OneToOneField` enforces exactly one profile per user at the database level.
- Future `Listing` and `Lead` records should use `ForeignKey(CommissionnaireProfile, ...)` so profile updates do not break attribution.
- Prefer updating the same profile row rather than delete/recreate. A changed display name or phone should not invalidate future or existing references.
- If the project adds status fields later, use lowercase `snake_case` values. Do not add status states in this story unless needed for eligibility.
- `on_delete=models.CASCADE` is acceptable for user-owned profile cleanup at this stage, but future Listings/Leads should be protected or otherwise designed so business history is not accidentally erased.

### Phone And Eligibility Guardrails

- The profile phone is a professional contact number. Initialize it from the user's completed `whatsapp_phone`, but allow it to be edited if valid and normalized.
- Store profile `whatsapp_phone` in E.164.
- A profile is eligible for future Listing publication only when:
  - it belongs to an authenticated user
  - the owning user is WhatsApp-ready
  - `display_name` is present after trimming
  - profile `whatsapp_phone` is present and valid
- Do not infer eligibility from template state. Use a model property, selector, or service that tests persisted data.
- Do not claim Maison has verified the offline professional identity. This story creates the minimum reachable professional profile.

### Access Control Guardrails

- Commissionnaire profile management is private to the owning user.
- A signed-in user cannot create a profile for another user.
- A signed-in user cannot edit another user's profile.
- Permission denied should avoid confirming whether another user's profile exists.
- Anonymous users should authenticate first.
- Authenticated users without WhatsApp phone should complete Story 1.4's phone gate before profile management.
- Do not expose future operational data such as Listings, Leads, Reports, moderation states, or audit history in this story.

### UX And Copy Guardrails

Suggested French copy:

- `Espace pro`
- `Profil commissionnaire`
- `Nom affiché`
- `Numéro WhatsApp professionnel`
- `Ce nom apparaîtra sur vos futures annonces.`
- `Maison utilise ce numéro pour les contacts liés à vos annonces.`
- `Enregistrer le profil`
- `Mettez à jour votre profil`
- `Vous n'avez pas accès à ce profil.`
- `Complétez votre numéro WhatsApp pour continuer.`

UI requirements:

- Compact form layout, not a marketing page.
- Visible labels and field-level errors.
- 44px minimum touch targets.
- Primary action uses the deep green Maison action token.
- Use compact rows and hairline dividers for any profile summary.
- Avoid nested dashboard cards, oversized metrics, and decorative hero sections.
- Use no trust copy implying Maison guarantees the Commissionnaire or offline outcomes.

### File Structure Requirements

Expected files to create or update, assuming previous stories have created the scaffold:

```text
apps/commissionnaires/
├── admin.py
├── models.py
├── forms.py
├── views.py
├── urls.py
├── selectors.py       # optional for ownership/eligibility reads
├── services.py        # optional for create/update workflow
└── tests/
    ├── test_models.py
    ├── test_forms.py
    ├── test_views.py
    └── test_permissions.py
templates/
└── commissionnaires/
    ├── profile_detail.html
    ├── profile_form.html
    └── permission_denied.html
config/
└── urls.py
```

Read existing files before editing. Preserve account auth, phone gate, and Google auth behavior.

### Testing Requirements

Minimum tests:

- Model:
  - one profile per user
  - required display name
  - required normalized phone
  - `is_publication_eligible` returns expected values
  - `updated_at` changes on profile update if practical to test
- Forms:
  - valid data creates/updates profile
  - display name trims whitespace
  - phone normalizes using Story 1.4 helper
  - invalid phone shows a field-level error
- Views:
  - anonymous user redirects to login with `next`
  - authenticated user without WhatsApp phone redirects to phone completion
  - authenticated WhatsApp-ready user can create a profile
  - profile owner can update their profile
  - update preserves the same profile primary key
  - non-owner cannot access edit route or private data

Use Django's built-in test runner. Do not add frontend or browser automation unless the implemented codebase has already established that test layer.

### Latest Technical Notes

- Django 5.2 `OneToOneField` is the standard way to model a one-to-one relationship and gives reverse access from the user to the profile.
- Django 5.2 `ModelForm` maps model fields into forms and supports editing an existing model instance by passing `instance=profile`.
- Django 5.2 auth decorators and mixins should enforce authentication and permission boundaries server-side.
- Reuse Story 1.4 phone validation rather than adding `django-phonenumber-field` unless the implementation already adopted it.

### Anti-Patterns To Avoid

- Creating more than one Commissionnaire Profile for a user.
- Recreating the profile row during edits and breaking future foreign-key attribution.
- Letting users create or edit profiles for other users.
- Treating profile creation as verified identity or a trust badge.
- Building Listing publication or inventory dashboards inside this story.
- Exposing private Listings, Leads, moderation notes, or Report information.
- Relying on template-only checks or JavaScript-only redirects for profile access.
- Creating a public API or DRF endpoints for profile CRUD.

### References

- `_bmad-output/planning-artifacts/epics.md#Story-1.5-Commissionnaire-Profile-Management`
- `_bmad-output/planning-artifacts/architecture.md#Commissionnaire-access`
- `_bmad-output/planning-artifacts/architecture.md#Project-Structure-and-Boundaries`
- `_bmad-output/planning-artifacts/architecture.md#Implementation-Patterns-and-Consistency-Rules`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/EXPERIENCE.md#Commissionnaire-Operations`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/EXPERIENCE.md#Access-Control`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/DESIGN.md#Commissionnaire-Operations`
- `_bmad-output/implementation-artifacts/1-1-set-up-initial-project-from-starter-template.md`
- `_bmad-output/implementation-artifacts/1-2-email-and-password-account-access.md`
- `_bmad-output/implementation-artifacts/1-3-google-account-access.md`
- `_bmad-output/implementation-artifacts/1-4-whatsapp-phone-completion-gate.md`
- `https://docs.djangoproject.com/en/5.2/topics/db/examples/one_to_one/`
- `https://docs.djangoproject.com/en/5.2/topics/forms/modelforms/`
- `https://docs.djangoproject.com/en/5.2/topics/auth/default/`

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- Story created from BMAD epics, architecture, UX artifacts, and previous Stories 1.1 through 1.4 context.
- No implemented Django code was present in the repository during story creation.
- Verified account prerequisites with `python manage.py test apps.accounts` (67 tests passing).
- Confirmed `CommissionnaireProfile` model/admin behavior with `python manage.py test apps.commissionnaires.tests.test_models` (7 tests passing) and full suite `python manage.py test` (75 tests passing).
- Confirmed `CommissionnaireProfileForm` behavior with `python manage.py test apps.commissionnaires.tests.test_forms` (5 tests passing) and full suite `python manage.py test` (80 tests passing).
- Confirmed commissionnaire profile permissions with `python manage.py test apps.commissionnaires.tests.test_permissions` (5 tests passing) and full suite `python manage.py test` (85 tests passing).
- Confirmed commissionnaire profile route/view behavior with `python manage.py test apps.commissionnaires.tests.test_views` (8 tests passing) and full suite `python manage.py test` (93 tests passing).
- Confirmed compact profile UI copy/rendering with `python manage.py test apps.commissionnaires.tests.test_views` (9 tests passing), `npm run css:build`, and full suite `python manage.py test` (94 tests passing).
- Confirmed attribution invariant documentation with `python manage.py test apps.commissionnaires` (26 tests passing), `python manage.py check`, and full suite `python manage.py test` (94 tests passing).
- Confirmed complete model/form/view/permission coverage with `python manage.py test apps.commissionnaires` (27 tests passing) and full suite `python manage.py test` (95 tests passing).
- Required Story 1.5 checks passed: `makemigrations --check --dry-run`, `migrate --check` after applying local `commissionnaires.0001_initial`, `check`, `test apps.commissionnaires`, full `test`, `npm run css:build`, and `collectstatic --noinput --dry-run`.
- Verified `/pro/profile/new/` and profile detail in the in-app Browser at desktop and mobile widths: compact French labels rendered, controls measured 48px high, profile phone normalized, and no horizontal overflow detected.

### Implementation Plan

- Reuse `apps.accounts.validators.normalize_whatsapp_phone` and `WhatsAppPhoneRequiredMixin` for profile phone validation and access gating.
- Implement profile foundation with Django model, ModelForm, class-based views, server-rendered templates, and focused Django tests.

### Completion Notes List

- Story context generated with status `ready-for-dev`.
- Sprint status updated for Story 1.5.
- Confirmed Stories 1.1 through 1.4 account foundations are available before Story 1.5 implementation.
- Added the Commissionnaire Profile model with one-to-one user ownership, normalized WhatsApp storage, publication eligibility, timestamps, admin registration, and migration.
- Added `CommissionnaireProfileForm` with trimmed display names, reused WhatsApp normalization, initial profile phone from the user, and update-in-place saves.
- Added private `/pro/` profile routes guarded by authentication, WhatsApp completion, and owner-only profile lookup.
- Added `/pro/` entry, profile create, detail, and edit views with redirects based on whether the signed-in user already has a profile.
- Added compact French profile templates and pro-surface CSS using Maison tokens, hairline profile rows, and existing 48px action controls.
- Documented `CommissionnaireProfile` as the stable future Listing/Lead attribution target and did not add Listing, Lead, Report, moderation, audit, or public profile models/pages.
- Added explicit blank WhatsApp phone form coverage and aligned required-field copy with Story 1.4.
- Ran all required Story 1.5 validation commands successfully.
- Browser-verified the profile creation form and detail surface on local Django runserver, then removed the temporary visual test user.

### File List

- `_bmad-output/implementation-artifacts/1-5-commissionnaire-profile-management.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `apps/commissionnaires/admin.py`
- `apps/commissionnaires/forms.py`
- `apps/commissionnaires/migrations/0001_initial.py`
- `apps/commissionnaires/models.py`
- `apps/commissionnaires/tests/test_permissions.py`
- `apps/commissionnaires/tests/test_views.py`
- `apps/commissionnaires/urls.py`
- `apps/commissionnaires/views.py`
- `config/urls.py`
- `static/css/app.css`
- `static_src/css/input.css`
- `apps/commissionnaires/tests/test_forms.py`
- `apps/commissionnaires/tests/test_models.py`
- `templates/commissionnaires/permission_denied.html`
- `templates/commissionnaires/profile_detail.html`
- `templates/commissionnaires/profile_form.html`

### Change Log

- 2026-06-07: Implemented Story 1.5 Commissionnaire Profile Management and moved story to review.
