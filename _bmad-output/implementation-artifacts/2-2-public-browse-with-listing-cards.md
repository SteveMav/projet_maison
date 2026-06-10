---
baseline_commit: 83de0f8f0b1584d8b991f06922f9a3af5385d75b
---

# Story 2.2: Public Browse With Listing Cards

Status: review

<!-- Validation: created from bmad-create-story workflow on 2026-06-06. -->

## Story

As a Tenant,
I want to browse recent available rental Listings through fast-scan cards,
so that I can quickly identify homes worth opening in detail.

## Acceptance Criteria

1. Given Listings exist with different Availability Status values, when a Tenant opens the public browse surface, then Maison displays only Listings with Availability Status `available` and Listings are ordered by recency.
2. Given an available Listing appears in browse results, when its Listing Card is rendered, then the card displays monthly price, Commune, bedroom count, primary photo, freshness/last update, and Verification Badge only when applicable and the card does not imply unverified Listings are verified.
3. Given a Tenant interacts with a Listing Card, when they tap or click the card body, then Maison opens the Listing Detail route or surface for that Listing and any independent card actions remain separate from card navigation.
4. Given browse is displayed on mobile, tablet, and desktop, when the layout responds, then it uses one-column, two-column, and three-column Listing layouts at the defined breakpoints and all card controls meet the 44px touch-target and visible-focus requirements.

## Tasks / Subtasks

- [x] Verify prerequisites and existing implementation state (AC: 1, 2, 3, 4)
  - [x] Confirm Stories 1.1 through 2.1 are implemented before coding this story.
  - [x] Confirm `Listing` exposes Availability Status values `available`, `unavailable`, and `under_review`.
  - [x] Confirm `ListingPhoto` exposes deterministic ordering and a primary-photo helper/selector from Story 2.1.
  - [x] Confirm Listing timestamps include `created_at`, `updated_at`, and `submitted_at`; use the existing fields rather than adding duplicates.
  - [x] Read existing `apps/listings`, `templates`, `static_src`, `static`, `config/urls.py`, base template, and existing tests before editing.
  - [x] If no Django implementation exists yet, implement prerequisite stories first rather than creating isolated browse templates.

- [x] Implement public browse selector/query shape (AC: 1, 2)
  - [x] Add or update `apps/listings/selectors.py`.
  - [x] Implement a selector such as `get_public_browse_listings()` that filters `Listing.availability_status == "available"` only.
  - [x] Exclude `under_review` and `unavailable` Listings from all public browse results.
  - [x] Order by a deterministic recency value, preferably `submitted_at` when present, then `updated_at`, then `id` descending.
  - [x] Use `select_related("commissionnaire_profile")` for owner/profile fields needed by card rendering.
  - [x] Use `prefetch_related()` or `Prefetch()` for photos so card rendering does not perform one query per Listing.
  - [x] Keep filter parameters for Commune, budget, and bedrooms out of this story; Story 2.3 owns combined search filters.
  - [x] Never treat `under_review` as a public fallback when no available Listings exist.

- [x] Add public browse route and view (AC: 1, 3)
  - [x] Add or update `apps/listings/views.py` with a public browse view.
  - [x] Add or update `apps/listings/urls.py` and include it from `config/urls.py`.
  - [x] Use stable route names such as `listings:browse` and `listings:detail`.
  - [x] Allow anonymous visitors to browse; do not require login or lightweight identification for browse.
  - [x] Paginate results with Django `Paginator` or `ListView.paginate_by`; do not render an unbounded Listing queryset.
  - [x] If the full detail surface from Story 2.4 does not exist, create only the minimal stable route/href contract needed for card navigation, without building the full detail drawer, report action, WhatsApp CTA, or gallery.
  - [x] Return a normal server-rendered HTML response; do not add a public REST/GraphQL API.

