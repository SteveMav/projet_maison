---
stepsCompleted: [1, 2, 3]
inputDocuments:
  - "_bmad-output/planning-artifacts/prds/prd-maison-2026-05-31/prd.md"
  - "_bmad-output/planning-artifacts/prds/prd-maison-2026-05-31/addendum.md"
  - "_bmad-output/planning-artifacts/architecture.md"
  - "_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/DESIGN.md"
  - "_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/EXPERIENCE.md"
---

# maison - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for maison, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR-1: A Tenant can browse available rental Listings ordered by recency; search results display only `available` Listings, each Listing Card displays monthly price, Commune, bedroom count, primary photo, and Verification Badge when applicable, and each card opens its Listing Detail Page.

FR-2: A Tenant can filter rental Listings by Commune, monthly budget range, and bedroom count; combined filters must return Listings satisfying every active filter, individual filters can be removed, all filters can be cleared, and an explicit empty state appears when there are no matches.

FR-3: A Tenant can review Listing details needed to decide whether to contact a Commissionnaire; the Listing Detail Page displays all Listing Card fields, media, description, Availability Status, Commissionnaire Profile identity, a Report Action, and the WhatsApp Contact Action only while the Listing is `available`.

FR-4: A Commissionnaire can create and maintain the minimum Profile required to publish Listings; Maison requires display name and reachable WhatsApp phone number before publication, associates each submitted Listing with exactly one Commissionnaire Profile, and allows Profile updates without losing existing Listings or Leads.

FR-5: A Commissionnaire can submit a valid rental Listing that meets the publication standard; Maison requires monthly price, Commune, bedroom count, description, Availability Status, and at least three photos, rejects unsupported or unusable media with correction guidance, stores submission and update timestamps, and associates each Listing with exactly one Commissionnaire Profile.

FR-6: A Commissionnaire can maintain a Listing's Availability Status after publication; they can mark a Listing `unavailable`, unavailable Listings disappear from search and hide the WhatsApp Contact Action, Maison records each status-change timestamp, and Maison prompts availability reconfirmation after a defined freshness period.

FR-7: A Tenant can complete Lightweight Identification before initiating a WhatsApp Handoff; Maison explains the purpose, requires explicit consent, validates required fields, and blocks handoff until the required identification fields are valid.

FR-8: Maison creates an attributable Lead when an identified Tenant confirms the WhatsApp Contact Action; the Lead records Tenant identifier, Listing, Commissionnaire Profile, timestamp, acquisition context available to Maison, is created before WhatsApp opens, and repeated contact attempts remain distinguishable in event history.

FR-9: Maison opens a WhatsApp conversation with the Listing's Commissionnaire after Lead creation; the handoff targets the Commissionnaire Profile phone number, includes a prefilled Listing identifier and human-readable Lead reference, and does not claim to track WhatsApp contents, visits, negotiation, payment, or contract execution.

FR-10: A Commissionnaire can view Leads attributed to their Listings; they see only Leads associated with their own Commissionnaire Profile, each Lead identifies the originating Listing and creation timestamp, and v1 includes basic Lead Status values `new`, `contacted`, and `closed` with status-change timestamps if retained for MVP.

FR-11: A Moderator can review Listing submissions and control visibility; they can publish, request correction, reject, or remove a Listing, Maison records the action, actor, timestamp, and resulting moderation state, and removed Listings disappear from search results.

FR-12: A Moderator can apply or remove a Verification Badge for a specific Listing; Maison displays the badge only while the Listing is marked verified, requires completion of the Verification Checklist before applying the badge, and removes the public badge immediately when verified state is removed.

FR-13: A Tenant can submit a Report from a Listing Detail Page; the Report identifies the Listing and associated Commissionnaire Profile, includes a selected reason and optional notes, confirms receipt without exposing internal moderation details, and can be reviewed and resolved by a Moderator.

FR-14: A Tenant can distinguish ordinary publication information from stronger Verification; Verified Listings display the Verification Badge consistently on Listing Cards and Detail Pages, unverified Listings never display the badge, the Listing Detail Page displays last update time, and v1 may display Listing view count as a secondary trust signal.

### NonFunctional Requirements

NFR-1: The Product Surface must support the Tenant and Commissionnaire journeys on current mobile browsers without requiring a native application.

NFR-2: Search results should become usable within 3 seconds on a typical mobile connection in Kinshasa under expected MVP load; the WhatsApp Contact Action must not open WhatsApp until Lead creation succeeds or Maison presents a recoverable error.

NFR-3: Maison must collect only the Tenant and Commissionnaire data required for the defined journeys, prevent Commissionnaires from viewing other Commissionnaires' Leads, require Moderator access for Moderator-only actions, and record consent for Lightweight Identification.

NFR-4: Maison must retain timestamps and actor identity for Listing moderation, Verification Badge changes, Availability Status changes, and Report resolution.

NFR-5: Maison must not silently discard Lead creation outcomes when a WhatsApp Handoff fails, and Tenants must receive a recoverable error state if Lead creation fails.

### Additional Requirements

