---
baseline_commit: 83de0f8f0b1584d8b991f06922f9a3af5385d75b
---

# Story 2.3: Search Filters And Empty States

Status: review

<!-- Validation: created from bmad-create-story workflow on 2026-06-06. -->

## Story

As a Tenant,
I want to filter rental Listings by Commune, budget, and bedrooms,
so that I can narrow the marketplace to homes that fit my search.

## Acceptance Criteria

1. Given available Listings exist across multiple Communes, budgets, and bedroom counts, when a Tenant applies Commune, monthly budget, and bedroom filters, then Maison returns only Listings satisfying every active filter and unavailable or under-review Listings remain excluded.
2. Given filters are active, when the Tenant removes one filter or clears all filters, then the results update accordingly and the chosen values are preserved correctly across refresh or enhanced updates.
3. Given filtering is enhanced with JavaScript, when results refresh, then Maison shows listing-shaped skeletons rather than a full-page spinner and result-count updates are announced through a live region.
4. Given no Listing matches active filters, when results render, then Maison displays the empty state `Aucune annonce ne correspond exactement.` and provides one clear reset action.
5. Given a developer validates search behavior, when query and view tests run, then they cover combined filters, filter removal, empty results, and performance-sensitive query shape under MVP expectations.

## Tasks / Subtasks

- [x] Verify prerequisites and current browse implementation (AC: 1, 2, 3, 4, 5)
  - [x] Confirm Stories 1.1 through 2.2 are implemented before coding this story.
  - [x] Confirm public browse route/view, Listing Card include, pagination, and available-only selector from Story 2.2 exist.
  - [x] Confirm Story 2.1 Listing fields exist: `availability_status`, `commune`, integer monthly USD price, `bedroom_count`, and recency timestamps.
  - [x] Read existing `apps/listings/selectors.py`, `apps/listings/views.py`, `apps/listings/forms.py`, `templates/listings/browse.html`, Listing Card include, `static_src/js`, CSS input, URL config, and tests before editing.
  - [x] Preserve the unrelated sprint status changes already present, including any story currently marked `in-progress`.

- [x] Add a GET-bound search/filter form (AC: 1, 2, 4, 5)
  - [x] Add or update `apps/listings/forms.py` with a plain Django `Form`, not a `ModelForm`.
  - [x] Use query parameter names in `snake_case`: `commune`, `budget_min`, `budget_max`, and `bedrooms_min`.
  - [x] Make every filter optional.
  - [x] Trim and normalize `commune`; use exact or case-insensitive matching against stored Commune values, not broad substring search.
  - [x] Validate `budget_min` and `budget_max` as non-negative integers.
  - [x] Validate `budget_max >= budget_min` when both are provided.
  - [x] Validate `bedrooms_min` as a non-negative or positive integer according to the implemented model rules.
  - [x] Keep invalid form submissions on the browse surface with field-level errors and no server error.
  - [x] Do not store filters in session, cookies, user profile, or local database.

- [x] Extend selectors for combined filters (AC: 1, 5)
  - [x] Reuse or wrap the Story 2.2 public browse selector so `available` filtering and recency ordering stay centralized.
  - [x] Apply `commune` only when a valid Commune filter is active.
  - [x] Apply `monthly_price_amount__gte` for `budget_min` and `monthly_price_amount__lte` for `budget_max`, adapting field names to the implemented Story 2.1 model.
  - [x] Apply `bedroom_count__gte` for `bedrooms_min`, matching UX-DR7/UX-DR8 bedroom-minimum behavior.
  - [x] Ensure combined filters use logical AND, not OR.
  - [x] Ensure unavailable and under-review Listings remain excluded even when filters are active.
  - [x] Preserve deterministic recency ordering after filtering.
  - [x] Preserve pagination after filtering and reset `page` to 1 when filters change.

- [x] Update browse view for filters, chips, reset, and pagination (AC: 1, 2, 4, 5)
  - [x] Bind the filter form to `request.GET`.
  - [x] Pass the bound form, active filters, result count, pagination object, and filter-preserving query strings to the template.
  - [x] Add active filter chip data in Python/view helpers instead of building fragile query strings in the template.
  - [x] Each removable filter chip must link to the same browse route with that one filter removed and all remaining valid filters preserved.
  - [x] The clear-all action must link to the unfiltered browse route.
  - [x] Pagination links must preserve active filters.
  - [x] Empty and invalid query params must not survive in generated URLs.
  - [x] If invalid filters are submitted, display form errors and avoid applying invalid values silently.