- [x] Build Listing Card template include (AC: 2, 3, 4)
  - [x] Add `templates/listings/includes/listing_card.html`.
  - [x] Render monthly USD price, Commune, bedroom count, primary photo, and freshness/last-update copy.
  - [x] Render a meaningful `alt` value for the primary photo using available Listing context.
  - [x] Use the primary photo helper from Story 2.1; fall back to the first ordered photo only through the shared selector/helper.
  - [x] If a data inconsistency leaves an available Listing without photos, render a neutral non-property placeholder or omit the Listing; never use AI-generated luxury/rental imagery as a silent substitute.
  - [x] Show a Verification Badge only when an explicit verified state already exists and is true.
  - [x] If no verification model/field exists yet, render no badge and do not add verification persistence in this story.
  - [x] Use text plus icon for verified state where available; never communicate verification through color alone.
  - [x] Do not include a vague trust label such as "trusted", "guaranteed", "checked", or "safe" for unverified Listings.
  - [x] Keep independent card actions outside the card body link to avoid nested interactive elements.
  - [x] Do not implement favorite persistence in this story. If a favorite action already exists, preserve it as an independent 44px control; otherwise omit it until the product explicitly owns favorites.

- [x] Build public browse template and responsive grid (AC: 1, 4)
  - [x] Add `templates/listings/browse.html`.
  - [x] Extend the existing `base.html`.
  - [x] Use compact French UI copy suitable for Tenant browsing.
  - [x] Render a default browse state with recent available Listings.
  - [x] Render a default empty state when no available Listings exist. Use distinct copy from the filtered empty-state copy reserved for Story 2.3.
  - [x] Use one-column Listing layout under `700px`.
  - [x] Use two-column Listing layout from `700px` through `920px`.
  - [x] Use three-column Listing layout above `920px`, with desktop content constrained around the established `1280px-1420px` range.
  - [x] Ensure each card has stable dimensions with image aspect ratio and does not shift layout when images load.
  - [x] Use 44px minimum touch targets and visible focus states for card links and any icon actions.
  - [x] Do not add the full filter panel, removable filter chips, filtered empty state, or live result-count announcements; Story 2.3 owns those.

- [x] Implement performance and media rendering controls (AC: 1, 2, 4)
  - [x] Keep page payload small through pagination and selective query fields where practical.
  - [x] Avoid loading original full-size images into oversized card slots when the existing media setup provides smaller derivatives. If derivatives do not exist yet, use CSS `aspect-ratio`, `object-fit: cover`, `loading="lazy"`, and explicit width/height attributes.
  - [x] Eager-load at most the first above-the-fold card image if useful; lazy-load the rest.
  - [x] Avoid full-page spinners. This story renders server HTML; Story 2.3 owns listing-shaped skeletons for filter refresh.
  - [x] Do not add Redis, external caching, image CDN, client-side rendering, or infinite scroll.

- [x] Add tests for selectors, views, templates, and accessibility basics (AC: 1, 2, 3, 4)
  - [x] Test anonymous users can load the browse page.
  - [x] Test available Listings appear.
  - [x] Test `unavailable` and `under_review` Listings do not appear.
  - [x] Test Listings are ordered by recency with deterministic tie-breaker.
  - [x] Test card HTML contains monthly price, Commune, bedroom count, primary photo, and last-update/freshness copy.
  - [x] Test unverified Listings do not render a Verification Badge.
  - [x] If verified state already exists, test verified Listings render text plus icon/accessible label.
  - [x] Test each card body links to the stable Listing detail route.
  - [x] Test independent card actions, if present, are not nested inside the card body link.
  - [x] Test the selector/view uses bounded pagination.
  - [x] Test query count stays bounded for a representative page of Listings with photos.
  - [x] Test the default no-available-listings empty state.
  - [x] Add template/CSS assertions for the responsive grid classes or selectors used for the `<700px`, `700px-920px`, and `>920px` ranges.

- [x] Run required checks (AC: 1, 2, 3, 4)
  - [x] `python manage.py check`
  - [x] `python manage.py test apps.listings`
  - [x] `python manage.py test`
  - [x] `npm run css:build`
  - [x] `python manage.py collectstatic --noinput --dry-run`

## Dev Notes

### Source Context