- Use a native Django 5.2 LTS scaffold as the selected starter; project initialization using Django, Tailwind CLI, settings, and base structure is the first implementation story.
- Use Python 3.14.x, Django 5.2.14 LTS, SQLite first, and a custom Django user model from the first migration.
- Use Tailwind CSS 4.3.0 through the official CLI; do not use Tailwind CDN or runtime CSS generation.
- Build a server-rendered Django application with templates as the primary frontend; do not introduce React, Vue, SPA routing, Django REST Framework, a public API, Redis, PostgreSQL, or payments in MVP without later architecture approval.
- Organize implementation around explicit app boundaries: `core`, `accounts`, `listings`, `commissionnaires`, `leads`, `moderation`, `audit`, and `pwa`.
- Implement email/password authentication, Google authentication through `django-allauth`, session-based auth, and mandatory WhatsApp phone completion before gated marketplace actions.
- Allow anonymous users to browse public listing cards and marketplace surfaces; require authentication for full listing detail beyond public preview, WhatsApp contact, commissionnaire surfaces, and moderation surfaces.
- Use a quick modal or sheet for gated authentication and profile completion, preserving the attempted destination.
- Treat the WhatsApp handoff as server-authoritative: authenticate the user, verify WhatsApp phone availability, collect confirmation, create the Lead, write an audit event, then return or redirect to the generated WhatsApp URL.
- If Lead creation fails, do not open WhatsApp; show a recoverable inline error that preserves user-entered identification data.
- Use internal JSON endpoints only for progressive enhancement where useful, such as Lead creation before WhatsApp handoff, push subscription registration, or filter refresh; every state-changing endpoint must enforce server-side auth, permissions, and CSRF.
- Store prices as USD using integer-safe representation rather than floating-point values.
- Use local media storage first with Django `MEDIA_ROOT` and `MEDIA_URL`; uploaded files are untrusted and must be validated so they cannot be executed or abused.
- Model explicit append-only business audit events for Listing availability changes, moderation actions, Verification Badge application/removal, Report submission/resolution, Lead creation, Lead status changes, and future notification events.
- Start without Redis or external cache; use indexed queries, pagination, selective prefetching, image-size discipline, and small frontend payloads as first performance controls.
- Include PWA manifest, installable icons, service worker, offline fallback page, static asset caching, and a push-subscription foundation, while avoiding promises of full offline marketplace behavior.
- Request notification permission only after meaningful user action; likely notification targets are new Leads, freshness reminders, new reports, and listings awaiting review.
- Account for iOS/iPadOS web push constraints by explaining Home Screen installation requirements rather than implying identical platform behavior.
- Keep deployment open between PythonAnywhere and VPS; use environment variables for deployment-sensitive settings, `collectstatic`, HTTPS for public deployment, and local media during development.
- Add minimum quality gates: Django tests, migration checks, `python manage.py check`, Tailwind build, and static collection validation.
- Add tests for state transitions, permission boundaries, and the invariant that Lead creation occurs before WhatsApp URL generation.
- Follow architecture naming conventions: Django model classes in `PascalCase`, fields in `snake_case`, status values in lowercase `snake_case`, JavaScript files in `kebab-case`, and internal JSON field names in `snake_case`.
- Use Django forms for validation, small service functions for state-changing workflows, selectors where useful, and keep business logic out of templates.
- Preserve PRD and UX trust-language guardrails: never imply every Listing is verified, never display the Verification Badge before checklist completion, and never imply Maison guarantees offline transaction outcomes.

### UX Design Requirements

UX-DR1: Implement the Maison design token system with warm neutral surfaces, deep green primary action/trust colors, terracotta only as a minor cue, semantic warning/error/trust surfaces, hairline borders, and a 40% ink scrim for overlays.

UX-DR2: Implement Manrope typography with Segoe UI fallback and the defined display, heading, body, and label roles; keep readable body copy at least 16px, avoid oversized operational headings, and keep paragraph lines near 65 characters.

UX-DR3: Implement the responsive spacing and layout system: 4px baseline, 16px mobile side margins, 24px-32px tablet margins, desktop max width around 1280px-1420px, and major section spacing of 40px-64px.

UX-DR4: Implement shape rules: 10px control radius, 16px listing card/grouped operational radius, 24px drawer/large-section radius, full-radius pills only for filters/status/badges, and circular icon buttons only for familiar controls.

UX-DR5: Implement primary, secondary, text, and icon button variants with default, hover, focus, active, loading, and disabled states; primary buttons must use the deep green action color, be at least 48px high, and use a subtle 0.97 press response.

UX-DR6: Implement desktop header navigation with compact mark, wordmark, tenant navigation, `Espace pro`, and `Publier un bien`; implement mobile bottom navigation with visible labels for `Explorer`, `Favoris`, and `Espace pro`.

UX-DR7: Implement the search form with visible labels, Commune, budget maximum/range, and bedroom controls; desktop may group fields in one raised search surface, while mobile must stack fields vertically.

UX-DR8: Preserve chosen filter values after refresh, support removable selected filter chips, provide a clear-all action, and announce result-count updates through an appropriate live region.

UX-DR9: Use listing-shaped skeletons while search results refresh; skeletons must match card geometry and must not replace the entire page with a full-page spinner.

UX-DR10: Implement the Listing Card as image-first, showing Commune, neighborhood when available, price, bedroom count, property type, freshness, favorite action, and optional verified label; the full card opens detail and favorite remains an independent action.

UX-DR11: Never show a Verification Badge on an unverified Listing; verified state must be communicated with text plus an icon, not color alone.

UX-DR12: Implement the Listing Detail experience as a mobile full-screen surface and desktop right-side drawer of roughly 480px-620px with scrim, preserved browse context, sticky top controls, and sticky bottom WhatsApp CTA when contact is valid.

UX-DR13: Implement Listing Detail accessibility behavior: trap focus inside open drawers/modals, support Escape on desktop, preserve familiar Back behavior on mobile, make closed overlays inert, and restore focus to the triggering element.

UX-DR14: Implement the gallery with a 4:3 main image, horizontal thumbnails, visible image count such as `1/8`, rounded image corners, and meaningful production alt text.

UX-DR15: Implement the Listing Detail content hierarchy: location, title, monthly price, facts, availability, last update, verification explanation where earned, description, Commissionnaire identity, Report Action, and WhatsApp CTA.

UX-DR16: Implement an Availability block that keeps status and last-update copy together; unavailable Listings must hide the WhatsApp CTA and route users back to filtered results.

UX-DR17: Implement the Verification Box only for verified Listings and use the canonical narrow French copy: "Cette annonce a passé un contrôle supplémentaire. Le badge ne garantit pas le résultat d'une transaction hors ligne."

UX-DR18: Implement the Commissionnaire block as a compact identity row with a hairline border and a note that WhatsApp contact follows Lightweight Identification.

UX-DR19: Implement the Report Action as visually secondary error-colored text, opening a reason selection with optional notes and confirming receipt without exposing internal moderation details.

UX-DR20: Implement Lightweight Identification as a modal or sheet that explains why name and phone number are requested, requires explicit consent, includes the privacy reassurance "Maison ne lit pas vos conversations WhatsApp.", and uses one primary action.

UX-DR21: Implement recoverable Lead error handling in the identification flow: preserve entered values, show inline error on an error-soft surface, offer retry, and never open WhatsApp until Lead creation succeeds.