- [x] Update templates for search form, selected chips, results, and empty state (AC: 1, 2, 3, 4)
  - [x] Add or update `templates/listings/includes/search_form.html`.
  - [x] Add or update `templates/listings/includes/filter_chips.html`.
  - [x] Add or update `templates/listings/includes/results_grid.html`.
  - [x] Render visible labels above controls: `Commune`, `Budget minimum`, `Budget maximum`, and `Chambres minimum`.
  - [x] Use compact French copy suitable for mobile browsing.
  - [x] Preserve chosen values in form inputs after normal refresh.
  - [x] Render removable chips for every active valid filter.
  - [x] Render one clear-all/reset action when filters are active.
  - [x] Render the exact filtered empty-state copy: `Aucune annonce ne correspond exactement.`
  - [x] Keep the default no-available-listings empty state from Story 2.2 distinct from the filtered empty state.
  - [x] Do not render a full-page spinner.
  - [x] Keep Listing Card rendering through the Story 2.2 card include.

- [x] Add progressive filter enhancement with modular JavaScript (AC: 2, 3, 5)
  - [x] Add or update `static_src/js/filters.js`.
  - [x] Keep the form fully functional without JavaScript through GET requests.
  - [x] Enhance form submit/change events with `fetch()` to request the same browse route using serialized `URLSearchParams`.
  - [x] Use same-origin GET requests; do not create a public `/api/` namespace.
  - [x] Prefer the same browse URL returning a JSON payload with rendered partial HTML when a feature header such as `X-Maison-Partial: filters` is present.
  - [x] Use the architecture JSON response shape: `{ "ok": true, "data": { ... } }` or `{ "ok": false, "error": { ... } }`.
  - [x] While the request is pending, set `aria-busy="true"` on the results region and show listing-shaped skeletons matching the Listing Card geometry.
  - [x] Replace only the results/chips/count regions on success, not the full page shell.
  - [x] Update browser history with the filtered URL so refresh/back/share keep the chosen values.
  - [x] On fetch failure, remove loading state and allow the normal form submission path or show a small recoverable inline message.
  - [x] Respect `prefers-reduced-motion`; do not add decorative transitions beyond the established 150-250ms range.

- [x] Add live result-count announcements and accessible loading state (AC: 3)
  - [x] Add a result-count element that is present in the initial HTML.
  - [x] Use `role="status"` or `aria-live="polite"` for result-count updates.
  - [x] Keep announcements brief, for example `12 annonces trouvées`.
  - [x] Do not use `aria-live="assertive"` for normal filtering.
  - [x] Keep keyboard focus stable when enhanced results update.
  - [x] Ensure skeletons are marked as loading placeholders and do not create noisy repeated announcements.

- [x] Preserve performance expectations (AC: 1, 3, 5)
  - [x] Keep pagination from Story 2.2 active under all filter combinations.
  - [x] Use indexed model fields from Story 2.1: availability, Commune, bedroom count, price, and recency.
  - [x] Avoid N+1 queries for photos and Commissionnaire Profile.
  - [x] Do not introduce Redis, external caching, a search engine, client-side-only filtering, or infinite scroll.
  - [x] Keep response payloads small for enhanced updates by returning only results/chips/count partials.

- [x] Add tests for combined filters and UI state (AC: 1, 2, 3, 4, 5)
  - [x] Test no filters returns only available Listings.
  - [x] Test Commune filter returns only matching available Listings.
  - [x] Test budget min/max filters return only Listings within range.
  - [x] Test bedroom minimum returns only Listings meeting the minimum.
  - [x] Test combined Commune + budget + bedrooms uses AND semantics.
  - [x] Test unavailable and under-review Listings remain excluded under every filter combination.
  - [x] Test invalid numeric filter values show form errors and do not crash.
  - [x] Test `budget_max < budget_min` shows a field or non-field error.
  - [x] Test active filter chips render and each remove URL preserves remaining filters.
  - [x] Test clear-all URL removes all filter params.
  - [x] Test pagination links preserve active filters.
  - [x] Test filtered empty state renders exact copy `Aucune annonce ne correspond exactement.` and one reset action.
  - [x] Test enhanced partial response, if implemented, follows the architecture JSON response shape.
  - [x] Test result-count live region exists in initial HTML.
  - [x] Test query count stays bounded for a representative filtered page with photos.