- Story source: `_bmad-output/planning-artifacts/epics.md`, Epic 2, Story 2.2.
- Requirements: FR-1; NFR-1, NFR-2; UX-DR7, UX-DR10, UX-DR11, UX-DR23, UX-DR33.
- FR-1 requires available rental Listings ordered by recency, Listing Cards with monthly price, Commune, bedroom count, primary photo, and Verification Badge when applicable, and card navigation to detail.
- NFR-1 requires mobile browser support without a native app.
- NFR-2 requires search results to become usable within 3 seconds on a typical mobile connection in Kinshasa under expected MVP load.
- Epic 2 goal: Commissionnaires publish and maintain useful rental inventory while Tenants browse, filter, and inspect available Listings.

### Dependency On Previous Stories

This story depends on the model/media foundation from Story 2.1.

Required Story 2.1 foundations:

- `Listing` model linked to `CommissionnaireProfile`.
- `Listing.availability_status` choices: `available`, `unavailable`, `under_review`.
- Monthly USD price stored as an integer amount, not a float.
- `commune`, `bedroom_count`, `description`, `submitted_at`, `created_at`, and `updated_at`.
- `ListingPhoto` model with local media storage.
- Deterministic photo ordering.
- Primary photo helper/selector or explicit `is_primary` behavior.
- Query indexes for availability, recency, Commune, bedroom count, and price.

If these are missing, implement Story 2.1 first. Do not duplicate Listing ownership, status choices, photo ordering, or primary-photo logic in templates.

### Previous Story Intelligence

- Story 2.1 intentionally kept public browse, filters, detail surfaces, publication UI, moderation, verification, Leads, Reports, and audit tables out of scope. This story adds public browse cards only.
- Story 2.1 recommends `availability_status` defaulting to `under_review`; public browse must therefore filter explicitly to `available`.
- Story 2.1 recommends a `monthly_price_amount` plus `monthly_price_currency`; card rendering should use the implemented money fields and never assume floats.
- Story 2.1 recommends `availability_changed_at` as optional. For freshness display, prefer `availability_changed_at` when implemented, otherwise `updated_at`.
- Story 2.1 states the real-property-photo trust requirement cannot be fully automated. Browse cards should use persisted Listing photos and never silently replace them with generated aspirational property imagery.
- Story 1.5 established that Listing attribution belongs to `CommissionnaireProfile`. Browse cards may show only the card fields required here; detail identity belongs mostly to Story 2.4.

### Architecture Compliance

- Use Django 5.2 LTS server-rendered views and templates.
- Use Django selectors for read/query logic.
- Keep business logic out of templates.
- Use small template includes for repeated UI, especially Listing Cards.
- Use Tailwind CLI/static CSS output already established by Story 1.1.
- Use modular JavaScript only for progressive enhancement; no inline JavaScript for business behavior.
- Keep public marketplace logic inside `apps/listings`.
- Do not create public `/api/` endpoints.
- Do not add React, Vue, a SPA router, DRF, Redis, PostgreSQL, or an external cache.

### Query And Pagination Guardrails

Recommended selector shape:

```python
from django.db.models import F, Prefetch
from django.db.models.functions import Coalesce

from apps.listings.models import Listing, ListingPhoto


def get_public_browse_listings():
    ordered_photos = ListingPhoto.objects.order_by("-is_primary", "position", "id")

    return (
        Listing.objects.filter(
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
        )
        .select_related("commissionnaire_profile")
        .prefetch_related(Prefetch("photos", queryset=ordered_photos))
        .annotate(recency_at=Coalesce("submitted_at", "updated_at", "created_at"))
        .order_by("-recency_at", "-id")
    )
```

Adapt field names to the actual Story 2.1 implementation. Keep the invariant: only `available` Listings, deterministic recency, bounded page size, no N+1 photo/profile queries.

Recommended pagination:

- Use `ListView.paginate_by` or `Paginator`.
- Start with 12 cards per page unless the implemented design has a better page size.
- Keep previous/next controls accessible and keyboard reachable.
- Avoid infinite scroll for MVP.

### Card Rendering Guardrails

Required card fields:

- primary photo
- monthly USD price
- Commune
- bedroom count
- freshness/last-update copy
- Verification Badge only when explicit verified state exists and is true

Optional fields:

- neighborhood, property type, bathroom count, view count, and favorite action only if already implemented by previous work. Do not add new persistence or fields here.