UX-DR22: Implement WhatsApp handoff states: identification required, invalid input with field-level errors, Lead creation loading with disabled CTA, Lead created, Lead creation failed, and WhatsApp open failed with a retry path that acknowledges the Lead exists.

UX-DR23: Implement public discovery states: default recent available Listings, filtering with skeletons and live result-count announcement, empty result copy `Aucune annonce ne correspond exactement.` with one reset action, available detail state, unavailable detail state, verified state, unverified state, and Report submitted state.

UX-DR24: Implement Commissionnaire operational states for inventory rows: visible, reconfirm soon, unavailable, draft, awaiting moderation, and correction required, each with text plus icon/status cues and clear next action where applicable.

UX-DR25: Implement Lead rows for Commissionnaires showing tenant identity, originating Listing, timestamp, and optional status; never show or imply access to WhatsApp conversation contents.

UX-DR26: Implement Commissionnaire operations with compact rows and hairline dividers rather than nested dashboard cards; avoid oversized hero metrics in operational surfaces.

UX-DR27: Implement the Publication flow as a short mobile-friendly stepper with required rental fields, at least three real photos, precise correction messages for missing/unusable media, and a Listing Card preview before submission.

UX-DR28: Implement Moderator states: submission queued with age and summary, publish without badge, verification checklist, request correction, reject/remove with reason, report open, and report resolved.

UX-DR29: Implement the Verification Checklist as an operational list with explicit checked states, hairline dividers, actor context, and timestamp recording; every checklist item must be complete before badge application.

UX-DR30: Implement access-control UX states: authentication required must preserve attempted destination and avoid exposing operational data, and permission denied must explain lack of access without revealing another Commissionnaire's Leads or moderation data.

UX-DR31: Implement motion rules: 150ms-250ms transitions for drawer/modal/hover/pressed feedback, transform/opacity where possible, no motion for repeated keyboard-driven actions, and reduced-motion support that removes positional movement without losing comprehension.

UX-DR32: Meet the accessibility floor: WCAG 2.2 AA contrast, visible focus, keyboard reachability, at least 44px touch targets, no color-only status communication, live-region feedback for result counts and form failures, and visible mobile bottom navigation labels.

UX-DR33: Implement responsive layouts exactly by range: under 700px one-column listings and full-screen detail; 700px-920px two-column listings and compact navigation; above 920px three-column listings, desktop header, asymmetric browse hero, and right-side detail drawer.

UX-DR34: Use concise French UI copy that avoids manufactured urgency and inflated trust claims; use phrases like `Annonce vérifiée`, `Mise à jour hier`, `Signaler cette annonce`, and recoverable error copy instead of vague or overpromising language.

UX-DR35: Treat photography as part of the trust model: production Listings require real property photos, at least three usable photos, honest lighting, exterior/principal living/detail coverage when available, consistent card crops, and full detail context in the gallery.

UX-DR36: Do not use AI-generated villas, luxury-only placeholders, or architectural renders as silent production listing media; test layouts with ordinary credible rental inventory as well as aspirational placeholders.

UX-DR37: Instrument experience events from launch: browse viewed, filters applied/cleared, Listing detail opened, WhatsApp CTA tapped, Lightweight Identification submitted, Lead created, WhatsApp handoff attempted, Report submitted, Availability changed, Listing reconfirmed, and Lead status changed if retained.

UX-DR38: Preserve the layered trust contract in UI behavior and copy: Published Listing, Last Updated, Verified Listing, View Count, and Report Action are separate signals and must not be collapsed into one generic trust badge.

UX-DR39: Maintain open product decisions explicitly during story creation: exact Verification Checklist, freshness period, three-photo minimum, public view count, manual Lead statuses, and Moderator turnaround expectations.

### FR Coverage Map

FR-1: Epic 2 - Browse recent available rental Listings.

FR-2: Epic 2 - Filter Listings by Commune, budget, and bedroom count.

FR-3: Epic 2 - Review Listing details and contact eligibility.

FR-4: Epic 1 - Create and maintain the Commissionnaire Profile required to participate.

FR-5: Epic 2 - Submit valid rental Listings with required media.

FR-6: Epic 2 - Maintain Listing Availability Status and freshness.

FR-7: Epic 3 - Complete Lightweight Identification before WhatsApp handoff.

FR-8: Epic 3 - Create attributable Leads before WhatsApp opens.

FR-9: Epic 3 - Open WhatsApp with Listing and Lead context.

FR-10: Epic 3 - View Leads attributed to the signed-in Commissionnaire Profile.

FR-11: Epic 4 - Moderate submitted Listings.

FR-12: Epic 4 - Apply or remove Verification selectively.

FR-13: Epic 4 - Submit, review, and resolve Reports.

FR-14: Epic 4 - Display basic trust signals and Verification correctly.

## Epic List

### Epic 1: Account Access and Commissionnaire Profile Foundation

Users can register, authenticate, complete WhatsApp-ready identity, and Commissionnaires can maintain the profile required to participate.

**FRs covered:** FR-4

### Epic 2: Rental Inventory Marketplace

Commissionnaires can publish and maintain useful rental inventory, while Tenants can browse, filter, and inspect available Listings on mobile-first surfaces.

**FRs covered:** FR-1, FR-2, FR-3, FR-5, FR-6

### Epic 3: Traceable WhatsApp Lead Conversion

Tenants can identify themselves, consent, create an attributable Lead, and reach the right Commissionnaire through WhatsApp; Commissionnaires can view attributed demand.

**FRs covered:** FR-7, FR-8, FR-9, FR-10

### Epic 4: Moderation, Verification, and Marketplace Trust

Moderators can control publication quality, apply selective Verification, handle Reports, and expose defensible trust signals without overpromising.

**FRs covered:** FR-11, FR-12, FR-13, FR-14

## Epic 1: Account Access and Commissionnaire Profile Foundation

Users can register, authenticate, complete WhatsApp-ready identity, and Commissionnaires can maintain the profile required to participate.

### Story 1.1: Set up initial project from starter template

As a product team,
I want Maison initialized as a Django 5.2 LTS application with a custom user model and Tailwind foundation,
So that all account, marketplace, and trust workflows can build on the correct base from the first migration.

**Requirements:** FR-4; Architecture starter setup; UX-DR1, UX-DR2, UX-DR3, UX-DR4, UX-DR5.

**Acceptance Criteria:**

