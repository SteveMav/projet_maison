---
baseline_commit: 83de0f8f0b1584d8b991f06922f9a3af5385d75b
---

# Story 1.3: Google Account Access

Status: review

<!-- Validation: created from bmad-create-story workflow on 2026-06-05. -->

## Story

As a user,
I want to sign in with Google,
so that I can enter Maison quickly without creating a separate password first.

## Acceptance Criteria

1. Given the authentication foundation exists, when Google authentication is configured, then Maison uses `django-allauth` for Google login and the implementation remains session-based Django authentication.
2. Given an anonymous visitor chooses Google sign-in, when Google returns a valid authenticated identity, then Maison creates or links the local user account and the user is returned to the intended destination when one was preserved.
3. Given Google does not provide a usable WhatsApp phone number, when the signed-in user attempts a gated marketplace action that requires WhatsApp readiness, then Maison routes them to phone completion before the action proceeds and no protected action relies on client-side checks alone.
4. Given Google authentication fails or is cancelled, when the user returns to Maison, then Maison shows a recoverable French error state and the user can choose email/password access instead.
5. Given the implementation is inspected, when dependencies, settings, and templates are reviewed, then Google credentials are not hardcoded and no DRF, public API, React, Redis, PostgreSQL, payments, token auth, or custom OAuth flow has been introduced.

## Tasks / Subtasks

- [x] Verify prerequisite auth foundation (AC: 1, 2, 3, 4)
  - [x] Confirm Story 1.1 outputs exist: Django scaffold, `CustomUser`, `AUTH_USER_MODEL`, Tailwind/base template.
  - [x] Confirm Story 1.2 outputs exist: email/password registration and login, logout, protected-route redirect with safe `next`, and auth templates.
  - [x] Read existing `config/settings.py`, `config/urls.py`, `apps/accounts/urls.py`, `apps/accounts/views.py`, `apps/accounts/forms.py`, and auth templates before editing.
  - [x] Preserve working email/password behavior and tests from Story 1.2.

- [x] Install and configure `django-allauth` for Google social login (AC: 1, 5)
  - [x] Add `django-allauth[socialaccount]==65.18.0` to `requirements.txt` unless already pinned.
  - [x] Add required installed apps: `django.contrib.sites`, `allauth`, `allauth.account`, `allauth.socialaccount`, and `allauth.socialaccount.providers.google`.
  - [x] Set `SITE_ID = 1` unless the project uses a different explicit Sites strategy.
  - [x] Add `allauth.account.middleware.AccountMiddleware` after Django auth/message middleware as required by allauth.
  - [x] Add `allauth.account.auth_backends.AuthenticationBackend` while preserving `django.contrib.auth.backends.ModelBackend`.
  - [x] Run migrations for allauth tables.

- [x] Configure Google provider securely (AC: 1, 2, 5)
  - [x] Configure Google OAuth credentials through Django admin `SocialApp` records or environment-backed settings, not hardcoded values.
  - [x] Document required environment variables or admin setup in `README.md` and `.env.example` using placeholder names only.
  - [x] Request only the practical minimum Google scopes: profile and email.
  - [x] Enable PKCE in `SOCIALACCOUNT_PROVIDERS["google"]` unless implementation evidence shows allauth already enforces the needed protection.
  - [x] Do not request offline access or store Google refresh tokens unless a later story requires background Google API access.

- [x] Reconcile account URLs without breaking Story 1.2 (AC: 1, 2, 4)
  - [x] Include `allauth.urls` in `config/urls.py` under a deliberate prefix.
  - [x] Avoid route shadowing between local `apps.accounts.urls` and allauth account/social URLs.
  - [x] Preserve existing named routes used by email/password login, logout, register, and tests.
  - [x] Ensure Google callback URLs are predictable for local setup documentation.
  - [x] Preserve safe `next` destination behavior after Google login and failed/cancelled attempts.

