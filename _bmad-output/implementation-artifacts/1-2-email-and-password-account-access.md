---
baseline_commit: 83de0f8f0b1584d8b991f06922f9a3af5385d75b
---

# Story 1.2: Email And Password Account Access

Status: done

<!-- Validation: created from bmad-create-story workflow on 2026-06-05. -->

## Story

As a user,
I want to create an account and sign in with email and password,
so that Maison can protect gated marketplace actions while keeping public browsing open.

## Acceptance Criteria

1. Given an anonymous visitor, when they open public browse surfaces, then they can browse public Listing Cards without signing in and protected account, commissionnaire, and moderator destinations remain inaccessible.
2. Given an anonymous visitor chooses to register, when they submit valid email, password, and required profile fields, then Maison creates a user account using the custom user model and the user can sign in with email and password.
3. Given a user submits invalid registration or login information, when the form is processed, then Maison shows field-level errors without losing safe entered values and the error copy is concise French UI copy.
4. Given a signed-in user, when they try to access account-protected surfaces, then server-side permission checks allow only valid destinations and unauthenticated access attempts preserve the intended destination for later return.
5. Given the authentication implementation is inspected, when dependencies and routes are reviewed, then Maison remains session-based and does not introduce DRF, a public API, React, Redis, PostgreSQL, payments, or Google social login behavior in this story.

## Tasks / Subtasks

- [x] Verify Story 1.1 foundation before implementation (AC: 1, 2, 4, 5)
  - [x] Confirm `manage.py`, `config/settings.py`, `templates/base.html`, `static/css/app.css`, and the `apps/accounts` package exist.
  - [x] Confirm `settings.AUTH_USER_MODEL == "accounts.CustomUser"` and the custom user exists in the first accounts migration.
  - [x] Confirm `CustomUser` has usable `email` and `whatsapp_phone` fields; do not proceed with direct `django.contrib.auth.models.User` usage.
  - [x] If Story 1.1 has not been implemented, implement or block on it before coding this story.

- [x] Configure session-based account routes (AC: 2, 4, 5)
  - [x] Add `apps/accounts/urls.py` with named routes for `register`, `login`, `logout`, and a minimal protected account landing page if needed for smoke tests.
  - [x] Include `accounts.urls` from `config/urls.py` under a stable path such as `/accounts/`.
  - [x] Set `LOGIN_URL`, `LOGIN_REDIRECT_URL`, and `LOGOUT_REDIRECT_URL` to named routes or stable internal paths.
  - [x] Preserve the standard `next` redirect parameter for unauthenticated access attempts.

- [x] Implement registration with the custom user model (AC: 2, 3)
  - [x] Create `apps/accounts/forms.py`.
  - [x] Implement a custom registration form bound to `get_user_model()` or `CustomUser`, not the default `User`.
  - [x] Collect email and password fields required for email/password access.
  - [x] Include any currently required identity fields from the custom user model, but do not require WhatsApp completion here if Story 1.4 owns that gate.
  - [x] Use Django password validation and save hashed passwords through Django's user creation APIs or `set_password()`.
  - [x] Normalize email consistently before uniqueness checks and save.
  - [x] Prevent duplicate usable email registration with a field-level error.

- [x] Implement login and logout (AC: 2, 3, 4, 5)
  - [x] Use Django's session authentication flow through `LoginView`/`LogoutView` or equivalent Django auth helpers.
  - [x] Support email/password login. If `USERNAME_FIELD` remains `username`, add a small authentication backend or form logic deliberately; do not accidentally require a hidden username.
  - [x] Redirect authenticated users to the preserved `next` destination only when it is safe.
  - [x] Keep logout server-side and redirect to a public surface without exposing prior session data.

- [x] Protect account-only destinations server-side (AC: 1, 4)
  - [x] Use `login_required`, `LoginRequiredMixin`, or explicit server-side checks on protected account views.
  - [x] Add a minimal protected account view only if needed until later account/profile surfaces exist.
  - [x] Do not rely on JavaScript, hidden UI controls, or template-only checks for access control.
  - [x] Do not expose commissionnaire, Lead, moderation, or private listing data in unauthenticated responses.