Suggested French copy:

- `Annonces récentes`
- `Mis à jour le ...`
- `Disponible`
- `Voir l'annonce`
- `Aucune annonce disponible pour le moment.`
- `Vérifiée` only when explicit verified state is true

Trust copy boundaries:

- Do not say `garantie`, `sûre`, `confirmée`, `contrôlée`, or equivalent broad trust language for ordinary Listings.
- Do not imply Maison guarantees real-time availability.
- Do not show a Verification Badge for unverified Listings.
- Verification, when present later, must use text plus icon and detail explanation from later trust-signal stories.

### Responsive And Accessibility Guardrails

Use the UX-DR33 breakpoints exactly:

- `<700px`: one-column listings and mobile-first spacing.
- `700px-920px`: two-column listings and compact navigation.
- `>920px`: three-column listings, desktop header, and constrained desktop content.

Card accessibility:

- The card body link must have a clear accessible label such as `Voir l'annonce a Ngaliema, 2 chambres`.
- Any icon-only control needs an accessible name and 44px minimum target.
- Do not nest `<button>` inside `<a>` or `<a>` inside `<a>`.
- Use visible focus styles for card link and independent controls.
- Use stable card image dimensions to prevent layout shift.
- Use meaningful alt text for real property photos; if the photo is decorative in a later variant, use empty alt only with an adjacent textual equivalent.

### Scope Boundaries

Implement now:

- Public browse route/view.
- Available-only selector.
- Paginated server-rendered Listing grid.
- Listing Card include.
- Stable card link to detail route/surface.
- Responsive one/two/three-column card layout.
- No-available-listings default empty state.
- Tests for status filtering, recency, card fields, badge absence for unverified Listings, navigation href, pagination, and query shape.

Do not implement now:

- Commune/budget/bedroom filter behavior, filter chips, filtered empty state, or live result count. Story 2.3 owns this.
- Full Listing Detail drawer/screen, gallery, WhatsApp CTA, report action, or focus-trapped overlay. Story 2.4 owns this.
- Commissionnaire publication, preview, submission validation, or availability management.
- Verification state model, Verification Checklist, moderation queue, Reports, Leads, WhatsApp handoff, audit event tables, favorites persistence, or view counts.
- Full-page spinners, infinite scroll, SPA rendering, or external caching.

### File Structure Requirements

Expected files to create or update, assuming the prerequisite Django scaffold exists:

```text
apps/listings/
├── selectors.py
├── views.py
├── urls.py
└── tests/
    ├── test_selectors.py
    ├── test_views.py
    └── test_templates.py
templates/listings/
├── browse.html
└── includes/
    └── listing_card.html
static_src/
└── css/input.css          # only if responsive utility additions are required
config/
└── urls.py
```

Read existing files before editing. Preserve app registration, base template blocks, static asset pipeline, auth routes, phone gate, and any implemented Listing model API from Story 2.1.

### Testing Requirements

Minimum tests:

- Selector:
  - filters only `available` Listings
  - excludes `unavailable`
  - excludes `under_review`
  - orders by recency deterministically
  - keeps query count bounded with photos/profile data
- View:
  - anonymous browse returns 200
  - uses expected template
  - paginates results
  - exposes only available Listings in context
  - displays default empty state when no available Listings exist
- Template/card:
  - shows monthly price, Commune, bedroom count, primary photo, and freshness copy
  - unverified Listing has no Verification Badge
  - verified badge renders only if an explicit verified state already exists
  - card body href targets the Listing detail route/surface
  - independent actions, if present, are outside the card body link
  - responsive grid classes/selectors match the defined breakpoints

Use Django's built-in test client and test runner. Browser automation is optional only if the implemented project already uses it; this story can be validated with Django tests plus CSS/template assertions.

### Latest Technical Notes

