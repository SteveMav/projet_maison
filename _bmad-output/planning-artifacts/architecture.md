---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
inputDocuments:
  - "PRODUCT.md"
  - "_bmad-output/brainstorming/brainstorming-session-2026-05-30-144517.md"
  - "_bmad-output/planning-artifacts/briefs/brief-maison-2026-05-31/brief.md"
  - "_bmad-output/planning-artifacts/prds/prd-maison-2026-05-31/prd.md"
  - "_bmad-output/planning-artifacts/prds/prd-maison-2026-05-31/addendum.md"
  - "_bmad-output/planning-artifacts/prds/prd-maison-2026-05-31/reconcile-brainstorming.md"
  - "_bmad-output/planning-artifacts/prds/prd-maison-2026-05-31/review-rubric.md"
  - "_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/DESIGN.md"
  - "_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/EXPERIENCE.md"
  - "_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/reconcile-design-folder.md"
  - "_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/imports/design/README.md"
  - "_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/imports/design/STITCH-REVIEW.md"
  - "_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/imports/design/index.html"
  - "_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/imports/design/styles.css"
  - "_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/imports/design/app.js"
  - "_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/imports/design/stitch-imports/detail-ngaliema/screen.html"
  - "_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/imports/design/stitch-imports/detail-ngaliema/screen.png"
  - "_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/imports/design/stitch-imports/detail-ngaliema/property-01.jpg"
  - "_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/imports/design/stitch-imports/detail-ngaliema/property-02.jpg"
  - "_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/imports/design/stitch-imports/detail-ngaliema/property-03.jpg"
  - "_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/imports/design/stitch-imports/detail-ngaliema/property-04.jpg"
workflowType: 'architecture'
lastStep: 8
status: 'complete'
completedAt: '2026-06-03'
project_name: 'maison'
user_name: 'steve'
date: '2026-06-02'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**

Maison is a rental-first marketplace for Kinshasa with 14 functional requirements organized into five architectural areas:

1. **Rental inventory discovery (FR-1 to FR-3):**
   Public browsing, recency ordering, filters by Commune, budget and bedroom count, fast-scan listing cards, and detailed listing surfaces.

2. **Commissionnaire publication and availability (FR-4 to FR-6):**
   Commissionnaire profiles, mobile-friendly listing submission, media uploads, moderation states, and explicit availability updates.

3. **Traceable WhatsApp lead handoff (FR-7 to FR-10):**
   Lightweight tenant identification with consent, Lead persistence before external redirection, WhatsApp deep links with listing context, and commissionnaire Lead visibility.

4. **Moderation, selective verification and reporting (FR-11 to FR-13):**
   Moderator queues, correction and removal actions, operational Verification Checklist, reversible badges, Reports, and audit history.

5. **Basic trust signals (FR-14):**
   Listing freshness, selective verification, and an optional public view count without overstating credibility.

**Non-Functional Requirements:**

- Mobile-first responsive web experience on current mobile browsers.
- PWA installation support for Android and iOS.
- Push notifications, with recipient groups and trigger events still to define.
- Search results usable within 3 seconds on a typical mobile connection under MVP load.
- Reliable Lead creation before WhatsApp handoff, with recoverable failure states.
- Data minimization, explicit tenant consent, and strict role-based access control.
- Auditability for moderation, verification, availability and Report actions.
- WCAG 2.2 AA accessibility target, including keyboard support, focus management, minimum touch targets, live-region feedback and reduced-motion support.

**Scale & Complexity:**

- Primary domain: server-rendered full-stack web application with PWA capabilities.
- Complexity level: medium.
- Estimated architectural components: 10.

The complexity does not come from scale or real-time collaboration. It comes from preserving trustworthy state transitions across public discovery, Commissionnaire operations, moderation, external WhatsApp handoff, authentication, media handling and PWA notifications.

### Technical Constraints & Dependencies

Confirmed implementation constraints:

- Classical Django application with server-rendered HTML.
- Tailwind CSS for styling.
- JavaScript kept modular and separate from HTML templates.
- SQLite for the initial stage.
- Email/password authentication and Google authentication.
- PWA delivery rather than native mobile applications.
- Payments explicitly deferred.
- WhatsApp handoff through generated deep links; Maison does not inspect private conversations.
- Real property photo uploads are required for listings.

Dependencies and decisions to resolve later:

- Push notification delivery strategy and notification triggers.
- Offline scope: installability only, or limited cached browsing and offline fallback.
- Tenant authentication boundary: lightweight Lead identification versus optional or required Tenant accounts.
- Media storage approach when moving beyond local development.
- SQLite exit criteria before production concurrency becomes a concern.
- Exact Verification Checklist and Listing freshness period.

### Cross-Cutting Concerns Identified

- Role-based authorization for Tenants, Commissionnaires and Moderators.
- Consent capture and privacy boundaries for tenant contact information.
- Auditable state machines for Listings, Leads, Reports and Verification.
- Mobile-first performance and image optimization.
- Recoverable failures around external WhatsApp transitions.
- Notification permission UX and platform differences between Android and iOS.
- Trust-language guardrails: selective verification must never imply transaction guarantees.
- Accessibility across drawers, modals, filters, galleries and operational forms.
- Progressive migration path from SQLite and local media storage as usage grows.

## Starter Template Evaluation

### Primary Technology Domain

Server-rendered full-stack Django web application with progressive PWA capabilities.

### Starter Options Considered

**1. Native Django scaffold — selected**

Use Django's official `startproject` command and add only the required frontend tooling. This keeps the initial architecture explicit, small and easy to evolve.

**2. Cookiecutter Django — rejected for the MVP**

Cookiecutter Django is actively maintained and production-oriented. It includes PostgreSQL, environment layering, Docker options, cloud storage choices, email integrations and other operational decisions. Those capabilities are useful later, but they would introduce too many moving parts for the requested SQLite-first foundation.

**3. Django-Tailwind integration package — deferred**

`django-tailwind` is maintained and supports Tailwind CSS v4. It adds a generated Django theme app and development commands. Maison does not need that abstraction initially: the official Tailwind CLI is sufficient and keeps the asset pipeline easier to understand.

### Selected Starter: Native Django 5.2 LTS Scaffold

**Rationale for Selection:**

Maison requires a classical Django application: server-rendered templates, modular JavaScript, SQLite initially, Tailwind CSS, Django authentication extensions, media handling and PWA assets. The native scaffold provides the right amount of structure without committing the project prematurely to Docker, PostgreSQL, an API framework or a frontend framework.

Django `5.2.14 LTS` is selected over `6.0.5` because its extended support lasts until April 2028 and it offers a conservative baseline for third-party integrations.

**Initialization Commands:**

```powershell
py -3.14 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install "Django==5.2.14"
python -m django startproject config .
npm install --save-dev tailwindcss@4.3.0 @tailwindcss/cli@4.3.0
```

**Architectural Decisions Provided by Starter:**

**Language & Runtime:**
- Python `3.14.x`
- Django `5.2.14 LTS`
- SQLite development database using Django's default configuration

**Styling Solution:**
- Tailwind CSS `4.3.0`
- Official `@tailwindcss/cli`
- Compiled stylesheet stored under Django static assets
- No Tailwind CDN and no runtime CSS generation

**Build Tooling:**
- Minimal npm scripts for Tailwind build and watch modes
- Django static asset handling
- Separate JavaScript modules under static assets
- PWA manifest, service worker and push-notification support added explicitly during implementation

**Testing Framework:**
- Django's built-in test runner available immediately
- Focused test structure added alongside domain apps
- No additional testing framework imposed by the starter

**Code Organization:**
- `config/` for project settings, URLs and deployment entry points
- Domain apps introduced deliberately for marketplace concerns
- Shared templates and static assets organized explicitly
- Django admin enabled as an internal operational starting point