**Given** a fresh Maison repository
**When** the implementation is completed
**Then** the project contains a native Django 5.2 LTS scaffold with `config/`, `manage.py`, SQLite settings, and the planned app structure started
**And** a custom Django user model exists from the first migration.

**Given** the frontend foundation is installed
**When** Tailwind is built
**Then** the project uses Tailwind CLI, not CDN/runtime generation
**And** the base CSS includes Maison design tokens for color, typography, spacing, radius, focus, and state primitives.

**Given** a developer validates the foundation
**When** they run Django checks and the Tailwind build
**Then** both complete successfully
**And** no React, DRF, Redis, PostgreSQL, public API, or payment dependency is introduced.

### Story 1.2: Email And Password Account Access

As a user,
I want to create an account and sign in with email and password,
So that Maison can protect gated marketplace actions while keeping public browsing open.

**Requirements:** FR-4; NFR-3; UX-DR30, UX-DR32, UX-DR34.

**Acceptance Criteria:**

**Given** an anonymous visitor
**When** they open public browse surfaces
**Then** they can browse public Listing Cards without signing in
**And** protected account, commissionnaire, and moderator destinations remain inaccessible.

**Given** an anonymous visitor chooses to register
**When** they submit valid email, password, and required profile fields
**Then** Maison creates a user account using the custom user model
**And** the user can sign in with email and password.

**Given** a user submits invalid registration or login information
**When** the form is processed
**Then** Maison shows field-level errors without losing safe entered values
**And** the error copy is concise French UI copy.

**Given** a signed-in user
**When** they try to access account-protected surfaces
**Then** server-side permission checks allow only valid destinations
**And** unauthenticated access attempts preserve the intended destination for later return.

### Story 1.3: Google Account Access

As a user,
I want to sign in with Google,
So that I can enter Maison quickly without creating a separate password first.

**Requirements:** FR-4; NFR-3; UX-DR30, UX-DR34.

**Acceptance Criteria:**

**Given** the authentication foundation exists
**When** Google authentication is configured
**Then** Maison uses `django-allauth` for Google login
**And** the implementation remains session-based Django authentication.

**Given** an anonymous visitor chooses Google sign-in
**When** Google returns a valid authenticated identity
**Then** Maison creates or links the local user account
**And** the user is returned to the intended destination when one was preserved.

**Given** Google does not provide a usable WhatsApp phone number
**When** the signed-in user attempts a gated marketplace action that requires WhatsApp readiness
**Then** Maison routes them to phone completion before the action proceeds
**And** no protected action relies on client-side checks alone.

**Given** Google authentication fails or is cancelled
**When** the user returns to Maison
**Then** Maison shows a recoverable French error state
**And** the user can choose email/password access instead.

### Story 1.4: WhatsApp Phone Completion Gate

As a signed-in user,
I want Maison to confirm my WhatsApp phone number before phone-dependent actions,
So that leads, publication, and commissionnaire contact routes use reachable identity data.

**Requirements:** FR-4; NFR-3; UX-DR20, UX-DR30, UX-DR32, UX-DR34.

**Acceptance Criteria:**

**Given** a signed-in user has no valid WhatsApp phone number
**When** they attempt a WhatsApp-dependent action
**Then** Maison blocks the action server-side
**And** routes the user to a phone completion screen, modal, or sheet with the attempted destination preserved.

**Given** the user submits a valid WhatsApp phone number
**When** the form is saved
**Then** the number is stored on the user identity record
**And** Maison returns the user to the preserved destination or a sensible account surface.

**Given** the user submits an invalid or missing phone number
**When** validation runs
**Then** Maison shows a field-level error
**And** the protected action does not proceed.

**Given** phone completion UI is rendered
**When** a keyboard or screen-reader user interacts with it
**Then** labels, focus order, focus visibility, and touch targets meet the Maison accessibility floor
**And** the copy stays concise and in French.

### Story 1.5: Commissionnaire Profile Management

As a Commissionnaire,
I want to create and update my Commissionnaire Profile,
So that Maison can attribute Listings and Leads to a reachable professional identity.

**Requirements:** FR-4; NFR-3; UX-DR24, UX-DR26, UX-DR30, UX-DR32.

**Acceptance Criteria:**

**Given** a signed-in user with a valid WhatsApp phone number
**When** they create a Commissionnaire Profile with a display name and reachable WhatsApp phone number
**Then** Maison stores the profile and links it to exactly one user identity
**And** the profile becomes eligible for future Listing publication.

**Given** a Commissionnaire updates their profile information
**When** valid changes are saved
**Then** existing Listings and Leads remain associated with the same Commissionnaire Profile
**And** the updated profile identity is shown on future relevant surfaces.

**Given** a user attempts to create or edit a profile with missing required fields
**When** the form is submitted
**Then** Maison shows field-level errors
**And** no incomplete Commissionnaire Profile becomes eligible for publication.

**Given** a signed-in user tries to access another Commissionnaire's profile management surface
**When** the request is processed
**Then** Maison denies access server-side
**And** does not expose private profile, Listing, or Lead data.

**Given** the profile management UI is displayed
**When** it appears on mobile and desktop
**Then** it uses compact French copy, visible labels, 44px touch targets, and the Maison design tokens established in Story 1.1.

## Epic 2: Rental Inventory Marketplace

Commissionnaires can publish and maintain useful rental inventory, while Tenants can browse, filter, and inspect available Listings on mobile-first surfaces.

### Story 2.1: Listing Domain Model And Media Foundation

As a product team,
I want the Listing and ListingPhoto foundation modeled around rental inventory,
So that Tenant discovery and Commissionnaire publication can share a consistent source of truth.

**Requirements:** FR-1, FR-3, FR-5, FR-6; NFR-2; UX-DR35, UX-DR36.

**Acceptance Criteria:**

**Given** the account and Commissionnaire Profile foundation exists
**When** the listing domain is implemented
**Then** Maison can store a rental Listing linked to exactly one Commissionnaire Profile
**And** the Listing stores monthly USD price, Commune, bedroom count, description, Availability Status, submission timestamp, and last update timestamp.

**Given** listing media is implemented
**When** photos are attached to a Listing
**Then** Maison stores ListingPhoto records through local media storage
**And** uploaded files are validated as usable images before being accepted.