- Django 5.2 `Paginator` can paginate a `QuerySet` and lets the page use efficient `count()` behavior where available.
- Django 5.2 `ListView.paginate_by` automatically adds `paginator` and `page_obj` context for templates.
- Django 5.2 `select_related()` fetches single-valued FK/O2O relations in the same query; use it for `commissionnaire_profile` when card rendering touches profile data.
- Django 5.2 `prefetch_related()` fetches multi-valued relations in separate batched queries; use it for Listing photos.
- Django's `{% include %}` tag renders small subtemplates with current or explicitly provided context; use it for `listing_card.html`.
- Django's test client can request project URLs without a running server, which is sufficient for browse route tests.

### Anti-Patterns To Avoid

- Showing `under_review` or `unavailable` Listings in public browse.
- Ordering by non-deterministic database default order.
- Rendering all Listings without pagination.
- Querying photos or profiles once per card.
- Showing a Verification Badge without an explicit verified state.
- Adding a verification model or moderation workflow in this story.
- Using fake or AI-generated property photos as silent fallback media.
- Nesting interactive controls inside the card link.
- Adding filter logic that belongs to Story 2.3.
- Building full detail drawer/screen behavior that belongs to Story 2.4.
- Claiming availability is guaranteed or real-time.

### References

- `_bmad-output/planning-artifacts/epics.md#Story-2.2-Public-Browse-With-Listing-Cards`
- `_bmad-output/planning-artifacts/epics.md#Epic-2-Rental-Inventory-Marketplace`
- `_bmad-output/planning-artifacts/prds/prd-maison-2026-05-31/prd.md#FR-1-Browse-rental-Listings`
- `_bmad-output/planning-artifacts/prds/prd-maison-2026-05-31/prd.md#NFR-1-Mobile-usability`
- `_bmad-output/planning-artifacts/prds/prd-maison-2026-05-31/prd.md#NFR-2-Performance`
- `_bmad-output/planning-artifacts/architecture.md#Core-Architectural-Decisions`
- `_bmad-output/planning-artifacts/architecture.md#Implementation-Patterns-and-Consistency-Rules`
- `_bmad-output/planning-artifacts/architecture.md#Project-Structure`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/DESIGN.md#Listing-Card`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/EXPERIENCE.md#Tenant-Discovery`
- `_bmad-output/implementation-artifacts/2-1-listing-domain-model-and-media-foundation.md`
- `https://docs.djangoproject.com/en/5.2/topics/pagination/`
- `https://docs.djangoproject.com/en/5.2/ref/models/querysets/`
- `https://docs.djangoproject.com/en/5.2/ref/templates/builtins/#include`
- `https://docs.djangoproject.com/en/5.2/topics/testing/tools/`

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- Story created from BMAD epics, PRD, architecture, UX artifacts, previous Story 2.1 context, and Django 5.2 documentation.
- No implemented Django code was present in the repository during story creation.
- 2026-06-07: Started implementation from baseline commit `83de0f8f0b1584d8b991f06922f9a3af5385d75b`; confirmed Stories 1.1-2.1 are implemented, read listings/templates/static/URL/test context, and `python manage.py test apps.listings` passed with 36 tests before Story 2.2 edits.
- 2026-06-07: Selector RED failed on missing `get_public_browse_listings`; GREEN added available-only selector, deterministic recency ordering, profile `select_related`, photo `Prefetch`, and prefetched primary-photo helper. `python manage.py test apps.listings.tests.test_selectors`, `python manage.py test apps.listings`, and `python manage.py test` passed.
- 2026-06-07: View RED failed on missing `listings` namespace; GREEN added `PublicBrowseView`, `listings:browse`, `listings:detail`, root URL include, pagination, anonymous browse, and a minimal detail route contract. `python manage.py test apps.listings.tests.test_views`, `python manage.py test apps.listings`, `python manage.py check`, and `python manage.py test` passed.
- 2026-06-07: Card RED failed on missing required card fields/accessibility label; GREEN added `listing_card.html`, primary-photo card context, no-photo placeholder, detail link, badge suppression for unverified listings, and template tests. `python manage.py test apps.listings.tests.test_templates`, `python manage.py test apps.listings`, `python manage.py check`, and rerun `python manage.py test` passed with 141 tests.
- 2026-06-08: Layout RED failed on missing browse shell/pagination/CSS grid rules; GREEN added full-width browse shell, accessible pagination, responsive 1/2/3-column grid, stable media aspect ratio, and 44px targets. `python manage.py test apps.listings.tests.test_templates`, `python manage.py test apps.listings`, `python manage.py check`, `npm run css:build`, and `python manage.py test` passed with 144 tests.
- 2026-06-08: Performance/media guardrails added for bounded browse-page query count and card image loading controls; `python manage.py test apps.listings`, `python manage.py check`, and `python manage.py test` passed with 146 tests.
- 2026-06-08: Test coverage task completed across `apps/listings/tests/test_selectors.py`, `test_views.py`, and `test_templates.py`. Verified-state test is not applicable because no explicit verified field/model exists yet; unverified badge absence is covered.
- 2026-06-08: Required checks passed: `python manage.py check`, `python manage.py test apps.listings` (51 tests), `python manage.py test` (146 tests), `npm run css:build`, and `python manage.py collectstatic --noinput --dry-run`.
- 2026-06-08: Final Definition of Done gate passed: no unchecked task boxes remained and `python manage.py test` passed with 146 tests before moving Story 2.2 to `review`.
- 2026-06-08: Browser verification passed on `http://127.0.0.1:8001/annonces/`: CSS loaded, browse page rendered, empty state visible, no console errors, and mobile viewport had no horizontal overflow.