**Development Experience:**
- Django development server with automatic reload
- Tailwind CLI watch process for CSS changes
- A transparent structure suitable for incremental implementation

**Note:** Project initialization using these commands should be the first implementation story.

## Core Architectural Decisions

### Data Architecture

**Database: SQLite first**

Maison will start with SQLite for local development and the first implementation phase. This matches the user's preference for a simple Django foundation.

SQLite remains acceptable while the project is local, single-developer, and validation-oriented. A migration path to PostgreSQL is preserved for later, especially if Maison moves toward a public launch with concurrent writes, stronger backups, multi-worker deployment, or larger media and Lead volume.

Potential future deployment targets remain open: PythonAnywhere or VPS.

**Media storage: local first**

Listing photos will use Django's local media handling during development:

- `MEDIA_ROOT` for uploaded files
- `MEDIA_URL` for development serving
- `ImageField`/file fields for listing media
- local filesystem storage in the first phase

Object storage is deferred until public deployment needs are clearer.

**Currency model: USD only for MVP**

Listing prices will be modeled in USD for the MVP. Prices should be stored as integer minor units or an integer monthly amount plus explicit currency code, rather than as floating-point values.

**Audit events: explicit business history**

Maison needs explicit audit/event records beyond Django admin logs. The architecture should model important business events directly, including:

- Listing availability changes
- Moderation actions
- Verification badge application and removal
- Report submission and resolution
- Lead creation and Lead status changes
- Future notification-related events where relevant

**Caching: no Redis initially**

No Redis or external cache will be introduced at the start. The first optimization layer is:

- good model boundaries
- indexed queries
- pagination
- selective prefetching
- image-size discipline
- avoiding unnecessary frontend payload

Redis or another cache can be revisited later if real usage shows the need.

### Authentication & Security

**Custom Django User from the start**

Maison will use a custom Django user model based on `AbstractUser`. The model stays simple, but it must exist from the first migration to avoid painful changes later.

Required user identity fields:

- email
- WhatsApp phone number
- password for email/password accounts
- Google social account where applicable

**Authentication methods**

Maison will support:

- email/password login
- Google login via `django-allauth`
- session-based Django authentication

`django-allauth` version verified: `65.18.0`.

**Public browsing with gated actions**

Anonymous visitors can browse listings and see the public marketplace surface.

Authentication is required for:

- viewing full listing details beyond the public preview
- contacting a commissionnaire on WhatsApp
- saving or future account-based actions
- accessing commissionnaire surfaces
- accessing moderation surfaces

The login flow should appear as a quick modal/sheet when a gated action is attempted, with Google and email/password options.

**WhatsApp number requirement**

Every registered user must provide a WhatsApp phone number. For Google signup, if the provider does not supply a phone number, Maison must require phone completion before allowing gated marketplace actions.

**Commissionnaire access**

Commissionnaires must be authenticated and linked to a `CommissionnaireProfile`. A commissionnaire cannot publish listings or view Leads without a valid profile.

**Moderator access**

Moderators use Django groups and permissions:

- `is_staff` for admin access
- `Moderators` group for moderation actions
- explicit business audit events for moderation, verification and report handling

**Security posture**

Maison uses standard Django web security:

- server-side sessions
- CSRF protection on all POST forms
- permission checks in views/services
- no public API in the MVP
- HTTPS required for public deployment
- uploaded media treated carefully and not trusted as executable content

### API & Communication Patterns

**No public API for MVP**

Maison will not expose a public REST, GraphQL or mobile API in the MVP. The product is a server-rendered Django web application.

**Primary communication pattern: Django views + templates**

Most user flows use standard Django views:

- listing browse and search pages
- partial or full listing detail pages
- authentication-gated detail access
- commissionnaire dashboard
- publication forms
- moderation queues
- report handling

**Internal JSON endpoints only when useful**

Small authenticated internal JSON endpoints are allowed for progressive UI behavior, but only when they simplify the experience:

- creating a Lead before WhatsApp handoff
- returning a WhatsApp handoff URL after Lead creation
- toggling favorite-like actions later
- registering or updating PWA push subscriptions
- possibly refreshing filter results without a full page reload

These endpoints are not a public API contract.

**WhatsApp handoff flow**

The WhatsApp contact flow must be server-authoritative:

1. User must be authenticated.
2. User must have a WhatsApp number.
3. User confirms contact action.
4. Django creates the Lead in the database.
5. Django records a Lead/audit event.
6. Django returns or redirects to the generated WhatsApp URL.

If Lead creation fails, WhatsApp must not open.

**Error handling**

- HTML form errors for normal Django form submissions.
- Inline recoverable errors for JavaScript-enhanced flows.
- Django messages only for broad page-level feedback.
- No silent failures around Lead creation, report submission, publication, verification or availability changes.

**No Django REST Framework initially**

DRF is deferred until Maison needs a real external API, native mobile client, partner integration, or richer asynchronous frontend.

### Frontend Architecture

**Server-rendered Django first**

Maison will use Django templates as the primary frontend architecture. There is no React, Vue, SPA router or client-side application shell in the MVP.

Django owns:

- page routing
- template rendering
- form rendering and validation
- authentication gates
- permission-sensitive content
- SEO-friendly public marketplace surfaces

**Template organization**

Use a predictable Django template structure:

- `base.html` for global shell, metadata, CSS and JavaScript includes
- shared partials for header, navigation, listing cards, modals and form fields
- app-level templates for marketplace, accounts, commissionnaire and moderation flows
- small template includes rather than large monolithic pages

**Tailwind CSS**

Maison uses Tailwind CSS `4.3.0` through the official CLI.

- No Tailwind CDN in production
- No runtime CSS generation
- Design tokens from `DESIGN.md` mapped into CSS/Tailwind conventions
- Compiled CSS served through Django static files

**JavaScript architecture**

JavaScript stays modular, separate from templates and progressively enhances Django-rendered pages.

Use page-focused modules for:

- listing detail drawer/screen behavior
- authentication modal/sheet for gated actions
- Lead creation before WhatsApp handoff
- filter enhancement where useful
- report modal
- gallery interactions
- PWA install and notification permission flows

Avoid inline JavaScript except small `data-*` hooks in templates.

**State management**

No global frontend state library.

State belongs in:

- Django/database for business state
- forms and query parameters for filters
- small local module state for UI interactions
- service worker cache only for static/offline behavior

**Authentication-gated UX**

Anonymous users can browse public listing cards and marketplace surfaces.

When they attempt gated actions, Maison opens a quick login/signup modal or sheet:

- Google login
- email/password login
- account creation
- WhatsApp number completion when missing

Gated actions include:

- full listing detail beyond public preview
- WhatsApp contact
- future favorites or saved actions

**PWA architecture**

Maison will include:

- web app manifest
- installable icons
- service worker
- offline fallback page
- static asset caching
- push subscription registration when notifications are enabled

The MVP should not promise full offline marketplace behavior. Listing publication, Lead creation, moderation and contact handoff remain online-only.

**Push notifications**

Push notifications are supported architecturally but introduced carefully.

Likely notification targets:

- commissionnaire receives a new Lead
- commissionnaire gets a freshness/reconfirmation reminder
- moderator receives a new report or listing awaiting review

Notification permission must be requested after meaningful user action, not on first page load.

iOS/iPadOS support requires the web app to be added to the Home Screen for web push behavior, so the UX must explain this rather than pretending notifications work identically everywhere.

**Performance and accessibility**

Frontend implementation must preserve the UX contract:

- mobile-first layout
- listing-shaped skeletons instead of full-page spinners
- 150-250ms transitions
- `prefers-reduced-motion` support
- focus trapping in modals/drawers
- focus restoration after close
- visible labels and 44px touch targets
- no color-only status communication

