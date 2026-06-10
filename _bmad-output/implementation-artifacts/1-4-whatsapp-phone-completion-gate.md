---
baseline_commit: 83de0f8f0b1584d8b991f06922f9a3af5385d75b
---

# Story 1.4: WhatsApp Phone Completion Gate

Status: review

<!-- Validation: created from bmad-create-story workflow on 2026-06-05. -->

## Story

As a signed-in user,
I want Maison to confirm my WhatsApp phone number before phone-dependent actions,
so that leads, publication, and commissionnaire contact routes use reachable identity data.

## Acceptance Criteria

1. Given a signed-in user has no valid WhatsApp phone number, when they attempt a WhatsApp-dependent action, then Maison blocks the action server-side and routes the user to a phone completion screen, modal, or sheet with the attempted destination preserved.
2. Given the user submits a valid WhatsApp phone number, when the form is saved, then the number is stored on the user identity record and Maison returns the user to the preserved destination or a sensible account surface.
3. Given the user submits an invalid or missing phone number, when validation runs, then Maison shows a field-level error and the protected action does not proceed.
4. Given phone completion UI is rendered, when a keyboard or screen-reader user interacts with it, then labels, focus order, focus visibility, and touch targets meet the Maison accessibility floor and the copy stays concise and in French.
5. Given the implementation is inspected, when phone readiness is used by later protected actions, then it is enforced by reusable server-side helpers/decorators/mixins and not by JavaScript, hidden buttons, or template-only conditions.

## Tasks / Subtasks

- [x] Verify prerequisite auth foundation (AC: 1, 2, 5)
  - [x] Confirm Stories 1.1, 1.2, and 1.3 foundations exist before implementation.
  - [x] Confirm `CustomUser.whatsapp_phone` exists and can store a normalized international string.
  - [x] Read existing `config/settings.py`, `config/urls.py`, `apps/accounts/models.py`, `apps/accounts/forms.py`, `apps/accounts/views.py`, `apps/accounts/urls.py`, auth templates, and account tests before editing.
  - [x] Preserve email/password login, Google login, safe `next`, and existing auth tests.

- [x] Add phone normalization and validation (AC: 2, 3, 5)
  - [x] Prefer a focused dependency on `phonenumbers==9.0.32` for parsing and normalization unless the codebase already has an approved phone-number validation dependency.
  - [x] Store normalized numbers in E.164 format such as `+243...` in `CustomUser.whatsapp_phone`.
  - [x] Default parsing to Democratic Republic of the Congo region `CD` for local-format numbers while accepting explicit international `+` numbers.
  - [x] Reject blank, malformed, impossible, or invalid numbers with field-level French copy.
  - [x] Do not claim Maison can prove the number has an active WhatsApp account; this story validates phone format and stores a user-provided WhatsApp contact number.

- [x] Implement reusable phone-readiness checks (AC: 1, 5)
  - [x] Add a helper such as `user_has_whatsapp_phone(user)` that returns `True` only for authenticated users with a valid stored number.
  - [x] Add a decorator and/or class-based-view mixin such as `whatsapp_phone_required` or `WhatsAppPhoneRequiredMixin`.
  - [x] Preserve attempted destinations through the existing safe `next` pattern.
  - [x] Ensure unsafe external `next` values fall back to a safe account or public route.
  - [x] Do not add global middleware that blocks every authenticated view; only WhatsApp-dependent actions should require this gate.

- [x] Add phone completion routes and views (AC: 1, 2, 3, 4)
  - [x] Add a named route such as `accounts:phone_complete`.
  - [x] Require authentication for the phone completion view.
  - [x] On GET, show the completion form and preserve the safe destination from `next`.
  - [x] On valid POST, save the normalized phone number on the current user and redirect to the safe preserved destination or account home.
  - [x] On invalid POST, keep the form open, preserve safe entered values, and show field-level errors.
  - [x] Do not implement Lead creation, WhatsApp handoff, listing publication, or commissionnaire profile creation here.