- [x] Build accessible French auth templates (AC: 2, 3, 4)
  - [x] Add `templates/accounts/register.html`, `templates/accounts/login.html`, and any shared includes under lowercase paths.
  - [x] Extend `templates/base.html` and use Maison design tokens from Story 1.1.
  - [x] Use concise French UI copy, visible labels, visible focus states, and at least 44px touch targets.
  - [x] Render field-level errors near the relevant controls and keep safe entered values such as email after validation failures.
  - [x] Avoid exposing raw exception messages or internal validation details.

- [x] Prepare the gated-auth pattern without overbuilding product flows (AC: 1, 4)
  - [x] Ensure protected redirects preserve the attempted destination with `next`.
  - [x] Add a reusable template include or context shape that later stories can use for a quick auth modal/sheet.
  - [x] If JavaScript is added, keep it in `static_src/js/auth-gate.js`, use `data-*` hooks, and treat it as progressive enhancement only.
  - [x] Do not implement Google login, WhatsApp phone completion, commissionnaire profile creation, listing detail gating, or moderation permission workflows in this story.

- [x] Add tests for authentication and access boundaries (AC: 1, 2, 3, 4, 5)
  - [x] Test registration creates `settings.AUTH_USER_MODEL` users with hashed passwords.
  - [x] Test duplicate email registration returns a field-level error and does not create a second user.
  - [x] Test invalid login displays a French recoverable error without authenticating.
  - [x] Test successful login establishes a session and honors a safe `next` destination.
  - [x] Test unauthenticated access to a protected account view redirects to login with `next`.
  - [x] Test authenticated access to the protected account view succeeds.
  - [x] Test public routes remain accessible to anonymous visitors.

- [x] Run required checks (AC: 5)
  - [x] `python manage.py makemigrations --check --dry-run`
  - [x] `python manage.py migrate --check`
  - [x] `python manage.py check`
  - [x] `python manage.py test apps.accounts`
  - [x] `python manage.py test`
  - [x] `npm run css:build`
  - [x] `python manage.py collectstatic --noinput --dry-run`

### Review Findings

- [x] [Review][Patch] Email normalization is inconsistent between registration, manager creation, and login [apps/accounts/models.py:12]
- [x] [Review][Patch] Password validation does not receive the submitted user, so email-similarity checks are skipped [apps/accounts/forms.py:94]
- [x] [Review][Patch] Duplicate registration can race past the form check and return a 500 instead of a field error [apps/accounts/forms.py:80]
- [x] [Review][Patch] Invalid login renders as a non-field error despite the field-level error requirement [templates/accounts/includes/auth_form_errors.html:1]
- [x] [Review][Patch] Authenticated users can submit registration and silently switch to a new account [apps/accounts/views.py:13]
- [x] [Review][Patch] Protected `next` flow is lost on invalid registration POST and when switching from login to register [apps/accounts/views.py:27]
- [x] [Review][Patch] Gated-auth modal/sheet reuse point is marked complete but no include, context shape, or `auth-gate.js` exists [_bmad-output/implementation-artifacts/1-2-email-and-password-account-access.md:69]
- [x] [Review][Patch] Unsafe registration `next` handling lacks regression coverage [apps/accounts/tests/test_auth_views.py:23]
- [x] [Review][Patch] Story deliverables remain untracked in Git, so a normal branch/PR diff would omit them [git status]
- [x] [Review][Defer] Login has no brute-force throttling or audit hook [apps/accounts/views.py:38] - deferred, outside Story 1.2 acceptance criteria

## Dev Notes

### Source Context

- Story source: `_bmad-output/planning-artifacts/epics.md`, Epic 1, Story 1.2.
- Requirements: FR-4, NFR-3, UX-DR30, UX-DR32, UX-DR34.
- Epic 1 goal: users can register, authenticate, complete WhatsApp-ready identity, and Commissionnaires can maintain the profile required to participate.
- PRD context: anonymous public browsing remains open, but full detail/contact, commissionnaire, and moderator operations are protected.
- Architecture context: Maison uses Django server-rendered templates, server-side sessions, CSRF-protected POST forms, a custom user model, and no public API in the MVP.

### Dependency On Story 1.1

Story 1.2 should be implemented after the Story 1.1 foundation exists. Required foundation outputs:

- Native Django project at repository root.
- `apps/accounts` installed with `CustomUser(AbstractUser)`.
- `AUTH_USER_MODEL = "accounts.CustomUser"` set before the first migration.
- Base templates and static CSS from Tailwind CLI.
- No React, DRF, Redis, PostgreSQL, public API, or payment dependency.