### Infrastructure & Deployment

**Deployment target: open between PythonAnywhere and VPS**

Maison does not choose a final public hosting target yet. The architecture keeps both likely paths viable:

- PythonAnywhere for the simplest Django deployment path
- VPS for more control over Nginx, Gunicorn, static/media serving, backups and future PostgreSQL

The local-first phase remains the priority.

**Environment configuration**

Use environment variables for deployment-sensitive settings:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- database configuration when PostgreSQL is introduced
- Google OAuth credentials
- push notification/VAPID keys later
- email settings later

Settings should be split or structured so local development remains simple while public deployment can be hardened.

**Static files**

Use Django staticfiles with `collectstatic`.

- Tailwind output is committed or built before collection, depending on the final workflow.
- `STATIC_ROOT` is used for collected files.
- Production/static hosting depends on deployment target:
  - PythonAnywhere static mappings if PythonAnywhere is selected
  - Nginx static serving if VPS is selected

**Media files**

Media files stay local during development.

For public deployment:

- PythonAnywhere can serve media through configured mappings for the first small launch.
- VPS should serve media through Nginx with strict upload validation.
- Object storage remains deferred until volume, backup needs or portability justify it.

Uploaded files are untrusted and must never be executed by the web server.

**HTTPS and PWA**

Public deployment must use HTTPS. This is required for secure authentication, service workers and push-related browser APIs.

Localhost remains acceptable for local PWA development.

**Process model**

Initial deployment can run as a traditional WSGI Django app.

- PythonAnywhere: hosted WSGI configuration.
- VPS: Gunicorn behind Nginx.

No ASGI/WebSocket requirement exists in the MVP.

**Database and backups**

SQLite is acceptable locally and during early private testing.

Before meaningful public usage, the project should revisit:

- PostgreSQL migration
- database backup process
- media backup process
- restore testing
- log retention

**CI/CD**

No heavy CI/CD platform is required immediately. Minimum quality gate before implementation grows:

- run Django tests
- run migrations check
- run `python manage.py check`
- build Tailwind CSS
- collect static files for deployment validation

**Monitoring and logging**

Start with Django structured application logs and explicit audit events in the database.

Later additions may include:

- error tracking
- uptime monitoring
- request metrics
- notification delivery diagnostics

### Decision Priority Analysis

**Critical Decisions:**

- Django 5.2 LTS server-rendered application.
- SQLite first, PostgreSQL deferred.
- Custom Django user from the first migration.
- Email/password and Google auth through django-allauth.
- Authenticated access required for full details and WhatsApp contact.
- Django templates, Tailwind CLI and modular JavaScript.
- No public API or DRF in the MVP.
- Explicit audit events for sensitive business actions.

**Important Decisions:**

- Local media storage first.
- USD-only pricing for MVP.
- PWA installability with service worker and offline fallback.
- Push notifications supported architecturally but introduced carefully.
- PythonAnywhere and VPS both remain viable deployment targets.

**Deferred Decisions:**

- PostgreSQL migration timing.
- Object storage.
- Redis/cache.
- DRF or public API.
- Payments.
- Full offline marketplace behavior.
- Error tracking and advanced monitoring.

### Decision Impact Analysis

**Implementation Sequence:**

1. Initialize Django project, custom user and settings.
2. Add Tailwind build pipeline and base templates.
3. Build auth and WhatsApp-number completion.
4. Model listings, photos, commissionnaire profiles and audit events.
5. Build public browse and gated detail/contact flows.
6. Build Lead creation before WhatsApp handoff.
7. Build commissionnaire publication and dashboard.
8. Build moderation, reports and verification.
9. Add PWA manifest, service worker and notification subscription foundation.
10. Add deployment hardening when moving beyond local/private use.

**Cross-Component Dependencies:**

