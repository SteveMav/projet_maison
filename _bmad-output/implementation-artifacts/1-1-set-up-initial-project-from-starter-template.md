---
baseline_commit: 83de0f8f0b1584d8b991f06922f9a3af5385d75b
---

# Story 1.1: Set up initial project from starter template

Status: done

<!-- Validation: created from bmad-create-story workflow on 2026-06-05. -->

## Story

As a product team,
I want Maison initialized as a Django 5.2 LTS application with a custom user model and Tailwind foundation,
so that all account, marketplace, and trust workflows can build on the correct base from the first migration.

## Acceptance Criteria

1. Given a fresh Maison repository, when the implementation is completed, then the project contains a native Django 5.2 LTS scaffold with `config/`, `manage.py`, SQLite settings, and the planned app structure started.
2. Given the first migrations are created, when the developer inspects the account app migrations, then a custom Django user model exists in `apps/accounts/migrations/0001_initial.py` and `AUTH_USER_MODEL` points to it before the first `migrate`.
3. Given the frontend foundation is installed, when Tailwind is built, then the project uses the official Tailwind CLI, not CDN/runtime generation.
4. Given the base CSS is inspected, when the Maison foundation is reviewed, then it includes design tokens for color, typography, spacing, radius, focus, and state primitives from the UX design contract.
5. Given a developer validates the foundation, when Django checks and the Tailwind build run, then both complete successfully.
6. Given dependency files are inspected, when this story is complete, then no React, DRF, Redis, PostgreSQL, public API, or payment dependency has been introduced.

## Tasks / Subtasks

- [x] Initialize the native Django foundation (AC: 1, 5, 6)
  - [x] Create and document a Python 3.14 virtual environment workflow.
  - [x] Add `requirements.txt` with `Django==5.2.14`.
  - [x] Create the project with `python -m django startproject config .`.
  - [x] Keep SQLite as the default database and avoid PostgreSQL-specific configuration.
  - [x] Keep the starter minimal: no DRF, React, Vue, Redis, payment, Docker, or public API dependencies.

- [x] Add the planned app structure (AC: 1, 2)
  - [x] Create the `apps` package and app packages: `core`, `accounts`, `listings`, `commissionnaires`, `leads`, `moderation`, `audit`, and `pwa`.
  - [x] Add app configs with dotted names such as `apps.accounts`.
  - [x] Add each app to `INSTALLED_APPS` only when importable and intentionally part of the scaffold.
  - [x] Create matching `tests/` packages so later stories have a stable location for tests.

- [x] Create the custom user model before the first migration (AC: 2)
  - [x] Implement `apps.accounts.models.CustomUser` based on `AbstractUser`.
  - [x] Include `email` and `whatsapp_phone` fields from the first migration; `whatsapp_phone` may be blank until Story 1.4 enforces completion.
  - [x] Set `AUTH_USER_MODEL = "accounts.CustomUser"` before running migrations.
  - [x] Register the custom user model in the Django admin using `UserAdmin`.
  - [x] Ensure future relations use `settings.AUTH_USER_MODEL` or `get_user_model()`, never direct imports from `django.contrib.auth.models.User`.

- [x] Configure settings and project entry points (AC: 1, 5)
  - [x] Set `BASE_DIR`, `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS` with deployment-sensitive values read from environment variables where practical.
  - [x] Add `templates/` as the project template directory.
  - [x] Configure `STATIC_URL`, `STATIC_ROOT`, `STATICFILES_DIRS`, `MEDIA_URL`, and `MEDIA_ROOT`.
  - [x] Keep `config/urls.py`, `config/wsgi.py`, and `config/asgi.py` in standard Django locations.
  - [x] Add development-only media serving in `config/urls.py` under `DEBUG`.

- [x] Add the Tailwind CLI foundation (AC: 3, 4, 5, 6)
  - [x] Add `package.json` and `package-lock.json` with `tailwindcss@4.3.0` and `@tailwindcss/cli@4.3.0` as dev dependencies.
  - [x] Add scripts named `css:build` and `css:watch`.
  - [x] Create `static_src/css/input.css` with `@import "tailwindcss";`.
  - [x] Compile CSS to `static/css/app.css`.
  - [x] Do not use the Tailwind CDN, Play CDN, runtime CSS generation, Vite, PostCSS, or `django-tailwind` in this story.

- [x] Encode Maison design tokens in the base CSS (AC: 4)
  - [x] Add CSS custom properties or Tailwind v4 theme tokens for surface, ink, accent, trust, warning, border, error, scrim, inverse, radius, and spacing values from `DESIGN.md`.
  - [x] Use the typography stack `"Manrope", "Segoe UI", sans-serif`; loading a web font may be deferred, but the stack must be present.
  - [x] Include focus-ring, disabled, loading, and pressed-state primitives for later components.
  - [x] Keep the token layer reusable and avoid component-specific marketplace UI beyond a minimal shell.