If any of these are missing, stop and complete Story 1.1 first. Do not work around a missing custom user model by using Django's default `User`.

### Previous Story Intelligence

Story 1.1 established the intended foundation rather than implemented code in this workflow run. Its guidance that directly affects this story:

- Use Python `3.14.x`, Django `5.2.14 LTS`, SQLite, server-rendered templates, Tailwind CSS `4.3.0`, and official `@tailwindcss/cli`.
- Use `CustomUser(AbstractUser)` and include `email` and `whatsapp_phone` from the first migration.
- Prefer email uniqueness for email/password account access.
- Keep JavaScript modular and progressive under static assets.
- Use Django forms for validation and keep business logic out of templates.
- Tests should use Django's built-in test runner.

### Architecture Compliance

- Implement standard Django session authentication; do not introduce token auth or an API login endpoint.
- All POST forms must use CSRF protection.
- Protected views must enforce access on the server with Django auth decorators, mixins, or explicit checks.
- Public browsing stays anonymous. In this story, use the current public shell or a minimal public route as the anonymous-access proof until listing browse exists in Epic 2.
- Commissionnaire and moderator authorization are not fully implemented here. This story should establish the auth boundary and reusable patterns; role-specific rules belong to Stories 1.5 and 4.1.
- Google authentication belongs to Story 1.3. Do not add provider credentials, social login templates, or allauth URL behavior here unless Story 1.1 already pinned the package and it remains dormant.

### File Structure Requirements

Expected files to create or update, assuming Story 1.1 has created the scaffold:

```text
apps/accounts/
├── forms.py
├── views.py
├── urls.py
└── tests/
    ├── test_auth_forms.py
    ├── test_auth_views.py
    └── test_access_boundaries.py
templates/
└── accounts/
    ├── login.html
    ├── register.html
    └── includes/
        └── auth_form_errors.html
static_src/
└── js/
    └── auth-gate.js        # optional progressive enhancement only
config/
├── settings.py
└── urls.py
```

Read existing files before editing if Story 1.1 has already created them. Preserve any working custom user, admin, Tailwind, and base-template setup.

### Auth Form Guardrails

- Use `get_user_model()` for form/query logic unless importing `CustomUser` is clearer inside `apps.accounts`.
- If extending Django `UserCreationForm`, set `Meta.model` to the custom user model and explicit fields. Do not rely on the default `User` binding.
- If implementing a custom `forms.Form`, call Django password validators and create users through the custom model manager or `set_password()`.
- Do not store raw passwords, log credentials, or include submitted passwords in validation errors.
- Authentication should accept the user's email plus password. If the user model still uses `username` internally, deliberately map email to the authenticated user; avoid requiring a separate username in the UI.
- Keep WhatsApp phone optional here unless Story 1.1 made it required at the database level. Story 1.4 owns the completion gate before WhatsApp-dependent actions.

### UX And Copy Guardrails

- Use concise French UI copy and avoid generic dead-end errors.
- Suggested labels and messages:
  - `Adresse e-mail`
  - `Mot de passe`
  - `Créer un compte`
  - `Se connecter`
  - `Nous n'avons pas pu vous connecter. Vérifiez l'adresse e-mail et le mot de passe.`
  - `Un compte existe déjà avec cette adresse e-mail.`
  - `Connectez-vous pour continuer.`
- Preserve safe entered values after form errors, especially email. Never re-render password values.
- Authentication required states must preserve the attempted destination and avoid exposing operational data.
- Permission denied states must explain lack of access without revealing another user's private data.
- Meet the accessibility floor: visible labels, visible focus, keyboard reachability, live-region or semantic error feedback, and 44px touch targets.

### Security And Privacy Guardrails

- Keep authentication state in Django sessions.
- Use Django's password hashing and validation. Never compare plaintext passwords manually.
- Sanitize and validate `next` redirects with Django-safe redirect helpers or equivalent checks.
- Keep session cookies and CSRF middleware enabled.
- Do not leak whether a specific email exists during login beyond normal field-level registration errors.
- Avoid logs containing email/password payloads or session identifiers.
- Do not expose private commissionnaire, Lead, moderation, or full listing data to anonymous users.

### Testing Requirements

Minimum tests for this story:

- Registration:
  - valid registration creates a custom user
  - password is hashed and usable through Django auth
  - duplicate email is rejected
  - invalid passwords return form errors