- Auth affects listing detail access, contact flow, commissionnaire dashboard and moderation.
- Audit events affect listings, leads, reports, verification and notifications.
- PWA notifications depend on authenticated users, notification subscriptions and meaningful business events.
- Media storage affects listing publication, performance and deployment.
- SQLite remains acceptable locally, but deployment scale may force PostgreSQL later.

## Implementation Patterns & Consistency Rules

### Pattern Categories Defined

**Critical Conflict Points Identified:** 9 areas: naming, Django app boundaries, templates, static assets, internal JSON endpoints, audit events, forms/validation, errors/loading states, and tests.

### Naming Patterns

**Database Naming Conventions:**

- Use Django defaults unless there is a strong reason not to.
- Model classes use `PascalCase`: `Listing`, `Lead`, `AuditEvent`.
- Fields use `snake_case`: `whatsapp_phone`, `created_at`, `verified_at`.
- Status values use lowercase `snake_case`: `available`, `under_review`, `correction_required`.
- Use explicit timestamp names: `created_at`, `updated_at`, `submitted_at`, `resolved_at`.

**Code Naming Conventions:**

- Python modules, functions and variables use `snake_case`.
- Python classes use `PascalCase`.
- Django templates use lowercase path names grouped by app.
- JavaScript files use kebab-case: `listing-detail.js`, `auth-gate.js`.
- JavaScript functions use `camelCase`.

**Internal Endpoint Naming:**

- Internal JSON endpoints live under feature paths, not `/api/`.
- Use action-oriented names only for state changes, e.g. `/listings/<id>/create-lead/`.
- Query parameters use `snake_case`.

### Structure Patterns

**Project Organization:**

- Keep business logic out of templates.
- Use Django forms for validation.
- Use small service functions for state-changing workflows such as Lead creation, verification, report resolution and availability changes.
- Keep public marketplace, commissionnaire and moderation concerns separated by app/module boundaries.

**Templates and Static Assets:**

- Use `base.html` plus small includes for repeated UI.
- Use `data-*` attributes as JavaScript hooks.
- No inline JavaScript for business behavior.
- Static JavaScript modules should enhance server-rendered HTML, not replace it.

### Format Patterns

**Internal JSON Response Formats:**

- Success: `{ "ok": true, "data": { ... } }`
- Failure: `{ "ok": false, "error": { "code": "...", "message": "..." } }`
- Dates in JSON use ISO 8601 strings.
- JSON field names use `snake_case`.

**User-Facing Errors:**

- Form errors appear next to fields.
- Gated-action errors appear inside the modal/sheet.
- Lead creation failures must preserve entered state and must not open WhatsApp.

### Communication Patterns

**Audit Event Patterns:**

- Audit event types use dot notation: `listing.verified`, `lead.created`, `report.resolved`.
- Every audit event records actor, target object, event type, timestamp and metadata.
- Audit events are append-only.

**PWA/Notification Events:**

- Notification subscriptions are user-owned.
- Push events must correspond to explicit business events, not vague engagement nudges.
- Notification permission is requested only after user action.

### Process Patterns

**Authentication Gates:**

- Server checks permissions first.
- JavaScript may open the quick auth modal, but cannot be the only gate.
- Missing WhatsApp phone number routes to profile completion before gated actions.

**Loading States:**

- Use local loading states near the action.
- Search uses listing-shaped skeletons.
- Forms disable submit buttons during submission.
- Avoid full-page spinners.

**Testing Patterns:**

- Tests live near the app they validate.
- State transitions require tests.
- Permission boundaries require tests.
- WhatsApp handoff must test that Lead creation happens before URL generation.

### Enforcement Guidelines

**All AI Agents MUST:**

- Follow Django server-rendered architecture.
- Keep JavaScript modular and progressive.
- Use Django forms/services for validation and state changes.
- Record explicit audit events for sensitive business actions.
- Preserve the trust-language boundaries from the PRD and UX docs.
- Avoid introducing DRF, Redis, PostgreSQL, React or payments unless a later architecture update explicitly allows it.

**Anti-Patterns:**