**Given** a Listing has multiple photos
**When** the Listing is rendered later on card or detail surfaces
**Then** one primary photo can be identified
**And** photo ordering is deterministic.

**Given** a developer validates the domain foundation
**When** model and service tests run
**Then** they verify Commissionnaire ownership, required Listing fields, image validation behavior, and valid Availability Status values.

### Story 2.2: Public Browse With Listing Cards

As a Tenant,
I want to browse recent available rental Listings through fast-scan cards,
So that I can quickly identify homes worth opening in detail.

**Requirements:** FR-1; NFR-1, NFR-2; UX-DR7, UX-DR10, UX-DR11, UX-DR23, UX-DR33.

**Acceptance Criteria:**

**Given** Listings exist with different Availability Status values
**When** a Tenant opens the public browse surface
**Then** Maison displays only Listings with Availability Status `available`
**And** Listings are ordered by recency.

**Given** an available Listing appears in browse results
**When** its Listing Card is rendered
**Then** the card displays monthly price, Commune, bedroom count, primary photo, freshness/last update, and Verification Badge only when applicable
**And** the card does not imply unverified Listings are verified.

**Given** a Tenant interacts with a Listing Card
**When** they tap or click the card body
**Then** Maison opens the Listing Detail route or surface for that Listing
**And** any independent card actions remain separate from card navigation.

**Given** browse is displayed on mobile, tablet, and desktop
**When** the layout responds
**Then** it uses one-column, two-column, and three-column Listing layouts at the defined breakpoints
**And** all card controls meet the 44px touch-target and visible-focus requirements.

### Story 2.3: Search Filters And Empty States

As a Tenant,
I want to filter rental Listings by Commune, budget, and bedrooms,
So that I can narrow the marketplace to homes that fit my search.

**Requirements:** FR-2; NFR-1, NFR-2; UX-DR7, UX-DR8, UX-DR9, UX-DR23.

**Acceptance Criteria:**

**Given** available Listings exist across multiple Communes, budgets, and bedroom counts
**When** a Tenant applies Commune, monthly budget, and bedroom filters
**Then** Maison returns only Listings satisfying every active filter
**And** unavailable or under-review Listings remain excluded.

**Given** filters are active
**When** the Tenant removes one filter or clears all filters
**Then** the results update accordingly
**And** the chosen values are preserved correctly across refresh or enhanced updates.

**Given** filtering is enhanced with JavaScript
**When** results refresh
**Then** Maison shows listing-shaped skeletons rather than a full-page spinner
**And** result-count updates are announced through a live region.

**Given** no Listing matches active filters
**When** results render
**Then** Maison displays the empty state `Aucune annonce ne correspond exactement.`
**And** provides one clear reset action.

**Given** a developer validates search behavior
**When** query and view tests run
**Then** they cover combined filters, filter removal, empty results, and performance-sensitive query shape under MVP expectations.

### Story 2.4: Listing Detail Surface

As a Tenant,
I want to review a Listing's full details, photos, availability, and Commissionnaire identity,
So that I can decide whether it is worth contacting someone about that home.

**Requirements:** FR-3, FR-14; NFR-1; UX-DR12, UX-DR13, UX-DR14, UX-DR15, UX-DR16, UX-DR18, UX-DR33.

**Acceptance Criteria:**

**Given** an available Listing exists
**When** a Tenant opens its detail surface
**Then** Maison displays all Listing Card fields plus media gallery, description, Availability Status, last update time, and Commissionnaire Profile identity
**And** the WhatsApp Contact Action is visible only while Availability Status is `available`.

**Given** a Listing has photos
**When** the gallery renders
**Then** Maison shows a 4:3 main image, deterministic thumbnails, image count, rounded image corners, and meaningful alt text where available.

**Given** the Listing is unverified
**When** detail renders
**Then** Maison does not show a Verification Badge or Verification Box
**And** the copy does not imply Maison guarantees availability or transaction outcome.

**Given** the Listing is opened on desktop
**When** the detail surface appears
**Then** it renders as a right-side drawer preserving browse context behind a scrim
**And** focus is trapped, Escape closes the drawer, closed content is inert, and focus returns to the triggering card.

**Given** the Listing is opened on mobile
**When** the detail surface appears
**Then** it renders as a full-screen detail surface with familiar back behavior and sticky bottom CTA when valid
**And** controls meet mobile touch-target and visible-focus requirements.

### Story 2.5: Commissionnaire Listing Submission

As a Commissionnaire,
I want to submit a rental Listing from my phone,
So that I can contribute useful inventory without a heavy administrative process.

**Requirements:** FR-5; NFR-1, NFR-3; UX-DR24, UX-DR26, UX-DR27, UX-DR35, UX-DR36.

**Acceptance Criteria:**

**Given** a signed-in Commissionnaire has a valid Commissionnaire Profile
**When** they open the publication flow
**Then** Maison presents a mobile-friendly form or stepper for monthly price, Commune, bedroom count, description, Availability Status, and photos
**And** the flow uses visible labels, concise French copy, and 44px touch targets.

**Given** the Commissionnaire submits the required Listing fields and at least three usable real photos
**When** the submission is processed
**Then** Maison stores the Listing with submission time and last update time
**And** associates it with exactly one Commissionnaire Profile.

**Given** required fields are missing
**When** the form is submitted
**Then** Maison blocks submission
**And** identifies the exact fields to correct.

**Given** uploaded media is unsupported or unusable
**When** validation runs
**Then** Maison rejects the affected media
**And** explains what the Commissionnaire must correct without accepting the invalid photo.

**Given** a user without a valid Commissionnaire Profile attempts publication
**When** the request is processed
**Then** Maison denies or redirects server-side to the required profile setup
**And** no Listing is created.

### Story 2.6: Listing Preview And Submission Validation

As a Commissionnaire,
I want to preview my Listing before submission,
So that I can catch missing or misleading information before it enters moderation or public inventory.

**Requirements:** FR-5; UX-DR10, UX-DR24, UX-DR27, UX-DR34.

**Acceptance Criteria:**

**Given** a Commissionnaire has entered draft Listing information
**When** they open the preview step
**Then** Maison renders a preview of the future Listing Card using the current price, Commune, bedroom count, primary photo, and availability/freshness display
**And** the preview never shows a Verification Badge before moderation.