- [x] Run required checks (AC: 1, 2, 3, 4, 5)
  - [x] `python manage.py check`
  - [x] `python manage.py test apps.listings`
  - [x] `python manage.py test`
  - [x] `npm run css:build`
  - [x] `python manage.py collectstatic --noinput --dry-run`

## Dev Notes

### Source Context

- Story source: `_bmad-output/planning-artifacts/epics.md`, Epic 2, Story 2.3.
- Requirements: FR-2; NFR-1, NFR-2; UX-DR7, UX-DR8, UX-DR9, UX-DR23.
- FR-2 requires filtering rental Listings by Commune, monthly budget range, and bedroom count. Combined filters must return Listings satisfying every active filter.
- UX-DR7 requires visible labels and Commune, budget maximum/range, and bedroom controls. Desktop may group controls in one raised search surface; mobile stacks vertically.
- UX-DR8 requires preserved chosen values, removable selected filter chips, clear-all, and result-count announcements through a live region.
- UX-DR9 requires listing-shaped skeletons while search results refresh, never a full-page spinner.
- UX-DR23 requires the filtered empty state copy `Aucune annonce ne correspond exactement.` with one reset action.

### Dependency On Previous Stories

This story depends on Story 2.2 public browse.

Required Story 2.2 foundations:

- Public browse route and view.
- Available-only public Listing selector.
- Paginated server-rendered Listing grid.
- Listing Card include.
- No-available-listings default empty state.
- Query shape avoiding N+1 profile/photo loading.
- Stable Listing detail route or href contract.

If these are missing, implement Story 2.2 first. Do not create a separate search page that bypasses the existing browse route or card include.

### Current Workspace Snapshot

Targeted file inspection during story creation found a Django scaffold in place, but not the Listing implementation required by Stories 2.1 and 2.2:

- `apps/listings/apps.py` exists with `ListingsConfig`.
- `apps/listings/models.py`, `forms.py`, `selectors.py`, `views.py`, and `urls.py` do not exist yet.
- `templates/listings/` does not exist yet.
- `config/settings.py` already includes `apps.listings`, SQLite settings, `MEDIA_URL`, and `MEDIA_ROOT`.
- `config/urls.py` currently includes core, accounts, admin, and debug media serving; it does not yet include Listing URLs.
- `templates/base.html` provides the French HTML shell, header, messages, and `{% block content %}`.
- `static_src/css/input.css` already contains Maison design tokens, global focus styles, button styles, form-control styles, and a mobile breakpoint at `max-width: 700px`.

Because the prerequisite Listing model and browse/card implementation are not present in the current workspace snapshot, the developer must implement Stories 2.1 and 2.2 before this story or work from their completed branch if those stories are developed elsewhere.

### Previous Story Intelligence

- Story 2.2 explicitly deferred Commune/budget/bedroom filter behavior, filter chips, filtered empty state, and live result count to this story.
- Story 2.2 requires public browse to show only `available` Listings. This remains true under every filter combination.
- Story 2.2 requires pagination and bounded query counts. Filtering must compose with pagination rather than rendering every match.
- Story 2.2 keeps the full detail surface out of scope. Filter result cards should continue using the existing card navigation contract only.
- Story 2.1 recommended integer monthly USD fields. Budget filtering must compare integers, not formatted strings or floats.

### Architecture Compliance

- Use Django 5.2 LTS server-rendered views and templates.
- Use Django `forms.Form` for GET filter validation.
- Use selectors for query logic; keep business/query rules out of templates.
- Use query parameters for filters and `snake_case` parameter names.
- Keep JavaScript modular under `static_src/js/filters.js`.
- JavaScript must progressively enhance server-rendered HTML; the browse page must work without JS.
- Use `data-*` hooks for JavaScript.
- No inline JavaScript for business behavior.
- No public `/api/` namespace and no DRF.
- Do not add React, Vue, a SPA router, Redis, external search, PostgreSQL, or third-party filtering libraries.

### Recommended Filter Contract

Use these query parameters unless the implemented code already established equivalent names:

```text
commune=Ngaliema
budget_min=500
budget_max=1500
bedrooms_min=2
page=2
```

Filter semantics:

- `commune`: exact normalized Commune match; case-insensitive is acceptable.
- `budget_min`: `monthly_price_amount >= budget_min`.
- `budget_max`: `monthly_price_amount <= budget_max`.
- `bedrooms_min`: `bedroom_count >= bedrooms_min`.
- Combined filters use AND.
- Status filter is always `availability_status == available`.
- Recency order from Story 2.2 remains after filtering.
- Invalid filters produce form errors and should not be silently coerced into surprising searches.