- [x] Add a minimal server-rendered shell (AC: 1, 4, 5)
  - [x] Create `templates/base.html` loading the compiled CSS through Django staticfiles.
  - [x] Create a minimal `core` view and URL route only if needed to smoke-test templates and static loading.
  - [x] Do not implement authentication screens, listing browse, lead handoff, moderation flows, or PWA behavior in this story.

- [x] Add foundation tests and checks (AC: 2, 5, 6)
  - [x] Add Django tests for the configured custom user model and basic project importability.
  - [x] Add a smoke test for the base template or core route if one is created.
  - [x] Run `python manage.py makemigrations --check --dry-run` after committing generated migrations to verify there are no pending model changes.
  - [x] Run `python manage.py migrate --check`.
  - [x] Run `python manage.py check`.
  - [x] Run `python manage.py test`.
  - [x] Run `npm run css:build`.
  - [x] Run `python manage.py collectstatic --noinput --dry-run`.

- [x] Document local setup (AC: 1, 3, 5)
  - [x] Update `README.md` with Windows PowerShell setup commands, Django checks, tests, Tailwind build/watch, and collectstatic validation.
  - [x] Add `.env.example` with deployment-sensitive setting names but no real secrets.

### Review Findings

- [x] [Review][Patch] Deployment settings fail open when environment variables are missing [config/settings.py:15]
- [x] [Review][Patch] Fresh setup docs say to create the SQLite schema but only run `migrate --check` [README.md:15]
- [x] [Review][Patch] Local uploaded media is not ignored even though `MEDIA_ROOT` is inside the repo [.gitignore:1]
- [x] [Review][Patch] Python 3.14 is documented but not enforced or verified by project metadata [README.md:7]
- [x] [Review][Patch] Story deliverables remain untracked in Git, so a normal branch/PR diff would omit them [git status]

## Dev Notes

### Source Context

- Story source: `_bmad-output/planning-artifacts/epics.md`, Epic 1, Story 1.1.
- PRD context: Maison is a Kinshasa rental marketplace that keeps browsing fast, uses WhatsApp as a measured handoff boundary, and avoids overpromising trust signals.
- Architecture context: native Django scaffold is selected; Cookiecutter Django and `django-tailwind` are intentionally rejected or deferred for this MVP foundation.
- UX context: Story 1.1 must establish the visual token foundation used by later marketplace, commissionnaire, and moderation surfaces.
- Persistent facts: no `project-context.md` file exists in this repository at story creation time.
- Previous story intelligence: none. This is the first implementation story.
- Git intelligence: the repository currently has only the initial import commit (`83de0f8 chore: initial project import`) and no existing Django code to preserve.

### Architecture Compliance

- Use Python `3.14.x`, Django `5.2.14 LTS`, SQLite, server-rendered Django templates, Tailwind CSS `4.3.0`, and the official `@tailwindcss/cli`.
- Django 5.2 LTS is intentionally pinned even though newer Django docs exist. Do not upgrade to Django 6.x inside this story.
- Start from `python -m django startproject config .`; do not introduce Cookiecutter Django.
- Do not introduce Django REST Framework, a public `/api/` namespace, React, Vue, SPA routing, Redis, PostgreSQL, payments, Docker, or external object storage.
- Keep JavaScript modular and under static assets. Story 1.1 may create the directory structure, but should not add business JavaScript behavior.
- Keep business logic out of templates. Later stories should use forms, selectors, and service functions.
- All future state-changing endpoints must enforce server-side auth, permissions, and CSRF. This story should not create state-changing product endpoints.

### File Structure Requirements

Create or preserve this structure as the implementation foundation:

```text
maison/
├── manage.py
├── requirements.txt
├── package.json
├── package-lock.json
├── .env.example
├── README.md
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── core/
│   ├── accounts/
│   ├── listings/
│   ├── commissionnaires/
│   ├── leads/
│   ├── moderation/
│   ├── audit/
│   └── pwa/
├── templates/
│   ├── base.html
│   └── includes/
├── static_src/
│   ├── css/input.css
│   └── js/
├── static/
│   ├── css/app.css
│   ├── js/
│   ├── icons/
│   └── images/
├── media/
└── docs/
```

The architecture names future app responsibilities as follows:

- `core`: shared validators, constants, and generic utilities only.
- `accounts`: user identity, auth gates, and WhatsApp phone completion.
- `listings`: discovery, listing detail, photos, filters, and availability.
- `commissionnaires`: professional profile, publication dashboard, and inventory ownership.
- `leads`: Lead creation, WhatsApp handoff, and lead status.
- `moderation`: reports, listing review, and verification.
- `audit`: append-only business events.
- `pwa`: manifest, service worker, and push subscriptions.