**Given** the draft Listing lacks required publication data
**When** the Commissionnaire attempts final submission
**Then** Maison blocks submission
**And** shows precise correction guidance for missing fields, insufficient photos, or unusable media.

**Given** the draft Listing meets the publication standard
**When** the Commissionnaire submits it
**Then** Maison moves it into the correct initial moderation or publication state defined for MVP
**And** shows a confirmation explaining the next operational state.

**Given** publication flow states render on mobile
**When** the Commissionnaire moves between entry, preview, correction, and confirmation
**Then** Maison preserves entered values
**And** avoids full-page spinners, oversized dashboard cards, or decorative UI that slows the task.

### Story 2.7: Availability Management And Freshness

As a Commissionnaire,
I want to update and reconfirm Listing availability,
So that Tenants do not waste time contacting me about homes that are no longer available.

**Requirements:** FR-6, FR-3; NFR-4; UX-DR16, UX-DR24, UX-DR38, UX-DR39.

**Acceptance Criteria:**

**Given** a Commissionnaire owns a Listing
**When** they update its Availability Status
**Then** Maison allows valid transitions such as `available` and `unavailable`
**And** records the status-change timestamp and actor.

**Given** a Listing is marked `unavailable`
**When** public browse, filter, and detail surfaces render
**Then** the Listing disappears from search results
**And** its detail surface no longer exposes the WhatsApp Contact Action.

**Given** a Listing is still available but reaches the freshness threshold
**When** the Commissionnaire views their inventory
**Then** Maison shows a reconfirmation prompt with a clear status cue and action
**And** reconfirming updates the freshness timestamp.

**Given** availability changes occur
**When** audit behavior is inspected
**Then** Maison retains append-only audit history for each change
**And** the public UI shows last update/freshness without implying real-time guaranteed availability.

**Given** a Commissionnaire attempts to change a Listing they do not own
**When** the request is processed
**Then** Maison denies the action server-side
**And** does not expose private Listing or Commissionnaire data.

## Epic 3: Traceable WhatsApp Lead Conversion

Tenants can identify themselves, consent, create an attributable Lead, and reach the right Commissionnaire through WhatsApp; Commissionnaires can view attributed demand.

### Story 3.1: Lightweight Identification And Consent

As a Tenant,
I want to provide the minimum identity information and consent before contacting a Commissionnaire,
So that Maison can create an attributable enquiry without forcing a heavy account journey.

**Requirements:** FR-7; NFR-3; UX-DR20, UX-DR22, UX-DR32, UX-DR34.

**Acceptance Criteria:**

**Given** a signed-in Tenant opens the WhatsApp Contact Action for an available Listing
**When** Lightweight Identification is required
**Then** Maison presents a modal, sheet, or page that collects the required Tenant identity fields
**And** explains that the information is used to connect the Tenant with the Commissionnaire and attribute the enquiry.

**Given** Lightweight Identification is displayed
**When** the Tenant reviews the form
**Then** Maison requires explicit consent before continuing
**And** includes the privacy reassurance `Maison ne lit pas vos conversations WhatsApp.`

**Given** required identity fields or consent are missing
**When** the Tenant attempts to continue
**Then** Maison blocks progression
**And** shows field-level French error copy without opening WhatsApp.

**Given** the identification UI appears on mobile or desktop
**When** a keyboard, touch, or screen-reader user interacts with it
**Then** controls have visible labels, visible focus, 44px touch targets, and accessible error feedback
**And** the CTA exposes loading and disabled states for later Lead creation.

### Story 3.2: Attributable Lead Creation

As Maison,
I want to create a Lead before any WhatsApp handoff,
So that tenant intent is attributable to the selected Listing and Commissionnaire.

**Requirements:** FR-8; NFR-2, NFR-3, NFR-5; UX-DR20, UX-DR21, UX-DR22.

**Acceptance Criteria:**

**Given** a Tenant has completed Lightweight Identification with consent
**When** they confirm the WhatsApp Contact Action for an available Listing
**Then** Maison creates a Lead before opening or returning any WhatsApp URL
**And** the Lead records Tenant identifier, Listing, Commissionnaire Profile, creation timestamp, and acquisition context available to Maison.

**Given** the same Tenant contacts the same Listing more than once
**When** each contact attempt is confirmed
**Then** Maison preserves distinguishable event history
**And** repeated attempts do not overwrite the original Lead provenance.

**Given** the selected Listing is no longer available before Lead creation
**When** the contact action is processed
**Then** Maison does not create a handoff-ready Lead
**And** shows a recoverable state explaining that the Listing is unavailable.

**Given** Lead creation is implemented
**When** tests run
**Then** they verify Lead ownership, Listing-to-Commissionnaire provenance, consent presence, timestamp creation, and the invariant that Lead creation precedes WhatsApp URL generation.

### Story 3.3: WhatsApp Handoff With Listing Context

As a Tenant,
I want Maison to open WhatsApp with the right Commissionnaire and Listing context,
So that the conversation starts clearly and the Commissionnaire can identify my enquiry.

**Requirements:** FR-9; NFR-5; UX-DR18, UX-DR22, UX-DR34, UX-DR38.

**Acceptance Criteria:**

**Given** a Lead has been created successfully
**When** Maison prepares the WhatsApp Handoff
**Then** the handoff targets the WhatsApp phone number associated with the Listing's Commissionnaire Profile
**And** the generated message includes a Listing identifier and a human-readable Lead reference.

**Given** a Tenant confirms contact
**When** the handoff succeeds
**Then** Maison opens or returns the WhatsApp deep link only after Lead creation
**And** records a handoff-attempt event separately from the Lead record.

**Given** the handoff message is rendered
**When** its text is inspected
**Then** it does not claim Maison can track WhatsApp conversation contents, visits, negotiation, payment, or contract execution
**And** it stays concise enough for a practical WhatsApp opening message.

**Given** a developer validates the handoff service
**When** tests run
**Then** they verify correct Commissionnaire phone targeting, Listing reference, Lead reference, URL encoding, and no handoff URL when Lead creation has failed.

### Story 3.4: Recoverable Handoff Failure States

As a Tenant,
I want clear recovery options when Lead creation or WhatsApp opening fails,
So that my intent is not lost and I understand what happened.