- Inline scripts that create Leads directly from templates.
- Trust copy that implies Maison guarantees an offline transaction.
- Public API routes invented before they are needed.
- Business state changed only through Django admin logs.
- JavaScript-only permission checks.
- Upload handling that trusts file names, extensions or MIME types without validation.

## Project Structure & Boundaries

### Complete Project Directory Structure

```text
maison/
├── manage.py
├── requirements.txt
├── requirements-dev.txt
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
│   │   ├── models.py
│   │   ├── validators.py
│   │   ├── services.py
│   │   └── tests/
│   ├── accounts/
│   │   ├── models.py          # CustomUser
│   │   ├── forms.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests/
│   ├── listings/
│   │   ├── models.py          # Listing, ListingPhoto
│   │   ├── forms.py
│   │   ├── selectors.py
│   │   ├── services.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests/
│   ├── commissionnaires/
│   │   ├── models.py          # CommissionnaireProfile
│   │   ├── forms.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests/
│   ├── leads/
│   │   ├── models.py          # Lead, LeadStatusEvent
│   │   ├── services.py        # create lead before WhatsApp
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests/
│   ├── moderation/
│   │   ├── models.py          # Report, verification/check states if needed
│   │   ├── forms.py
│   │   ├── services.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests/
│   ├── audit/
│   │   ├── models.py          # AuditEvent
│   │   ├── services.py
│   │   └── tests/
│   └── pwa/
│       ├── models.py          # PushSubscription
│       ├── views.py           # manifest + service worker
│       ├── urls.py
│       └── tests/
├── templates/
│   ├── base.html
│   ├── includes/
│   ├── accounts/
│   ├── listings/
│   ├── commissionnaires/
│   ├── moderation/
│   └── pwa/
├── static_src/
│   ├── css/input.css
│   └── js/
│       ├── auth-gate.js
│       ├── listing-detail.js
│       ├── lead-handoff.js
│       ├── filters.js
│       ├── gallery.js
│       └── pwa.js
├── static/
│   ├── css/app.css
│   ├── js/
│   ├── icons/
│   └── images/
├── media/
└── docs/
```

### Architectural Boundaries

**API Boundaries:**

- No public `/api/` namespace in the MVP.
- Internal JSON endpoints stay inside feature apps, e.g. `leads/create-lead/`.
- All state-changing endpoints require server-side auth, permissions and CSRF.

**Component Boundaries:**

- `accounts`: user identity, auth gates, WhatsApp phone completion.
- `listings`: public discovery, listing detail, photos, filters, availability.
- `commissionnaires`: professional profile, publication dashboard, own inventory.
- `leads`: Lead creation, WhatsApp handoff, lead status.
- `moderation`: reports, listing review, verification.
- `audit`: append-only business events.
- `pwa`: manifest, service worker, push subscriptions.
- `core`: shared validators, constants and generic utilities only.

### Requirements to Structure Mapping

- FR-1 to FR-3: `apps/listings`, `templates/listings`, `static_src/js/filters.js`, `listing-detail.js`
- FR-4 to FR-6: `apps/commissionnaires`, `apps/listings/forms.py`, `apps/listings/services.py`
- FR-7 to FR-10: `apps/accounts`, `apps/leads`, `static_src/js/lead-handoff.js`
- FR-11 to FR-13: `apps/moderation`, `apps/audit`
- FR-14: `apps/listings`, `apps/audit`
- PWA and notifications: `apps/pwa`, `static_src/js/pwa.js`, `templates/pwa`

### Integration Points

**Internal Communication:**

- Views call forms/selectors/services.
- Services perform state changes and write audit events.
- Templates render server-owned state.
- JavaScript calls only small internal endpoints for progressive enhancement.

**External Integrations:**

- Google OAuth through `django-allauth`.
- WhatsApp through generated deep links after Lead creation.
- Web Push endpoints later through stored `PushSubscription` records.

**Data Flow:**