Recommended selector shape:

```python
def filter_public_listings(filters):
    queryset = get_public_browse_listings()

    commune = filters.get("commune")
    if commune:
        queryset = queryset.filter(commune__iexact=commune)

    budget_min = filters.get("budget_min")
    if budget_min is not None:
        queryset = queryset.filter(monthly_price_amount__gte=budget_min)

    budget_max = filters.get("budget_max")
    if budget_max is not None:
        queryset = queryset.filter(monthly_price_amount__lte=budget_max)

    bedrooms_min = filters.get("bedrooms_min")
    if bedrooms_min is not None:
        queryset = queryset.filter(bedroom_count__gte=bedrooms_min)

    return queryset
```

Adapt field names to the actual Story 2.1 implementation. The status filter should remain inside `get_public_browse_listings()` or an equivalent single source of truth.

### Query String And Chip Guardrails

- Generate chip remove URLs in Python using `QueryDict.copy()` or `urllib.parse.urlencode`, not hand-built string concatenation in templates.
- Drop empty values from generated URLs.
- Remove `page` when filters change or when a chip is removed.
- Preserve active filters when moving between pagination pages.
- The clear-all action should point to the unfiltered browse route without query params.
- Do not persist filters in server-side session state; URLs are the source of truth.

### Progressive Enhancement Guardrails

Baseline behavior:

- The filter form uses `method="get"`.
- Normal form submission reloads the browse page with values preserved.
- The filtered empty state and clear action work without JavaScript.

Enhanced behavior:

- `filters.js` intercepts form changes/submission only after the page has usable server-rendered HTML.
- It builds the query string with `URLSearchParams`.
- It uses `fetch()` with a GET request to the same browse URL.
- It requests a partial response through a feature header, not a new public API path.
- It sets a local loading state on the results region, shows listing-shaped skeletons, and updates `aria-busy`.
- It updates results, filter chips, pagination, and result count from the server-rendered partials.
- It announces result-count changes via `role="status"` or `aria-live="polite"`.
- It updates `history.pushState()` to preserve shareable URLs and browser Back behavior.
- If enhancement fails, the normal GET flow remains available.

### UX And Copy Guardrails

Suggested French copy:

- `Rechercher`
- `Commune`
- `Budget minimum`
- `Budget maximum`
- `Chambres minimum`
- `Effacer les filtres`
- `Aucune annonce ne correspond exactement.`
- `12 annonces trouvées`
- `1 annonce trouvée`

Visual behavior:

- Mobile stacks controls vertically.
- Desktop may group controls in one raised search surface.
- Filter chips are removable and at least 44px tall/tappable.
- The clear-all action remains reachable when filters are active.
- Skeletons match Listing Card geometry and should not replace header/search/filter context.
- Do not add decorative empty-state illustrations unless the existing design system already uses them.

### Scope Boundaries

Implement now:

- GET filter form.
- Combined filters on public available Listings.
- Active filter chips and clear-all.
- Filter-preserving pagination.
- Filtered empty state with exact required copy.
- Progressive enhanced result refresh, listing-shaped skeletons, and live result-count announcements.
- Tests for combined filters, chip URLs, empty state, partial response, and query shape.

Do not implement now:

- Full Listing Detail drawer/screen, gallery, WhatsApp CTA, report flow, or contact eligibility. Story 2.4 owns detail.
- Publication stepper, preview, or submission validation.
- Availability reconfirmation workflow.
- Moderation, verification state modeling, Reports, Leads, audit events, favorites persistence, or view counts.
- External search services, autocomplete, map search, saved searches, analytics instrumentation, or personalized recommendations.

### File Structure Requirements

Expected files to create or update, assuming prerequisite Django scaffold exists:

```text
apps/listings/
├── forms.py
├── selectors.py
├── views.py
├── urls.py
└── tests/
    ├── test_forms.py
    ├── test_selectors.py
    ├── test_views.py
    └── test_templates.py
templates/listings/
├── browse.html
└── includes/
    ├── search_form.html
    ├── filter_chips.html
    ├── results_grid.html
    ├── listing_card.html
    └── listing_skeleton.html
static_src/js/
└── filters.js
static_src/css/
└── input.css              # only if skeleton or responsive styles need explicit CSS
```

Read existing files before editing. Preserve the card include and browse route from Story 2.2, and preserve app registration/static asset conventions from Story 1.1.

### Testing Requirements

Minimum tests:

- Form:
  - all fields optional
  - valid integer budgets and bedrooms clean to integers
  - non-numeric budgets/bedrooms fail validation
  - negative values fail validation
  - `budget_max < budget_min` fails validation
  - Commune whitespace is trimmed
- Selector:
  - no filters returns available Listings only
  - Commune filter works
  - budget min/max work
  - bedroom minimum works
  - combined filters use AND semantics
  - unavailable and under-review Listings are always excluded
  - ordering remains deterministic after filters
- View/template:
  - filter values persist after GET refresh
  - active chips render with remove URLs
  - clear-all removes all filters
  - pagination links preserve filters
  - filtered empty state uses exact copy
  - result-count live region exists
  - enhanced partial response uses expected JSON shape if implemented
  - query count stays bounded for representative filtered results with photos

Use Django's built-in test runner. Browser automation is optional only if the project already has that layer; this story can be validated with Django client, form, selector, and template tests.

### Latest Technical Notes

- Django 5.2 forms are appropriate for GET search filters because forms validate, clean, and preserve submitted values without changing database state.
- Django documentation explicitly treats GET as suitable for search-style forms because it produces bookmarkable, shareable URLs and should not change system state.
- Django `QuerySet.filter()` composes conditions through chained calls; chaining the active filters gives the required AND behavior.
- Django `Paginator` should continue paginating filtered `QuerySet` results rather than loading every match.
- MDN documents `aria-live="polite"` as the appropriate non-interruptive live-region behavior for ordinary UI updates such as refreshed results.
- MDN Fetch API supports GET requests with query strings through `URLSearchParams`; use it only as progressive enhancement.

### Anti-Patterns To Avoid

- Filtering client-side from all Listings already loaded into the page.
- Losing the `available` status filter when search params are present.
- Using OR semantics for combined filters.
- Preserving stale `page` numbers when filters change.
- Building chip URLs by string concatenation in templates.
- Showing the wrong empty-state copy for filtered results.
- Replacing the full page with a spinner.
- Requiring JavaScript for basic filtering.
- Adding a public API namespace, DRF, external search, or Redis.
- Building detail, Lead, WhatsApp, moderation, verification, reports, favorites, or analytics features inside this story.

### References

- `_bmad-output/planning-artifacts/epics.md#Story-2.3-Search-Filters-And-Empty-States`
- `_bmad-output/planning-artifacts/epics.md#UX-DR7`
- `_bmad-output/planning-artifacts/epics.md#UX-DR8`
- `_bmad-output/planning-artifacts/epics.md#UX-DR9`
- `_bmad-output/planning-artifacts/epics.md#UX-DR23`
- `_bmad-output/planning-artifacts/prds/prd-maison-2026-05-31/prd.md#FR-2-Filter-rental-Listings`
- `_bmad-output/planning-artifacts/architecture.md#Primary-communication-pattern-Django-views--templates`
- `_bmad-output/planning-artifacts/architecture.md#JavaScript-architecture`
- `_bmad-output/planning-artifacts/architecture.md#Implementation-Patterns-and-Consistency-Rules`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/DESIGN.md#Search-Form`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/EXPERIENCE.md#Tenant-Discovery`
- `_bmad-output/implementation-artifacts/2-2-public-browse-with-listing-cards.md`
- `https://docs.djangoproject.com/en/5.2/topics/forms/`
- `https://docs.djangoproject.com/en/5.2/ref/models/querysets/#filter`
- `https://docs.djangoproject.com/en/5.2/topics/pagination/`
- `https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-live`
- `https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch`

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- Story created from BMAD epics, PRD, architecture, UX artifacts, previous Story 2.2 context, and Django/MDN documentation.
- Targeted workspace inspection found the Django scaffold and `apps.listings` app config, but no Listing models, browse views, Listing templates, or filter implementation yet.
- 2026-06-08: Started implementation from baseline commit `83de0f8f0b1584d8b991f06922f9a3af5385d75b`; confirmed Story 2.1 model fields and Story 2.2 browse route/view, Listing Card include, pagination, and available-only selector are present. `python manage.py check` and `python manage.py test apps.listings` passed with 51 tests before Story 2.3 feature edits.
- 2026-06-08: Form RED failed on missing `apps.listings.forms.ListingFilterForm`; GREEN added a plain GET-bound `forms.Form` with optional `commune`, `budget_min`, `budget_max`, and `bedrooms_min` validation. `python manage.py test apps.listings.tests.test_forms` passed with 6 tests.
- 2026-06-08: Selector RED failed on missing `filter_public_listings`; GREEN wrapped `get_public_browse_listings()` with AND-composed Commune, budget, and bedroom filters while preserving available-only filtering, photo/profile prefetching, and deterministic recency ordering. `python manage.py test apps.listings.tests.test_selectors` passed with 9 tests.
- 2026-06-08: View/template RED failed on missing filter context, chips, filter-preserving pagination, form UI, filtered empty state, and live count. GREEN added bound form handling, Python-generated chip URLs, partial templates, result counts, field-level errors, filtered empty copy, and filter-preserving pagination. View/template targeted tests passed.
- 2026-06-08: Progressive enhancement RED failed on full-page HTML for `X-Maison-Partial: filters` and missing script. GREEN added same-route JSON partial envelopes, `static_src/js/filters.js`, listing-shaped skeletons, `aria-busy`, live count updates, `history.pushState()`, and a recoverable fetch error message. Targeted partial and template tests passed.
- 2026-06-08: Performance coverage added for representative filtered pages with photos; bounded-query view test passed without N+1 profile/photo regressions.
- 2026-06-08: Required checks passed: `python manage.py check`, `python manage.py test apps.listings` (76 tests), `python manage.py test` (171 tests), `npm run css:build`, and `python manage.py collectstatic --noinput --dry-run`.
- 2026-06-08: Browser verification passed on `http://127.0.0.1:8002/annonces/`: filter form and script loaded, enhanced Commune change used partial fetch, chip and URL updated to `?commune=Ngaliema`, `aria-busy` returned to `false`, mobile viewport had no horizontal overflow, and no console errors were emitted.