**Requirements:** FR-7, FR-8, FR-9; NFR-2, NFR-5; UX-DR21, UX-DR22, UX-DR32, UX-DR34.

**Acceptance Criteria:**

**Given** Lead creation fails
**When** the Tenant confirms contact
**Then** Maison keeps the identification flow open
**And** preserves entered values, shows a recoverable French error, offers retry, and does not open WhatsApp.

**Given** Lead creation succeeds but WhatsApp opening fails
**When** the Tenant remains on Maison
**Then** Maison explains that the Lead exists
**And** provides a retry action or fallback link for the WhatsApp handoff.

**Given** the contact CTA is processing
**When** the Lead or handoff request is in progress
**Then** Maison disables duplicate submission
**And** shows a localized loading state near the action rather than a full-page spinner.

**Given** failure states are rendered
**When** they are tested for accessibility
**Then** errors are announced through appropriate semantics or live-region behavior
**And** color is not the only signal for error, warning, or success.

### Story 3.5: Commissionnaire Lead Inbox

As a Commissionnaire,
I want to view Leads attributed to my Listings,
So that I can understand and respond to tenant demand generated by Maison.

**Requirements:** FR-10; NFR-3; UX-DR25, UX-DR26, UX-DR38.

**Acceptance Criteria:**

**Given** a signed-in Commissionnaire has attributed Leads
**When** they open their Lead view
**Then** Maison shows only Leads associated with their own Commissionnaire Profile
**And** each Lead row identifies the originating Listing and creation timestamp.

**Given** a Lead row is rendered
**When** the Commissionnaire reviews it
**Then** the row shows tenant identity fields permitted by the Lead consent and marketplace purpose
**And** does not show or imply access to WhatsApp conversation contents.

**Given** a Commissionnaire has no Leads
**When** they open the Lead view
**Then** Maison shows a useful empty state
**And** avoids oversized hero metrics or nested dashboard cards.

**Given** a Commissionnaire attempts to access another Commissionnaire's Lead
**When** the request is processed
**Then** Maison denies access server-side
**And** does not expose private Lead, Tenant, Listing, or Commissionnaire data.

### Story 3.6: Lead Status Updates

As a Commissionnaire,
I want to update simple Lead statuses,
So that I can track response discipline without Maison reading WhatsApp conversations.

**Requirements:** FR-10; NFR-4; UX-DR25, UX-DR37, UX-DR38.

**Acceptance Criteria:**

**Given** a Commissionnaire has a Lead attributed to their profile
**When** the Lead is created
**Then** Maison assigns the initial status `new`
**And** records the Lead creation timestamp.

**Given** the Commissionnaire updates a Lead status
**When** they choose a valid status such as `contacted` or `closed`
**Then** Maison saves the new status
**And** records the status-change timestamp and actor.

**Given** the Commissionnaire Lead view displays status
**When** Leads are rendered
**Then** Maison shows status labels with text plus visual cues
**And** does not imply the status came from reading WhatsApp conversation content.

**Given** a Commissionnaire attempts to update a Lead they do not own
**When** the request is processed
**Then** Maison denies the action server-side
**And** leaves the Lead status unchanged.

**Given** response-discipline instrumentation is inspected
**When** Lead status changes occur
**Then** Maison can measure percentage moved to `contacted` and time from Lead creation to that change
**And** the measurement uses Maison-owned status events only.

## Epic 4: Moderation, Verification, and Marketplace Trust

Moderators can control publication quality, apply selective Verification, handle Reports, and expose defensible trust signals without overpromising.

### Story 4.1: Moderator Access And Queue

As a Moderator,
I want a protected queue of submitted Listings,
So that I can review marketplace inventory before it becomes or remains visible.

**Requirements:** FR-11; NFR-3, NFR-4; UX-DR28, UX-DR30, UX-DR32.

**Acceptance Criteria:**

**Given** a signed-in user has Moderator permissions
**When** they open the moderation queue
**Then** Maison displays submitted Listings awaiting review
**And** each queue item shows age, Commissionnaire identity, Listing summary, media count, and current moderation state.

**Given** a signed-in user does not have Moderator permissions
**When** they attempt to access moderation surfaces
**Then** Maison denies access server-side
**And** does not expose Listing submissions, private Commissionnaire data, or moderation notes.

**Given** the moderation queue contains no pending Listings
**When** a Moderator opens it
**Then** Maison shows a compact empty state
**And** provides a route back to valid Moderator surfaces without decorative dashboard clutter.

**Given** the moderation queue renders on mobile and desktop
**When** a Moderator reviews the page
**Then** rows remain scannable, controls have visible labels and focus states, and status is communicated with text plus visual cues.

### Story 4.2: Listing Moderation Decisions

As a Moderator,
I want to publish, request correction, reject, or remove Listings,
So that Maison can enforce publication quality without claiming every Listing is verified.

**Requirements:** FR-11; NFR-4; UX-DR28, UX-DR34, UX-DR38.

**Acceptance Criteria:**

**Given** a Moderator opens a submitted Listing
**When** the required information and media are reviewed
**Then** Maison allows the Moderator to publish, request correction, reject, or remove the Listing
**And** each action requires any reason or correction detail needed for downstream clarity.

**Given** a Moderator publishes a Listing without Verification
**When** the Listing becomes visible
**Then** Maison includes it in public search only if it is otherwise `available`
**And** does not display a Verification Badge.

**Given** a Moderator requests correction or rejects a Listing
**When** the action is saved
**Then** Maison records the resulting moderation state
**And** the Listing does not appear as an available public Listing.

**Given** a Moderator removes an already visible Listing
**When** the action is saved
**Then** Maison removes it from search results
**And** hides the WhatsApp Contact Action on its detail surface.

**Given** any moderation action is taken
**When** audit history is inspected
**Then** Maison records actor, timestamp, action, target Listing, resulting state, and reason or metadata where applicable.

### Story 4.3: Selective Verification Checklist

As a Moderator,
I want to apply a Verification Badge only after completing a checklist,
So that Maison's trust signal stays specific, defensible, and reversible.

**Requirements:** FR-12, FR-14; NFR-4; UX-DR11, UX-DR17, UX-DR28, UX-DR29, UX-DR38.

**Acceptance Criteria:**