- [x] Adapt templates for a unified sign-in choice (AC: 2, 4)
  - [x] Add a Google sign-in action to the existing login/register or auth-gate UI.
  - [x] Use allauth template tags, provider URLs, or allauth-provided views rather than hand-building OAuth URLs.
  - [x] Keep UI copy concise and in French.
  - [x] Keep email/password as an available fallback on the same auth surface or a clear adjacent path.
  - [x] Keep controls accessible: visible labels or accessible names, visible focus, keyboard reachability, 44px touch targets, and semantic error feedback.

- [x] Handle social-account user creation and linking (AC: 2, 3, 5)
  - [x] Ensure allauth creates local users using Maison's custom user model.
  - [x] Define how Google email maps to the local email field and how duplicate local emails are handled.
  - [x] Link a Google social account to an existing local account only when the email is verified by Google and the implementation deliberately enables that behavior for Google.
  - [x] Do not silently create duplicate local users with the same email.
  - [x] Keep `whatsapp_phone` blank when Google does not provide a usable phone; Story 1.4 owns completion and validation.

- [x] Preserve WhatsApp phone completion boundary (AC: 3)
  - [x] Add or preserve a server-side helper/property to detect whether a signed-in user is WhatsApp-ready.
  - [x] For any existing protected route that requires WhatsApp readiness, route missing-phone users to the future phone-completion path or a temporary explicit placeholder only if Story 1.4 is not implemented yet.
  - [x] Do not allow JavaScript-only checks to bypass phone readiness.
  - [x] Do not implement the full phone completion form in this story.

- [x] Add recoverable failure and cancellation behavior (AC: 4)
  - [x] Configure templates/messages for social login cancellation and provider errors.
  - [x] Show French recovery copy and a clear route back to email/password login.
  - [x] Avoid exposing OAuth internals, provider payloads, tokens, stack traces, or sensitive diagnostics.
  - [x] Ensure failed Google auth leaves the user unauthenticated unless a prior valid session already existed.

- [x] Add tests for Google auth configuration and regressions (AC: 1, 2, 3, 4, 5)
  - [x] Test allauth apps, middleware, auth backends, and Google provider are configured.
  - [x] Test login/register templates render a Google sign-in action while preserving email/password actions.
  - [x] Test existing email/password registration and login tests still pass.
  - [x] Test protected-route `next` preservation still works after allauth URL integration.
  - [x] Test duplicate-email handling or document the chosen allauth setting and test it at adapter/config level.
  - [x] Test missing `whatsapp_phone` after social signup does not mark the user WhatsApp-ready.
  - [x] Test failure/cancel routes render recoverable French messaging where practical without live Google network calls.

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

- Story source: `_bmad-output/planning-artifacts/epics.md`, Epic 1, Story 1.3.
- Requirements: FR-4, NFR-3, UX-DR30, UX-DR34.
- Epic 1 goal: users can register, authenticate, complete WhatsApp-ready identity, and Commissionnaires can maintain the profile required to participate.
- Architecture context: Maison uses email/password and Google auth through `django-allauth`, session-based Django authentication, a custom Django user model, CSRF-protected forms, and server-side permission checks.
- UX context: access-required states preserve attempted destinations, avoid exposing operational data, and use concise French copy.

### Dependency On Previous Stories

This story should not be implemented before Stories 1.1 and 1.2 are working.

Required Story 1.1 foundation:

- Native Django 5.2.14 scaffold at repository root.
- `CustomUser(AbstractUser)` from first migration with `email` and `whatsapp_phone`.
- `AUTH_USER_MODEL = "accounts.CustomUser"`.
- Tailwind CLI foundation and `templates/base.html`.

Required Story 1.2 foundation:

- Email/password registration and login using the custom user model.
- Logout and a protected account surface.
- Safe `next` preservation for unauthenticated protected routes.
- French field-level errors and accessible auth templates.

If prerequisites are missing, complete them first. Do not create a parallel auth system or custom OAuth flow to compensate.

### Previous Story Intelligence

- Story 1.1 warned that Google auth belongs here and should use the architecture-verified `django-allauth` version `65.18.0`.
- Story 1.2 explicitly forbids adding Google behavior before this story and requires email/password behavior to remain session-based.
- Story 1.2 may have local `/accounts/` routes. Before including `allauth.urls`, inspect and prevent route shadowing or name collisions.
- Story 1.2 requires safe `next` handling. Google login must keep that invariant.