- [x] Add phone completion form and template (AC: 2, 3, 4)
  - [x] Create or update `apps/accounts/forms.py` with a `WhatsAppPhoneCompletionForm` or equivalent.
  - [x] Use one phone field with a visible label and helper copy explaining why Maison needs the number.
  - [x] Use concise French UI copy and Maison design tokens from Story 1.1.
  - [x] Include the privacy reassurance `Maison ne lit pas vos conversations WhatsApp.` where the flow is linked to WhatsApp-dependent actions.
  - [x] Use a single primary action such as `Enregistrer le numéro`.
  - [x] Keep touch targets at least 44px and primary action at least 48px high.
  - [x] Render semantic/accessible errors near the phone field and announce form failure appropriately.

- [x] Wire the gate to at least one controlled protected action surface (AC: 1, 5)
  - [x] If a real WhatsApp-dependent route exists, protect it with the reusable gate.
  - [x] If no real route exists yet, add a minimal test-only or account-level proof route only if needed to verify the gate without inventing product behavior.
  - [x] Ensure anonymous users still go through authentication first, then phone completion when required.
  - [x] Ensure signed-in users with a valid phone continue to the attempted destination.

- [x] Preserve Google and email/password account behavior (AC: 1, 2, 5)
  - [x] Ensure users created through email/password and Google can both complete or update `whatsapp_phone`.
  - [x] Ensure Google users without phone are authenticated but not WhatsApp-ready.
  - [x] Ensure phone completion does not overwrite email, social account links, password state, or session state.
  - [x] Ensure email/password and Google login fallbacks remain available.

- [x] Add tests for phone validation and gate behavior (AC: 1, 2, 3, 5)
  - [x] Test blank phone submission returns a field-level error.
  - [x] Test malformed phone submission returns a field-level error and does not update the user.
  - [x] Test local DRC-format and `+243` numbers normalize to E.164.
  - [x] Test a valid phone saves on the authenticated user's custom user record.
  - [x] Test anonymous access to a phone-dependent route redirects to login with `next`.
  - [x] Test authenticated user without phone redirects to phone completion with preserved safe `next`.
  - [x] Test authenticated user with valid phone reaches the protected route.
  - [x] Test unsafe external `next` values are rejected or ignored.
  - [x] Test Google-created users without phone are not treated as WhatsApp-ready.

- [x] Run required checks (AC: 5)
  - [x] `python manage.py makemigrations --check --dry-run`
  - [x] `python manage.py migrate --check`
  - [x] `python manage.py check`
  - [x] `python manage.py test apps.accounts`
  - [x] `python manage.py test`
  - [x] `npm run css:build`
  - [x] `python manage.py collectstatic --noinput --dry-run`

## Dev Notes

### Source Context

- Story source: `_bmad-output/planning-artifacts/epics.md`, Epic 1, Story 1.4.
- Requirements: FR-4, NFR-3, UX-DR20, UX-DR30, UX-DR32, UX-DR34.
- Epic 1 goal: users can register, authenticate, complete WhatsApp-ready identity, and Commissionnaires can maintain the profile required to participate.
- Architecture context: every registered user must provide a WhatsApp phone number before gated marketplace actions that depend on it; Google signup may not provide a phone number, so Maison must require completion before those actions proceed.
- WhatsApp handoff context: later contact flows must be server-authoritative: authenticate user, verify WhatsApp phone availability, collect confirmation, create Lead, write audit event, then return or redirect to WhatsApp.

### Dependency On Previous Stories

This story should be implemented after Stories 1.1, 1.2, and 1.3.

Required Story 1.1 foundation:

- Native Django 5.2.14 scaffold.
- `CustomUser(AbstractUser)` with `email` and `whatsapp_phone`.
- `AUTH_USER_MODEL = "accounts.CustomUser"`.
- Tailwind CLI and base template.

Required Story 1.2 foundation:

- Email/password registration and login.
- Logout and protected account route.
- Safe `next` preservation.
- French auth templates and accessible errors.

Required Story 1.3 foundation:

- Google login through `django-allauth`.
- Google-created users use the custom user model.
- Google-created users without `whatsapp_phone` are authenticated but not WhatsApp-ready.

If prerequisites are missing, complete them first. Do not create a second user profile just to store phone numbers in this story.

### Previous Story Intelligence