**Given** a Moderator reviews a Listing for Verification
**When** the Verification Checklist is displayed
**Then** Maison shows explicit checklist items for required-field review, media review, Commissionnaire contact confirmation, and the additional operational evidence check
**And** each item has a clear checked state and text label.

**Given** not all checklist items are complete
**When** the Moderator attempts to apply Verification
**Then** Maison blocks badge application
**And** explains which checklist items remain incomplete.

**Given** all checklist items are complete
**When** the Moderator applies Verification
**Then** Maison marks only that specific Listing as verified
**And** records actor, timestamp, checklist state, and resulting verified state.

**Given** a Moderator removes Verification
**When** the action is saved
**Then** Maison removes the verified state immediately
**And** records actor, timestamp, and reason or metadata.

**Given** public Listing surfaces render a verified Listing
**When** the badge appears
**Then** Maison shows `Annonce vérifiée` with icon plus text
**And** the detail page uses the canonical copy: `Cette annonce a passé un contrôle supplémentaire. Le badge ne garantit pas le résultat d'une transaction hors ligne.`

### Story 4.4: Tenant Report Submission

As a Tenant,
I want to report a suspicious, misleading, or stale Listing,
So that Maison can review trust problems surfaced by users.

**Requirements:** FR-13; NFR-3; UX-DR19, UX-DR23, UX-DR32, UX-DR34.

**Acceptance Criteria:**

**Given** a Tenant is viewing a Listing Detail Page
**When** they open the Report Action
**Then** Maison presents a reason selection and optional notes field
**And** the action remains visually secondary to the main WhatsApp CTA.

**Given** the Tenant submits a Report with a reason
**When** the submission succeeds
**Then** Maison creates a Report linked to the Listing and associated Commissionnaire Profile
**And** confirms receipt without exposing internal moderation details.

**Given** the Tenant submits a Report without a required reason
**When** validation runs
**Then** Maison blocks submission
**And** shows field-level French error copy.

**Given** the Report form is displayed
**When** a keyboard, touch, or screen-reader user interacts with it
**Then** labels, focus handling, touch targets, and error feedback meet the accessibility floor
**And** status is never communicated by color alone.

**Given** Report submission is implemented
**When** tests run
**Then** they verify Listing and Commissionnaire provenance, required reason validation, optional notes handling, and receipt confirmation behavior.

### Story 4.5: Report Review And Resolution

As a Moderator,
I want to review and resolve Tenant Reports,
So that Maison can act on suspicious, misleading, or stale inventory signals.

**Requirements:** FR-13, FR-11; NFR-3, NFR-4; UX-DR28, UX-DR38.

**Acceptance Criteria:**

**Given** Reports have been submitted
**When** a Moderator opens the Report queue
**Then** Maison displays open Reports with reason, optional notes, associated Listing, associated Commissionnaire Profile, and report age
**And** access is restricted server-side to Moderator users.

**Given** a Moderator reviews a Report
**When** they resolve it
**Then** Maison records the outcome, actor, timestamp, and any internal resolution notes
**And** sensitive moderation notes do not appear on public Listing Detail Pages.

**Given** a Report requires Listing action
**When** the Moderator removes, rejects, requests correction, or otherwise changes the Listing state
**Then** Maison updates the Listing according to moderation rules
**And** records the related audit event.

**Given** a Report has been resolved
**When** the queue is refreshed
**Then** the Report no longer appears as open
**And** the resolution remains available in moderation history.

**Given** report metrics are inspected
**When** Reports are submitted and resolved
**Then** Maison can measure report rate and median time to Moderator resolution
**And** the metric does not expose private report notes publicly.

### Story 4.6: Public Trust Signals

As a Tenant,
I want to distinguish normal publication information from stronger Verification signals,
So that I can judge Listings without being misled by overbroad trust claims.

**Requirements:** FR-14, FR-12; UX-DR11, UX-DR16, UX-DR17, UX-DR23, UX-DR34, UX-DR38, UX-DR39.

**Acceptance Criteria:**

**Given** a Listing is verified
**When** it appears on Listing Cards and Detail Pages
**Then** Maison displays the Verification Badge consistently with text plus icon
**And** the detail page shows the canonical narrow explanation of what verification means.

**Given** a Listing is not verified
**When** it appears on public surfaces
**Then** Maison never displays the Verification Badge or Verification Box
**And** the UI does not substitute vague trust language that implies verification.

**Given** a Listing Detail Page renders
**When** Tenant-facing trust signals appear
**Then** Maison shows last update time and availability state clearly
**And** does not imply real-time availability or guaranteed transaction success.

**Given** public view count remains in MVP
**When** it is displayed
**Then** Maison treats it as a secondary activity signal
**And** does not imply popularity equals credibility.

**Given** trust copy is reviewed
**When** visible Listing, Verification, freshness, Report, and WhatsApp copy are inspected
**Then** Maison avoids claims that every Listing is verified, that the badge guarantees offline outcomes, or that Maison reads WhatsApp conversations.

### Story 4.7: Launch Shell And Marketplace Instrumentation

As the Maison product team,
I want the launch product shell and key marketplace events instrumented,
So that users get a consistent navigation experience and the team can validate discovery, freshness, trust, and lead conversion.

**Requirements:** FR-1, FR-2, FR-3, FR-6, FR-8, FR-9, FR-10, FR-13, FR-14; UX-DR6, UX-DR31, UX-DR37.

**Acceptance Criteria:**

**Given** public and authenticated surfaces render
**When** Maison displays navigation
**Then** desktop shows the compact mark, wordmark, tenant navigation, `Espace pro`, and `Publier un bien`
**And** mobile shows visible bottom-navigation labels for `Explorer`, `Favoris`, and `Espace pro`.

**Given** interactive UI transitions are implemented
**When** drawers, modals, hover, pressed, and loading states appear
**Then** Maison uses 150-250ms motion based on transform/opacity where possible
**And** respects reduced-motion preferences without losing comprehension.

**Given** launch instrumentation is enabled
**When** users browse, filter, open detail, tap WhatsApp CTA, submit identification, create Leads, attempt handoff, report Listings, change availability, reconfirm Listings, or update Lead status
**Then** Maison records those events with enough context to measure the MVP success metrics
**And** no event claims access to WhatsApp conversation contents.