1. Visitor browses public listings.
2. Gated action opens auth/profile completion if needed.
3. Authenticated user requests contact.
4. `leads.services.create_lead_for_listing()` creates Lead and audit event.
5. Server returns WhatsApp URL.
6. Browser opens WhatsApp only after successful Lead creation.

## Architecture Validation Results

### Coherence Validation ✅

**Decision Compatibility:**

All major decisions work together: Django 5.2 LTS, SQLite-first, server-rendered templates, Tailwind CLI, modular JavaScript, django-allauth, local media and PWA support form a coherent simple-stack architecture.

Django latest is now `6.0.6`, but `5.2.14 LTS` remains intentionally selected for stability. `django-allauth` is `65.18.0`; Tailwind and `@tailwindcss/cli` are `4.3.0`.

**Pattern Consistency:**

Implementation patterns reinforce the architecture: server-owned state, services for state transitions, Django forms for validation, internal JSON only where progressive enhancement needs it, and explicit audit events for trust-sensitive workflows.

**Structure Alignment:**

The proposed app structure maps directly to product boundaries: listings, accounts, commissionnaires, leads, moderation, audit and PWA.

### Requirements Coverage Validation ✅

**Functional Requirements Coverage:**

- FR-1 to FR-3 are covered by `listings`, templates and filter/detail JavaScript.
- FR-4 to FR-6 are covered by `commissionnaires`, `listings` forms/services and media handling.
- FR-7 to FR-10 are covered by `accounts`, `leads` and the WhatsApp handoff service.
- FR-11 to FR-13 are covered by `moderation` and `audit`.
- FR-14 is covered by listing freshness, verification state and audit history.

**Non-Functional Requirements Coverage:**

Security, auditability, mobile-first UX, PWA installation, push-notification foundation, recoverable WhatsApp errors, accessibility and performance constraints are all architecturally addressed.

### Gap Analysis Results

**Critical Gaps:** None.

**Important Tracked Decisions:**

- Exact Verification Checklist.
- Listing freshness/reconfirmation period.
- Public/private boundary of listing detail content.
- Final hosting choice: PythonAnywhere or VPS.
- PostgreSQL migration threshold.

These do not block architecture. They should be resolved during implementation planning or story creation.

### Architecture Completeness Checklist

**Requirements Analysis**

- [x] Project context thoroughly analyzed
- [x] Scale and complexity assessed
- [x] Technical constraints identified
- [x] Cross-cutting concerns mapped

**Architectural Decisions**

- [x] Critical decisions documented with versions
- [x] Technology stack fully specified
- [x] Integration patterns defined
- [x] Performance considerations addressed

**Implementation Patterns**

- [x] Naming conventions established
- [x] Structure patterns defined
- [x] Communication patterns specified
- [x] Process patterns documented

**Project Structure**

- [x] Complete directory structure defined
- [x] Component boundaries established
- [x] Integration points mapped
- [x] Requirements to structure mapping complete

### Architecture Readiness Assessment

**Overall Status:** READY FOR IMPLEMENTATION

**Confidence Level:** High

**Key Strengths:**

- Simple Django architecture aligned with the user's stack preference.
- Clear boundaries for marketplace, leads, moderation and PWA.
- Strong audit and trust-language guardrails.
- No premature API, React, Redis, PostgreSQL or payments complexity.

**Areas for Future Enhancement:**

- PostgreSQL and object storage when public usage grows.
- Error tracking and uptime monitoring.
- DRF or external API if native apps or partners appear.
- Stronger notification delivery diagnostics.

### Implementation Handoff

**AI Agent Guidelines:**

- Follow the documented Django server-rendered architecture.
- Do not introduce unapproved technologies.
- Preserve authentication gates and WhatsApp-number requirements.
- Create Leads before WhatsApp handoff.
- Record audit events for sensitive state changes.
- Respect PRD/UX trust boundaries.

**First Implementation Priority:**

Initialize the Django project, custom user model, settings, Tailwind pipeline and base template structure.