### Implementation Plan

- Use `get_public_browse_listings()` as the public read boundary for browse: available-only queryset, `Coalesce(submitted_at, updated_at, created_at)` recency, `-id` tie-breaker, profile join, and ordered prefetched photos exposed through `get_listing_primary_photo()`.
- Expose browse through `PublicBrowseView` with `paginate_by = 12`; keep detail to a minimal available-listing route contract until Story 2.4 owns the full detail surface.
- Prepare card-only display attributes in the view (`card_primary_photo`, `card_photo_alt`, `card_freshness_at`) from selector/model helpers, then keep `listing_card.html` declarative.
- Keep browse as an unframed page-level surface with card-level framing only; CSS media queries implement `<700px`, `700px+`, and `921px+` grid behavior.
- Keep media controls server-rendered: no spinner, no infinite scroll, explicit image dimensions, CSS cropping, first card eager load, and lazy loading for the remaining card images.

### Completion Notes List

- Story context generated with status `ready-for-dev`.
- Sprint status updated for Story 2.2.
- Verified Story 2.2 prerequisites and existing implementation state: Listing statuses, timestamps, deterministic photo ordering, primary-photo helper, and prior story implementation are present.
- Added public browse selector coverage and implementation for available-only results, deterministic recency ordering, and bounded profile/photo access.
- Added anonymous public browse routing and view pagination, plus a minimal stable detail route for card navigation without implementing Story 2.4 detail features.
- Added Listing Card include rendering price, commune, bedrooms, primary photo, freshness copy, stable detail link, neutral no-photo fallback, and no unverified badge.
- Added responsive browse layout, accessible pagination, default empty state, stable image/card dimensions, visible focus-compatible card links, and rebuilt static CSS.
- Added performance/media tests for bounded page queries, first-image eager loading, lazy loading for later images, and explicit card image dimensions.
- Completed selector/view/template/accessibility test coverage required by Story 2.2; conditional verified-state and independent-action cases remain no-op because those features do not exist in the implemented model/UI.
- Ran all required Story 2.2 validation commands successfully.
- Story 2.2 is complete and ready for review.
- Local browser smoke test passed; server left running at `http://127.0.0.1:8001/annonces/` for manual review.

### File List

- `apps/listings/tests/test_templates.py`
- `apps/listings/tests/test_views.py`
- `apps/listings/selectors.py`
- `apps/listings/tests/test_selectors.py`
- `apps/listings/urls.py`
- `apps/listings/views.py`
- `config/urls.py`
- `templates/base.html`
- `templates/listings/browse.html`
- `templates/listings/includes/listing_card.html`
- `static_src/css/input.css`
- `static/css/app.css`
- `_bmad-output/implementation-artifacts/2-2-public-browse-with-listing-cards.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`

### Change Log

- 2026-06-08: Implemented Story 2.2 public browse cards and moved story to review.