### Custom User Guardrails

- The custom user model is not optional. It must exist before the first `migrate` because changing `AUTH_USER_MODEL` later creates migration and foreign-key complexity.
- Use `CustomUser(AbstractUser)` for a conservative Django-compatible start.
- Include at minimum:
  - `email = models.EmailField(...)`
  - `whatsapp_phone = models.CharField(max_length=32, blank=True)`
- Prefer `email` uniqueness now if Story 1.2 will support email/password account access directly.
- Do not implement the full phone completion gate in this story; Story 1.4 owns validation and gating behavior.
- Do not implement Google auth behavior in this story; Story 1.3 owns `django-allauth` setup. If the implementation chooses to pin `django-allauth` early, use the architecture-verified version `65.18.0` and do not add Google UX or provider credentials yet.

### Tailwind And Design Token Guardrails

- Tailwind input file should import Tailwind using `@import "tailwindcss";`.
- Build command should compile from `static_src/css/input.css` to `static/css/app.css`.
- The base CSS must include Maison token primitives:
  - surfaces: `#F7F4EE`, `#FEFDF9`, `#EEE8DC`, `#E3DCCF`
  - ink: `#1D2A25`, `#64706A`, `#89928E`
  - accent: `#276A52`, `#1E5642`, `#DCEDE4`
  - trust: `#EEFDF5`, `#B5EFD4`
  - warm cue: `#C77742`
  - warning/error: `#F8E7D8`, `#B8473D`, `#FBE2DE`
  - borders: `#DED8CC`, `#C8C0B3`
  - scrim: `rgba(29, 42, 37, 0.40)` or hex equivalent
  - inverse: `#26332E`, `#E5F4EC`
  - radius: `10px`, `16px`, `24px`, `9999px`
  - spacing baseline: `4px`, then `8px`, `12px`, `16px`, `24px`, `32px`, `40px`, `64px`
- Primary button primitives should be at least `48px` high, use deep green, include visible focus, and support disabled/loading/pressed states.
- Avoid broad component implementation. This story creates primitives; later stories create listing cards, drawers, filters, reports, and operational rows.

### Settings And Deployment Guardrails

- Use Django staticfiles and `collectstatic`.
- Configure `STATIC_ROOT`; do not confuse it with checked-in source assets.
- Use `MEDIA_ROOT` and `MEDIA_URL` for local media. Uploaded file validation arrives in listing/media stories, but the scaffold must not serve uploads as executable content.
- Public deployment remains open between PythonAnywhere and VPS. Do not hardcode either target.
- Use environment variables for deployment-sensitive settings such as `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, database settings later, Google OAuth credentials later, push keys later, and email settings later.
- Localhost is acceptable for local PWA development, but public service worker and push behavior later require HTTPS.

### Testing Requirements

Minimum story verification commands:

```powershell
python manage.py makemigrations --check --dry-run
python manage.py migrate --check
python manage.py check
python manage.py test
npm run css:build
python manage.py collectstatic --noinput --dry-run
```

Expected tests:

- `apps.accounts.tests` verifies `settings.AUTH_USER_MODEL == "accounts.CustomUser"` and `get_user_model()` resolves the custom model.
- A user creation test verifies the model can save `email` and optional `whatsapp_phone`.
- If a `core` route is added, a test verifies it returns HTTP 200 and uses the base template.
- Tests should use Django's built-in test runner; do not add pytest unless a later architecture update approves it.

### Latest Technical Notes

- Django 5.2 custom user docs require `AUTH_USER_MODEL` before migrations and note the model must be created in the first migration of its app.
- Django 5.2 staticfiles deployment docs define the `collectstatic` plus `STATIC_ROOT` production flow.
- Tailwind CLI docs use `tailwindcss` plus `@tailwindcss/cli`, an input CSS file with `@import "tailwindcss";`, and a CLI command from input to output CSS.
- django-allauth docs require `allauth.account.middleware.AccountMiddleware`, auth backends, installed apps, and `allauth.urls` when Story 1.3 introduces Google/social login.

### Anti-Patterns To Avoid

- Creating the Django project inside a nested subfolder instead of at repository root.
- Running `migrate` before the custom user model and `AUTH_USER_MODEL` are in place.
- Using direct references to `django.contrib.auth.models.User`.
- Adding Tailwind via CDN or browser runtime generation.
- Introducing a frontend framework or API framework because the scaffold feels sparse.
- Building product features that belong to later stories.
- Hardcoding real secrets, OAuth credentials, phone numbers, or deployment-only values.

### References

- `_bmad-output/planning-artifacts/epics.md#Story-1.1-Set-up-initial-project-from-starter-template`
- `_bmad-output/planning-artifacts/architecture.md#Selected-Starter-Native-Django-5.2-LTS-Scaffold`
- `_bmad-output/planning-artifacts/architecture.md#Custom-Django-User-from-the-start`
- `_bmad-output/planning-artifacts/architecture.md#Project-Structure-and-Boundaries`
- `_bmad-output/planning-artifacts/architecture.md#Implementation-Patterns-and-Consistency-Rules`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/DESIGN.md`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/EXPERIENCE.md`
- `https://docs.djangoproject.com/en/5.2/topics/auth/customizing/#substituting-a-custom-user-model`
- `https://docs.djangoproject.com/en/5.2/howto/static-files/deployment/`
- `https://tailwindcss.com/docs/installation/tailwind-cli`
- `https://docs.allauth.org/en/latest/installation/quickstart.html`

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- Story created from BMAD epics and architecture artifacts.
- No previous implementation story existed.
- 2026-06-06: Started implementation from baseline commit `83de0f8f0b1584d8b991f06922f9a3af5385d75b`.
- 2026-06-06: Generated `apps/accounts/migrations/0001_initial.py` with Django 5.2.14 before running migrations.
- 2026-06-06: Validation passed: `makemigrations --check --dry-run`, `migrate --check`, `check`, `test`, `npm run css:build`, and `collectstatic --noinput --dry-run`.