### Architecture Compliance

- Use `django-allauth`; do not hand-roll OAuth2, use `social-auth-app-django`, DRF social auth, token auth, or headless allauth APIs.
- Keep the app server-rendered with Django templates. JavaScript may progressively enhance the auth gate, but cannot be the only auth path.
- Keep Django sessions as the authentication mechanism.
- Keep `ModelBackend` so Django admin and existing email/password login continue to work.
- Add allauth's auth backend for allauth account/social behavior.
- Keep secrets out of source. Google OAuth client ID and secret must come from Django admin `SocialApp` setup or environment-backed settings.
- Do not introduce PostgreSQL, Redis, DRF, React, payments, or a public API.

### URL And Routing Guardrails

Allauth commonly expects a route set that includes provider login and callback paths. Choose one route strategy and document it:

- Preferred if compatible with Story 1.2: mount allauth under `/accounts/` and adjust local account routes to avoid path conflicts.
- Acceptable if local `/accounts/` routes must remain untouched: mount allauth under a distinct internal prefix and ensure provider callback URLs in Google Console match that prefix.

Whatever strategy is chosen:

- Existing email/password named routes must keep working or have deliberate compatibility redirects.
- Google login must return to the preserved `next` when safe.
- External or unsafe `next` values must not redirect off-site.
- The README must document the local callback URL for Google OAuth setup.

### Social Account Linking Guardrails

The most sensitive decision in this story is duplicate-email handling.

- If enabling `SOCIALACCOUNT_PROVIDERS["google"]["EMAIL_AUTHENTICATION"] = True`, do so only for Google because Google verified email can be treated as trusted for this product decision.
- If enabling automatic linking, set and test the explicit auto-connect behavior. Do not rely on accidental defaults.
- If not enabling automatic linking, show a recoverable conflict path that tells the user to sign in with email/password first or use the existing account flow.
- Do not create two active local users with the same normalized email.
- Do not overwrite existing `whatsapp_phone` or local account fields from Google payloads unless the mapping is explicit and tested.

### WhatsApp Phone Boundary

Google often does not provide a usable WhatsApp phone number. This story should preserve the product boundary:

- Social login can authenticate the user.
- Missing `whatsapp_phone` does not block all browsing.
- Missing `whatsapp_phone` must block WhatsApp-dependent gated actions server-side once those routes exist.
- Story 1.4 owns the actual phone completion UI, validation, and return path.

If Story 1.4 is not implemented, use a clearly named route placeholder or helper only where tests require a target. Do not build the full phone flow early.

### UX And Copy Guardrails

- Suggested French copy:
  - `Continuer avec Google`
  - `Ou connectez-vous avec votre adresse e-mail`
  - `La connexion Google a été annulée. Vous pouvez réessayer ou utiliser votre adresse e-mail.`
  - `Nous n'avons pas pu terminer la connexion Google. Réessayez ou utilisez votre adresse e-mail.`
  - `Complétez votre numéro WhatsApp pour continuer.`
- Do not imply Google provides a WhatsApp number.
- Do not imply Maison reads WhatsApp conversations.
- Keep auth actions calm and practical; no urgency or inflated trust claims.
- Use the Maison design tokens and accessibility floor from Stories 1.1 and 1.2.

### Security And Privacy Guardrails

- Never hardcode Google client secrets, OAuth callback URLs with secrets, social tokens, or test credentials.
- Never log OAuth provider payloads, access tokens, refresh tokens, ID tokens, authorization codes, session IDs, or cookies.
- Prefer online access. Do not request offline access or store refresh tokens unless a later story needs Google API calls in the background.
- Keep OAuth provider settings minimal: profile and email scopes are enough for sign-in.
- Use allauth's provider URL/template tags instead of manually constructing Google OAuth URLs.
- Keep CSRF and allauth's POST-based social-login initiation behavior unless there is a deliberate, documented reason to change it.

### File Structure Requirements

Expected files to create or update, assuming previous stories have created the scaffold:

```text
requirements.txt
.env.example
README.md
config/
├── settings.py
└── urls.py
apps/accounts/
├── adapters.py          # optional, only if duplicate-email or redirect behavior needs customization
├── views.py
├── urls.py
└── tests/
    ├── test_google_auth_config.py
    ├── test_social_account_flow.py
    └── test_auth_regressions.py
templates/
├── accounts/
│   ├── login.html
│   ├── register.html
│   └── socialaccount/
│       ├── login_cancelled.html
│       └── authentication_error.html
└── socialaccount/
    └── snippets/
        └── provider_list.html   # optional if shared allauth templates are customized
```

Read existing files before editing. Preserve working `apps.accounts` forms, views, routes, and tests.

### Testing Requirements

Minimum tests:

- Configuration:
  - allauth apps are installed
  - Google provider app is installed
  - allauth middleware is present
  - both auth backends are present
  - `SITE_ID` is configured
- UI:
  - login/register surface includes a Google sign-in action
  - email/password fallback remains visible
  - cancellation/error templates render recoverable French copy
- Auth behavior:
  - existing Story 1.2 email/password tests still pass
  - safe `next` is preserved through the login path
  - unsafe external `next` is rejected or falls back to a safe route
  - duplicate social email behavior is explicit and tested at adapter/config level
  - Google-created users use the custom user model
  - Google-created users without `whatsapp_phone` are not marked WhatsApp-ready

Do not write tests that require live Google network calls. Use allauth test helpers, Django test client, factories, adapter unit tests, or mocked provider responses.

### Latest Technical Notes

- `django-allauth` latest docs list `65.18.0` as a release dated 2026-05-29; keep the architecture-pinned version unless a later architecture update changes it.
- Current allauth quickstart requires `django.template.context_processors.request`, `ModelBackend`, `allauth.account.auth_backends.AuthenticationBackend`, `allauth`, `allauth.account`, `allauth.socialaccount`, provider apps, `AccountMiddleware`, and `include("allauth.urls")`.
- The Google provider is OAuth2-based and requires Google Console OAuth client credentials plus callback URLs such as `/accounts/google/login/callback/`, depending on the chosen mount prefix.
- Google provider settings can request `profile` and `email`, set `AUTH_PARAMS.access_type = "online"`, and enable `OAUTH_PKCE_ENABLED`.
- allauth recommends POST-based social login initiation by default for security; avoid changing `SOCIALACCOUNT_LOGIN_ON_GET` unless justified.

### Anti-Patterns To Avoid

- Hand-building Google OAuth URLs or writing a custom OAuth callback view.
- Replacing email/password auth with Google-only auth.
- Breaking Story 1.2 routes, templates, or tests.
- Creating duplicate users for the same normalized email.
- Treating Google login as WhatsApp phone completion.
- Hardcoding Google OAuth credentials.
- Requesting broad Google scopes, offline access, or storing refresh tokens without need.
- Introducing DRF, token auth, public API routes, React, Redis, PostgreSQL, or payments.

### References

- `_bmad-output/planning-artifacts/epics.md#Story-1.3-Google-Account-Access`
- `_bmad-output/planning-artifacts/architecture.md#Authentication-and-Security`
- `_bmad-output/planning-artifacts/architecture.md#Implementation-Patterns-and-Consistency-Rules`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/EXPERIENCE.md#Access-Control`
- `_bmad-output/implementation-artifacts/1-1-set-up-initial-project-from-starter-template.md`
- `_bmad-output/implementation-artifacts/1-2-email-and-password-account-access.md`
- `https://docs.allauth.org/en/latest/installation/quickstart.html`
- `https://docs.allauth.org/en/latest/socialaccount/providers/google.html`
- `https://docs.allauth.org/en/latest/socialaccount/configuration.html`
- `https://docs.djangoproject.com/en/5.2/topics/auth/default/`

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- Story created from BMAD epics, architecture, UX artifacts, and previous Stories 1.1 and 1.2 context.
- No implemented Django code was present in the repository during story creation.

### Completion Notes List