- Story 1.1 recommended `whatsapp_phone = models.CharField(max_length=32, blank=True)` on `CustomUser`.
- Story 1.2 required all protected access checks to run server-side and preserve safe `next` destinations.
- Story 1.3 explicitly deferred WhatsApp phone completion to this story and warned that Google often does not provide a usable WhatsApp number.
- These stories all preserve the no-DRF, no-public-API, server-rendered Django architecture.

### Architecture Compliance

- Use Django forms for validation.
- Keep business logic out of templates.
- Use small account helpers/decorators/mixins for phone-readiness checks.
- Keep JavaScript optional and progressive only.
- Keep phone completion as an authenticated server-rendered flow. Do not create a token auth, DRF, public API, or frontend-only gate.
- Do not block anonymous browsing, email/password login, Google login, logout, or ordinary account access. Only phone-dependent actions should require `whatsapp_phone`.
- Do not implement Lead creation, WhatsApp URL generation, listing publication, commissionnaire profile management, or moderation workflows in this story.

### Phone Validation Strategy

Store a canonical string in `CustomUser.whatsapp_phone`.

Preferred implementation:

- Add `phonenumbers==9.0.32` as a focused dependency for parsing and validation.
- Parse local-format input with region `CD`.
- Accept international `+` numbers without forcing DRC only, because a user may have a WhatsApp number from another country.
- Normalize accepted values to E.164 before saving.
- Use `is_possible_number()` and `is_valid_number()` or equivalent checks.

Avoid replacing the user model field with `django-phonenumber-field` unless the project already chose that dependency during implementation. Story 1.1 established a string field, and a direct validator keeps the migration surface small.

Important product boundary:

- A formatted phone number is not proof that the number is active on WhatsApp.
- Do not call external WhatsApp APIs in this story.
- UI copy can say Maison stores the number that the user says is reachable on WhatsApp, not that Maison verified the WhatsApp account.

### Gate Design

Recommended server-side pieces:

- `apps/accounts/validators.py`: phone normalization/validation function.
- `apps/accounts/forms.py`: `WhatsAppPhoneCompletionForm`.
- `apps/accounts/selectors.py` or `apps/accounts/services.py`: `user_has_whatsapp_phone(user)` if local patterns support selectors/services.
- `apps/accounts/decorators.py`: `whatsapp_phone_required`.
- `apps/accounts/mixins.py`: `WhatsAppPhoneRequiredMixin` for class-based views if the project uses them.

Gate behavior:

- Anonymous user -> login with safe `next`.
- Authenticated user without phone -> phone completion with safe `next`.
- Authenticated user with valid phone -> requested action.
- Invalid or unsafe `next` -> fallback to account home or public browse.

Do not use one global middleware for all authenticated requests; that would over-block normal account and browse behavior.

### UX And Copy Guardrails

Suggested French copy:

- `Complétez votre numéro WhatsApp`
- `Maison utilise ce numéro pour les actions qui passent par WhatsApp.`
- `Maison ne lit pas vos conversations WhatsApp.`
- `Numéro WhatsApp`
- `Exemple : +243...`
- `Enregistrer le numéro`
- `Entrez un numéro WhatsApp valide.`
- `Ce numéro ne semble pas valide. Vérifiez l'indicatif et réessayez.`

UX requirements:

- Visible label for the phone field.
- Field-level error near the field.
- No full-page spinner.
- One primary action.
- 44px minimum touch targets.
- Visible focus.
- Error feedback available to assistive technologies.
- Concise French copy with no inflated trust or WhatsApp tracking claims.

### Security And Privacy Guardrails

- Require authentication before phone completion.
- Use CSRF protection on the POST form.
- Validate and normalize server-side even if client-side input masks are added later.
- Do not log submitted phone numbers unless there is an explicit privacy-reviewed operational need.
- Do not expose another user's phone number.
- Preserve only safe internal `next` destinations.
- Keep the submitted phone in the form after validation errors only if it is safe and useful; never leak it through URLs.
- Store the normalized number on the current authenticated user only.

### File Structure Requirements

Expected files to create or update, assuming previous stories have created the scaffold:

```text
requirements.txt
config/
└── urls.py
apps/accounts/
├── validators.py
├── forms.py
├── views.py
├── urls.py
├── decorators.py       # optional if using function-based views
├── mixins.py           # optional if using class-based views
├── services.py         # optional for saving/normalization workflow
└── tests/
    ├── test_phone_validation.py
    ├── test_phone_completion_view.py
    └── test_whatsapp_phone_gate.py
templates/
└── accounts/
    └── phone_complete.html
```

Read existing files before editing. Preserve previous stories' auth forms, routes, templates, and tests.

### Testing Requirements

Minimum tests:

- Validation:
  - blank phone rejected
  - malformed phone rejected
  - valid `+243...` number accepted and normalized
  - valid local DRC number accepted and normalized if the chosen parser supports it
  - valid non-DRC international number accepted if product chooses international WhatsApp numbers
- View behavior:
  - phone completion requires authentication
  - GET renders the form
  - valid POST saves normalized number and redirects safely
  - invalid POST preserves the form and shows field error
  - unsafe `next` does not redirect off-site
- Gate behavior:
  - anonymous user is redirected to login before phone completion
  - authenticated user without phone is redirected to phone completion
  - authenticated user with valid phone reaches the protected action
  - Google-created user without phone is not WhatsApp-ready

Use Django's built-in test runner. Do not add browser automation for this story unless implementation already has a browser-test standard.

### Latest Technical Notes

- Django 5.2 form validation runs field cleaning and `clean_<fieldname>()`; normalized field values should be returned from cleaning methods, and reusable validators should raise `ValidationError` with codes.
- Django 5.2 provides `UserPassesTestMixin` and auth decorators/mixins for server-side gates; use these patterns rather than JavaScript-only checks.
- `phonenumbers` latest PyPI release is `9.0.32` on 2026-06-05. It can parse, validate, and format international phone numbers.
- `django-phonenumber-field` wraps `phonenumbers`, but Story 1.1 established a simple `CharField`; prefer direct validation unless the implemented codebase already chose the field package.

### Anti-Patterns To Avoid

- Treating a syntactically valid number as proof of WhatsApp account ownership.
- Calling WhatsApp or external verification services in this story.
- Adding a global phone-completion middleware that blocks every authenticated route.
- Blocking anonymous public browsing.
- Storing raw, inconsistent phone formats.
- Passing phone numbers through query strings.
- Relying on input masks, template checks, or JavaScript as the only validation/gate.
- Implementing Lead creation or WhatsApp handoff early.
- Creating a separate profile model for phone completion before Story 1.5's Commissionnaire Profile.

### References