### Completion Notes List

- Implemented native Django 5.2.14 scaffold at repository root with `config/`, `manage.py`, SQLite settings, templates, static/media configuration, and environment-driven deployment-sensitive settings.
- Added planned app packages, app configs, migrations/test packages, and `accounts.CustomUser(AbstractUser)` with unique email and optional `whatsapp_phone` in the first accounts migration.
- Added Tailwind v4 CLI scripts, locked npm dependencies, Maison design tokens, compiled `static/css/app.css`, and a minimal server-rendered public shell.
- Added README and `.env.example` for Windows PowerShell setup, Django checks, Tailwind build/watch, and collectstatic validation.
- Confirmed no React, DRF, Redis, PostgreSQL, public API, payment, Vite, PostCSS, `django-tailwind`, or CDN Tailwind dependency was introduced.

### Change Log

- 2026-06-06: Implemented Story 1.1 foundation and moved status to `review`.

### File List

- `.env.example`
- `.gitignore`
- `README.md`
- `requirements.txt`
- `package.json`
- `package-lock.json`
- `manage.py`
- `config/__init__.py`
- `config/asgi.py`
- `config/settings.py`
- `config/urls.py`
- `config/wsgi.py`
- `apps/__init__.py`
- `apps/accounts/__init__.py`
- `apps/accounts/admin.py`
- `apps/accounts/apps.py`
- `apps/accounts/migrations/__init__.py`
- `apps/accounts/migrations/0001_initial.py`
- `apps/accounts/models.py`
- `apps/accounts/tests/__init__.py`
- `apps/accounts/tests/test_custom_user.py`
- `apps/audit/__init__.py`
- `apps/audit/apps.py`
- `apps/audit/migrations/__init__.py`
- `apps/audit/tests/__init__.py`
- `apps/commissionnaires/__init__.py`
- `apps/commissionnaires/apps.py`
- `apps/commissionnaires/migrations/__init__.py`
- `apps/commissionnaires/tests/__init__.py`
- `apps/core/__init__.py`
- `apps/core/apps.py`
- `apps/core/migrations/__init__.py`
- `apps/core/tests/__init__.py`
- `apps/core/tests/test_core.py`
- `apps/core/urls.py`
- `apps/core/views.py`
- `apps/leads/__init__.py`
- `apps/leads/apps.py`
- `apps/leads/migrations/__init__.py`
- `apps/leads/tests/__init__.py`
- `apps/listings/__init__.py`
- `apps/listings/apps.py`
- `apps/listings/migrations/__init__.py`
- `apps/listings/tests/__init__.py`
- `apps/moderation/__init__.py`
- `apps/moderation/apps.py`
- `apps/moderation/migrations/__init__.py`
- `apps/moderation/tests/__init__.py`
- `apps/pwa/__init__.py`
- `apps/pwa/apps.py`
- `apps/pwa/migrations/__init__.py`
- `apps/pwa/tests/__init__.py`
- `templates/base.html`
- `templates/core/home.html`
- `static_src/css/input.css`
- `static/css/app.css`
- `_bmad-output/implementation-artifacts/1-1-set-up-initial-project-from-starter-template.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