- Story context generated with status `ready-for-dev`.
- Sprint status updated for Story 1.3.
- Verified Story 1.1/1.2 auth foundation before Google changes; `python manage.py test apps.accounts` passed with 21 tests.
- Configured django-allauth 65.18.0 with Sites, Google provider, middleware, auth backends, email-only allauth settings, and preserved local registration login with explicit `ModelBackend`; `python manage.py migrate` and `python manage.py test` passed.
- Configured Google provider with environment-backed credentials, minimal `profile`/`email` scopes, online access, PKCE, and placeholder-only setup docs; `python manage.py test` passed with 30 tests.
- Mounted allauth routes under `/accounts/` after local account routes, preserving `accounts:*` names and safe `next` behavior while exposing `/accounts/google/login/callback/`; `python manage.py test` passed with 33 tests.
- Added unified Google sign-in action to login/register using allauth's `google_login` provider view with POST, preserved email/password fallback, rebuilt CSS, and verified with `python manage.py test` passing 35 tests.
- Enabled Google-only verified email authentication with auto-connect, verified duplicate-email linking behavior, custom-user social signup shape, and blank `whatsapp_phone`; `python manage.py test` passed with 39 tests.
- Added server-side `CustomUser.is_whatsapp_ready` helper and tests for blank/nonblank WhatsApp state without implementing the Story 1.4 completion form; `python manage.py test` passed with 41 tests.
- Added Maison-styled allauth cancellation/error templates with French recovery copy and email/password fallback, avoiding sensitive OAuth internals; `python manage.py test` passed with 43 tests.
- Completed Google auth configuration, UI, routing, social flow, WhatsApp-boundary, and recovery regression coverage; `python manage.py test --timing` passed with 43 tests.
- Required final checks passed: `makemigrations --check --dry-run`, `migrate --check`, `check`, `test apps.accounts`, `test`, `npm run css:build`, and `collectstatic --noinput --dry-run`.
- Final Step 9 regression suite passed: `python manage.py test` ran 43 tests successfully before status moved to `review`.
- Post-cleanup regression suite passed: `python manage.py test` ran 43 tests successfully after removing dummy secret material from the social flow fixture.
- Browser verification passed on `http://127.0.0.1:8000`: desktop login/register, mobile login, cancellation, and error pages showed expected Google/email recovery UI without horizontal overflow.
- Added Maison-owned Google start route so clicking Google sign-in recovers to email/password login when OAuth credentials are missing, ignored placeholder Google env values, and added a Google mark to the sign-in button; `.venv\Scripts\python.exe manage.py test` passed with 46 tests.
- Verified the updated login button in Browser: Google mark visible, 48px button height, no horizontal overflow; verified real HTTP POST with CSRF returns to login with recovery messaging when Google is not configured.
- Added local `.env` loading in Django settings without a new dependency so configured Google credentials are available to allauth; verified one Google app is loaded without exposing secrets, real CSRF POST redirects to `accounts.google.com/o/oauth2/v2/auth`, Browser visual check passes, and `.venv\Scripts\python.exe manage.py test` passed with 47 tests.

### File List

- `_bmad-output/implementation-artifacts/1-3-google-account-access.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `apps/accounts/tests/test_google_auth_config.py`
- `apps/accounts/tests/test_auth_regressions.py`
- `apps/accounts/tests/test_social_account_flow.py`
- `apps/accounts/tests/test_custom_user.py`
- `apps/accounts/urls.py`
- `apps/accounts/models.py`
- `apps/accounts/views.py`
- `config/urls.py`
- `config/settings.py`
- `.env.example`
- `README.md`
- `requirements.txt`
- `templates/accounts/includes/google_signin.html`
- `templates/accounts/login.html`
- `templates/accounts/register.html`
- `templates/socialaccount/authentication_error.html`
- `templates/socialaccount/login_cancelled.html`
- `static_src/css/input.css`
- `static/css/app.css`

### Change Log

- 2026-06-06: Implemented Google account access with django-allauth configuration, secure Google provider settings, `/accounts/` allauth routing, unified auth UI, verified-email social linking, WhatsApp readiness boundary, recoverable failure templates, and regression coverage; story moved to `review`.
- 2026-06-06: Hardened Google sign-in button click behavior for missing credentials and added the Google mark to the auth UI.
- 2026-06-06: Enabled local `.env` loading for Google OAuth credentials and verified live Google redirect from the local login button.