- `_bmad-output/planning-artifacts/epics.md#Story-1.4-WhatsApp-Phone-Completion-Gate`
- `_bmad-output/planning-artifacts/architecture.md#Authentication-and-Security`
- `_bmad-output/planning-artifacts/architecture.md#WhatsApp-handoff-flow`
- `_bmad-output/planning-artifacts/architecture.md#Implementation-Patterns-and-Consistency-Rules`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/EXPERIENCE.md#Access-Control`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/EXPERIENCE.md#WhatsApp-Handoff`
- `_bmad-output/implementation-artifacts/1-1-set-up-initial-project-from-starter-template.md`
- `_bmad-output/implementation-artifacts/1-2-email-and-password-account-access.md`
- `_bmad-output/implementation-artifacts/1-3-google-account-access.md`
- `https://docs.djangoproject.com/en/5.2/ref/forms/validation/`
- `https://docs.djangoproject.com/en/5.2/topics/auth/default/`
- `https://pypi.org/project/phonenumbers/`
- `https://django-phonenumber-field.readthedocs.io/en/stable/reference.html`

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- Story created from BMAD epics, architecture, UX artifacts, and previous Stories 1.1 through 1.3 context.
- No implemented Django code was present in the repository during story creation.
- 2026-06-07: Started implementation from baseline commit `83de0f8f0b1584d8b991f06922f9a3af5385d75b`; Story 1.1/1.2 prerequisites are done, Story 1.3 is in review, `CustomUser.whatsapp_phone` exists, and `python manage.py test apps.accounts` passed with 46 tests before Story 1.4 edits.
- 2026-06-07: Added red tests for phone normalization/validation, then implemented `apps.accounts.validators.normalize_whatsapp_phone`; `python manage.py test apps.accounts.tests.test_phone_validation` passed with 5 tests and `python manage.py test apps.accounts` passed with 51 tests.
- 2026-06-07: Added red tests for `user_has_whatsapp_phone`, `whatsapp_phone_required`, and `WhatsAppPhoneRequiredMixin`, then implemented server-side phone-readiness gates; `python manage.py test apps.accounts.tests.test_whatsapp_phone_gate` passed with 5 tests and `python manage.py test apps.accounts` passed with 56 tests.
- 2026-06-07: Added red tests for `accounts:phone_complete`, then implemented authenticated phone completion form/view/route/template; `python manage.py test apps.accounts.tests.test_phone_completion_view` passed with 6 tests and `python manage.py test apps.accounts` passed with 62 tests.
- 2026-06-07: Refined phone completion accessibility and field help styling; `npm run css:build` and `python manage.py test apps.accounts.tests.test_phone_completion_view` passed.
- 2026-06-07: Added red route-level tests for a minimal account proof route protected by `whatsapp_phone_required`, then implemented `accounts:phone_required_probe`; `python manage.py test apps.accounts.tests.test_whatsapp_phone_gate` passed with 8 tests and `python manage.py test apps.accounts` passed with 65 tests.
- 2026-06-07: Added completion regression tests for email/password and Google-linked users; `python manage.py test apps.accounts.tests.test_phone_completion_view apps.accounts.tests.test_social_account_flow apps.accounts.tests.test_auth_views` passed with 22 tests and `python manage.py test apps.accounts` passed with 67 tests.
- 2026-06-07: Required checks passed: `makemigrations --check --dry-run`, `migrate --check`, `check`, `test apps.accounts` with 67 tests, full `test` with 68 tests, `npm run css:build`, and `collectstatic --noinput --dry-run`.
- 2026-06-07: Final Step 9 regression suite passed after moving story and sprint status to `review`: `python manage.py test` ran 68 tests successfully.

### Completion Notes List

- Story context generated with status `ready-for-dev`.
- Sprint status updated for Story 1.4.
- Verified existing Django/allauth account foundation and preserved account regression suite before adding phone-completion behavior.
- Added `phonenumbers==9.0.32` and reusable server-side normalization for blank, malformed, local DRC, `+243`, and non-DRC international WhatsApp phone input.
- Added reusable server-side phone readiness helper, function decorator, and class-based-view mixin; `CustomUser.is_whatsapp_ready` now requires a valid stored phone number instead of a nonblank string.
- Added authenticated phone completion route and server-rendered form that preserves safe `next`, stores E.164 numbers on the current user, rejects unsafe redirects, and renders field-level errors.
- Added concise French phone-completion template copy, single primary action, privacy reassurance, stable error/help descriptions, and rebuilt compiled CSS.
- Wired the reusable phone gate to a minimal account-level proof route used for server-side coverage without adding Lead, WhatsApp handoff, listing publication, or commissionnaire behavior.
- Verified phone completion preserves email/password credentials, Google social account links, session state, and existing auth fallbacks.
- Added validation, view, gate, social-account, and regression tests covering every Story 1.4 phone-readiness acceptance path; all required checks pass.

### Change Log

- 2026-06-07: Implemented WhatsApp phone completion gate with server-side normalization, reusable readiness helper/decorator/mixin, authenticated completion flow, protected proof route, accessible French template, and regression coverage; story moved to `review`.

### File List

- `_bmad-output/implementation-artifacts/1-4-whatsapp-phone-completion-gate.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `requirements.txt`
- `apps/accounts/validators.py`
- `apps/accounts/selectors.py`
- `apps/accounts/decorators.py`
- `apps/accounts/mixins.py`
- `apps/accounts/models.py`
- `apps/accounts/forms.py`
- `apps/accounts/views.py`
- `apps/accounts/urls.py`
- `apps/accounts/tests/test_phone_validation.py`
- `apps/accounts/tests/test_whatsapp_phone_gate.py`
- `apps/accounts/tests/test_phone_completion_view.py`
- `templates/accounts/phone_complete.html`
- `static_src/css/input.css`
- `static/css/app.css`