- Login/logout:
  - valid email/password login creates an authenticated session
  - invalid login stays unauthenticated with a recoverable French error
  - logout clears authentication and redirects to a public route
- Access boundaries:
  - anonymous public route returns 200
  - anonymous protected route redirects to login with `next`
  - authenticated protected route returns 200
  - unsafe external `next` does not redirect off-site

Use Django's built-in test runner. Do not add pytest, Selenium, Playwright, DRF test clients, or frontend test tooling in this story.

### Latest Technical Notes

- Django 5.2 authentication uses sessions and middleware to expose `request.user`; use `login()`/`logout()` or Django auth views rather than custom session manipulation.
- Django's `login_required` and `LoginRequiredMixin` preserve the attempted destination in the default `next` query parameter.
- Django password validation is controlled by `AUTH_PASSWORD_VALIDATORS`; validators are used by forms and management commands, not automatically at the model level.
- Django custom-user docs state that forms tied to the built-in `User`, including `UserCreationForm`, must be rewritten or extended with the custom user model.

### Anti-Patterns To Avoid

- Creating a second user model or switching back to Django's default `User`.
- Requiring a username in the UI when the product requirement is email/password access.
- Adding Google auth before Story 1.3.
- Adding WhatsApp completion enforcement before Story 1.4.
- Using template-only access checks or JavaScript-only auth gates.
- Redirecting blindly to arbitrary external `next` URLs.
- Returning JSON auth endpoints or a public API for normal login/register.
- Adding broad dashboard, listing, commissionnaire, or moderation features outside this story.

### References

- `_bmad-output/planning-artifacts/epics.md#Story-1.2-Email-And-Password-Account-Access`
- `_bmad-output/planning-artifacts/architecture.md#Authentication-and-Security`
- `_bmad-output/planning-artifacts/architecture.md#Implementation-Patterns-and-Consistency-Rules`
- `_bmad-output/planning-artifacts/architecture.md#Project-Structure-and-Boundaries`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/EXPERIENCE.md#Access-Control`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/EXPERIENCE.md#Voice-And-Tone`
- `_bmad-output/implementation-artifacts/1-1-set-up-initial-project-from-starter-template.md`
- `https://docs.djangoproject.com/en/5.2/topics/auth/default/`
- `https://docs.djangoproject.com/en/5.2/topics/auth/passwords/`
- `https://docs.djangoproject.com/en/5.2/topics/auth/customizing/`

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- Story created from BMAD epics, architecture, UX artifacts, and previous Story 1.1 context.
- No implemented Django code was present in the repository during story creation.
- 2026-06-06: Started implementation after Story 1.1 foundation was implemented in the same workflow run.
- 2026-06-06: Validation passed: `python manage.py test apps.accounts`, full `python manage.py test`, `migrate --check`, `check`, `npm run css:build`, and `collectstatic --noinput --dry-run`.

### Completion Notes List

- Implemented session-based registration, login, logout, and protected account dashboard routes under `/accounts/`.
- Registration uses the custom user model through `get_user_model()`, normalizes unique email, validates passwords, hashes credentials, logs users in, and preserves safe `next` destinations.
- Login uses Django `LoginView` with an email-labeled authentication form, safe `next` handling, concise French error copy, and no API/token/social-login behavior.
- Added accessible French auth templates with visible labels, preserved safe email values after errors, CSRF-protected POST forms, and server-side access enforcement.
- Added tests for registration, duplicate email rejection, invalid password handling, login/logout, safe and unsafe redirects, public access, and protected account boundaries.

### Change Log

- 2026-06-06: Implemented Story 1.2 account access and moved status to `review`.

### File List

- `config/settings.py`
- `config/urls.py`
- `apps/accounts/forms.py`
- `apps/accounts/urls.py`
- `apps/accounts/views.py`
- `apps/accounts/tests/test_access_boundaries.py`
- `apps/accounts/tests/test_auth_forms.py`
- `apps/accounts/tests/test_auth_views.py`
- `apps/accounts/tests/test_custom_user.py`
- `templates/base.html`
- `templates/accounts/dashboard.html`
- `templates/accounts/includes/auth_form_errors.html`
- `templates/accounts/login.html`
- `templates/accounts/register.html`
- `templates/core/home.html`
- `static_src/css/input.css`
- `static/css/app.css`
- `_bmad-output/implementation-artifacts/1-2-email-and-password-account-access.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