### Implementation Plan

- Keep `get_public_browse_listings()` as the public browse read boundary, then compose valid filter values in `filter_public_listings()` so availability, recency ordering, `select_related()`, and `Prefetch()` remain centralized.
- Bind `ListingFilterForm` to `request.GET` on every browse request; apply filters only when the form is valid, and keep invalid submissions on the browse page with field-level errors and unfiltered available results.
- Generate active filter chips, clear-all, and pagination URLs in Python from cleaned filter values so empty, invalid, and stale `page` parameters do not survive generated URLs.
- Split browse rendering into `search_form.html`, `filter_chips.html`, and `results_grid.html`; reuse the Story 2.2 `listing_card.html` include for all result cards.
- Use the same browse URL for progressive enhancement with `X-Maison-Partial: filters`, returning JSON envelopes with rendered partial HTML and updating only results, chips, count, and browser history.

### Completion Notes List

- Story context generated with status `ready-for-dev`.
- Sprint status updated for Story 2.3.
- Verified prerequisites and current browse implementation state; no project-level `project-context.md`, `apps/listings/forms.py`, or `static_src/js` exists yet, so this story will add the filter form and enhancement module.
- Added GET-bound listing filter form with optional normalized Commune, non-negative integer budget and bedroom filters, and `budget_max >= budget_min` validation.
- Added combined public listing filters using AND semantics while preserving available-only results, deterministic recency ordering, pagination compatibility, and photo/profile query performance.
- Updated browse view context with bound form, active filter values, result count, Python-generated removable chips, clear-all URL, and filter-preserving pagination URLs.
- Added search form, active filter chips, result grid partial, exact filtered empty state copy, live result-count region, and filter UI CSS while keeping the existing Listing Card include.
- Added same-route progressive enhancement with JSON partial responses, listing-shaped skeletons, `aria-busy`, live count updates, browser history updates, and recoverable fetch failure messaging.
- Added form, selector, view, template, partial response, chip URL, filtered empty state, live region, and filtered bounded-query tests.
- Ran all required validation commands successfully and completed a Playwright browser smoke test on a fresh local server.

### File List

- `_bmad-output/implementation-artifacts/2-3-search-filters-and-empty-states.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `apps/listings/forms.py`
- `apps/listings/selectors.py`
- `apps/listings/views.py`
- `apps/listings/tests/test_forms.py`
- `apps/listings/tests/test_selectors.py`
- `apps/listings/tests/test_views.py`
- `apps/listings/tests/test_templates.py`
- `config/settings.py`
- `templates/base.html`
- `templates/listings/browse.html`
- `templates/listings/includes/search_form.html`
- `templates/listings/includes/filter_chips.html`
- `templates/listings/includes/results_grid.html`
- `static_src/js/filters.js`
- `static_src/css/input.css`
- `static/css/app.css`

### Change Log

- 2026-06-08: Implemented Story 2.3 search filters and empty states; moved story to review.
