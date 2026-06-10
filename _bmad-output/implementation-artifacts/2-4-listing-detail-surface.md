---
baseline_commit: 83de0f8f0b1584d8b991f06922f9a3af5385d75b
---

# Story 2.4: Listing Detail Surface

Status: review

<!-- Validation: created from bmad-create-story workflow on 2026-06-06. -->

## Story

As a Tenant,
I want to review a Listing's full details, photos, availability, and Commissionnaire identity,
so that I can decide whether it is worth contacting someone about that home.

## Acceptance Criteria

1. Given an available Listing exists, when a Tenant opens its detail surface, then Maison displays all Listing Card fields plus media gallery, description, Availability Status, last update time, and Commissionnaire Profile identity and the WhatsApp Contact Action is visible only while Availability Status is `available`.
2. Given a Listing has photos, when the gallery renders, then Maison shows a 4:3 main image, deterministic thumbnails, image count, rounded image corners, and meaningful alt text where available.
3. Given the Listing is unverified, when detail renders, then Maison does not show a Verification Badge or Verification Box and the copy does not imply Maison guarantees availability or transaction outcome.
4. Given the Listing is opened on desktop, when the detail surface appears, then it renders as a right-side drawer preserving browse context behind a scrim and focus is trapped, Escape closes the drawer, closed content is inert, and focus returns to the triggering card.
5. Given the Listing is opened on mobile, when the detail surface appears, then it renders as a full-screen detail surface with familiar back behavior and sticky bottom CTA when valid and controls meet mobile touch-target and visible-focus requirements.

## Tasks / Subtasks

- [x] Verify prerequisites and current browse implementation (AC: 1, 2, 3, 4, 5)
  - [x] Confirm Stories 1.1 through 2.3 are implemented before coding this story.
  - [x] Confirm the `Listing` and `ListingPhoto` models, public browse route, Listing Card include, filter-preserving browse URL, and stable Listing detail href contract exist.
  - [x] Confirm `Listing` exposes monthly USD price, Commune, bedroom count, description, Availability Status, recency/update timestamps, and a `CommissionnaireProfile` relationship.
  - [x] Confirm `ListingPhoto` exposes deterministic ordering and primary-photo behavior from Story 2.1.
  - [x] Read existing `apps/listings`, `templates/listings`, `static_src/js`, `static_src/css/input.css`, `config/urls.py`, `templates/base.html`, and listing tests before editing.
  - [x] Preserve unrelated sprint status changes already present, including any story currently marked `in-progress`.

- [x] Add detail selectors and visibility rules (AC: 1, 2, 3)
  - [x] Add or update `apps/listings/selectors.py`.
  - [x] Implement a selector such as `get_listing_detail_queryset()` that loads Listing, Commissionnaire Profile, and ordered photos without N+1 queries.
  - [x] Exclude `under_review` Listings from public detail access.
  - [x] Allow `available` Listings to render the full detail surface.
  - [x] If an `available` Listing becomes `unavailable` after browse, render an unavailable detail state with no WhatsApp CTA and a clear return-to-results action.
  - [x] Preserve deterministic photo ordering: explicit primary first where implemented, then `position`, then `id`.
  - [x] Do not create new Listing ownership, verification, Lead, Report, or audit models in this story.

- [x] Add detail route and views (AC: 1, 4, 5)
  - [x] Add or update `apps/listings/views.py` with a public detail view or `DetailView`.
  - [x] Add or update `apps/listings/urls.py` with a stable route name such as `listings:detail`.
  - [x] Include Listing URLs from `config/urls.py` if Story 2.2 has not already done so.
  - [x] Support normal full-page HTML detail responses for no-JavaScript and mobile/back-button behavior.
  - [x] Support a partial detail response for desktop drawer enhancement when requested through a feature header such as `X-Maison-Partial: listing-detail`.
  - [x] Keep the response server-rendered; do not add a public API namespace or DRF.
  - [x] Return 404 for missing Listings and public-ineligible `under_review` Listings.

- [x] Build detail templates and includes (AC: 1, 2, 3, 5)
  - [x] Add `templates/listings/detail.html` for the full-page/mobile detail route.
  - [x] Add `templates/listings/includes/detail_panel.html` for reusable drawer/full-page content.
  - [x] Add `templates/listings/includes/gallery.html`.
  - [x] Add `templates/listings/includes/availability_block.html`.
  - [x] Add `templates/listings/includes/commissionnaire_block.html`.
  - [x] Add `templates/listings/includes/contact_cta.html`.
  - [x] Add `templates/listings/includes/report_action.html`.
  - [x] Render all Listing Card fields from Story 2.2 plus gallery, description, Availability Status, last update time, and Commissionnaire Profile identity.
  - [x] Keep report action visually secondary and error-colored, but do not implement report submission; Story 4.4 owns the report flow.
  - [x] Keep templates compact and avoid large monolithic pages.

- [x] Implement the gallery (AC: 2, 5)
  - [x] Render a main image with `aspect-ratio: 4 / 3`.
  - [x] Render thumbnails in deterministic order.
  - [x] Render a visible image count such as `1/8`.
  - [x] Use rounded image corners from Maison design tokens.
  - [x] Use meaningful alt text where available; fall back to concise Listing context such as Commune and bedroom count.
  - [x] Keep thumbnail controls at least 44px tappable and keyboard reachable.
  - [x] Add `static_src/js/gallery.js` only if needed for progressive thumbnail switching; the first image and thumbnails must still render without JavaScript.
  - [x] Do not use generated luxury imagery or unrelated placeholders as production media.

- [x] Implement availability and trust copy guardrails (AC: 1, 3)
  - [x] Render Availability Status and last update/freshness copy together in one availability block.
  - [x] Show the WhatsApp Contact Action only when `availability_status == "available"`.
  - [x] Hide the CTA for `unavailable` Listings and provide a return-to-results action.
  - [x] Do not expose a contact CTA for `under_review` Listings because they should not be public.
  - [x] Render no Verification Badge and no Verification Box for unverified Listings.
  - [x] If an explicit verified state already exists from prior work, render the badge and the canonical Verification Box copy only when that state is true.
  - [x] Do not add verification persistence, checklist state, or moderation workflow in this story.
  - [x] Do not imply Maison guarantees availability, information accuracy, a visit, negotiation, payment, or contract outcome.

- [x] Implement Commissionnaire block and CTA affordance (AC: 1, 5)
  - [x] Render Commissionnaire display identity from `CommissionnaireProfile`.
  - [x] Include a compact note that WhatsApp contact follows Lightweight Identification.
  - [x] Do not expose the Commissionnaire raw phone number in the detail page unless a later Lead/WhatsApp story explicitly requires it.
  - [x] Render `Contacter sur WhatsApp` only for available Listings.
  - [x] Do not open WhatsApp directly in this story.
  - [x] Do not create Leads, consent records, or handoff URLs in this story; Stories 3.1 through 3.3 own that flow.
  - [x] If Lead/identification routes are not implemented yet, render the CTA with stable `data-*` hooks or a disabled/future-safe affordance that tests can verify without side effects.

- [x] Add desktop drawer progressive enhancement (AC: 4)
  - [x] Add or update `static_src/js/listing-detail.js`.
  - [x] Keep card links valid normal links; JavaScript may intercept only on desktop widths above the UX-DR33 desktop breakpoint.
  - [x] Fetch the partial detail panel from the same Listing detail route using a feature header.
  - [x] Render the drawer as a right-side panel about `480px-620px` wide on desktop.
  - [x] Preserve browse context behind a scrim.
  - [x] Use a native `<dialog>` with `showModal()` where practical, or implement equivalent WAI-ARIA modal behavior if the chosen layout cannot use `<dialog>`.
  - [x] Trap focus inside the open drawer.
  - [x] Include a visible close button with an accessible name.
  - [x] Support Escape to close.
  - [x] Make closed overlay content inert/unfocusable.
  - [x] Restore focus to the triggering card after close.
  - [x] Respect `prefers-reduced-motion` and keep transitions within the established 150-250ms range.
  - [x] Do not create an SPA router or client-owned Listing state.

- [x] Preserve mobile full-screen behavior (AC: 5)
  - [x] Under `700px`, let card links navigate to the full detail route rather than opening a desktop drawer.
  - [x] Ensure browser Back returns to browse/search results with the existing query string when applicable.
  - [x] Use a sticky bottom CTA only when the Listing is available.
  - [x] Ensure close/back, gallery, report, and contact controls meet 44px touch target requirements.
  - [x] Ensure visible focus states remain clear on mobile and keyboard.
  - [x] Avoid nested cards, oversized hero treatment, and decorative layouts that slow detail review.

- [x] Add tests for detail selector, route, templates, and enhancement hooks (AC: 1, 2, 3, 4, 5)
  - [x] Test available Listing detail returns 200.
  - [x] Test `under_review` Listing detail returns 404 or public-ineligible response.
  - [x] Test unavailable Listing detail hides WhatsApp CTA and shows return-to-results action.
  - [x] Test detail renders monthly price, Commune, bedroom count, description, availability, last update, Commissionnaire identity, and report action.
  - [x] Test gallery uses deterministic photo order, main image, thumbnails, and count.
  - [x] Test unverified Listing renders no Verification Badge and no Verification Box.
  - [x] If verified state exists, test verified Listing renders text plus icon and canonical Verification Box copy.
  - [x] Test partial detail response works only through the intended feature header and does not return a public API contract.
  - [x] Test no direct WhatsApp URL or Lead creation occurs in this story.
  - [x] Test card/detail route preserves or accepts return-to-results query context where implemented.
  - [x] Test query count stays bounded for a detail page with photos and Commissionnaire Profile.
  - [x] Add template/CSS/JS assertions for drawer hooks, `dialog`/ARIA attributes, close control, inert behavior hooks, and sticky mobile CTA classes.

- [x] Run required checks (AC: 1, 2, 3, 4, 5)
  - [x] `python manage.py check`
  - [x] `python manage.py test apps.listings`
  - [x] `python manage.py test`
  - [x] `npm run css:build`
  - [x] `python manage.py collectstatic --noinput --dry-run`

## Dev Notes

### Source Context

- Story source: `_bmad-output/planning-artifacts/epics.md`, Epic 2, Story 2.4.
- Requirements: FR-3, FR-14; NFR-1; UX-DR12, UX-DR13, UX-DR14, UX-DR15, UX-DR16, UX-DR18, UX-DR33.
- FR-3 requires Listing detail to display all card fields, Listing media, description, Availability Status, Commissionnaire Profile identity, a Report Action, and a WhatsApp Contact Action only while the Listing is `available`.
- FR-14 requires unverified Listings to never display the Verification Badge and requires detail to show last update time.
- UX-DR12/UX-DR33 require mobile full-screen detail and desktop right-side drawer behavior.
- UX-DR13 requires focus trap, Escape support, inert closed overlays, and focus restoration.
- UX-DR14 requires a 4:3 gallery, deterministic thumbnails, visible count, rounded corners, and meaningful alt text.
- UX-DR15/UX-DR16 require the content hierarchy and availability block behavior.
- UX-DR18 requires a compact Commissionnaire identity row with a note that WhatsApp contact follows Lightweight Identification.

### Dependency On Previous Stories

This story depends on Stories 2.1 through 2.3.

Required previous foundations:

- Story 2.1: `Listing`, `ListingPhoto`, local media, status choices, ownership through `CommissionnaireProfile`, deterministic photo ordering, primary photo selection, and timestamps.
- Story 2.2: public browse route, card include, stable detail href contract, available-only browse selector, and no unverified badge.
- Story 2.3: filter-preserving browse/search URL state and progressive enhancement patterns.

If any prerequisite is missing, implement it first. Do not build detail against temporary fake Listing structures or duplicate card/gallery logic outside `apps/listings`.

### Current Workspace Snapshot

Targeted file inspection during story creation found a Django scaffold in place, but not the Listing implementation required by Stories 2.1 through 2.3:

- `apps/listings/apps.py` exists with `ListingsConfig`.
- `apps/listings/models.py`, `forms.py`, `selectors.py`, `views.py`, and `urls.py` do not exist yet.
- `templates/listings/` does not exist yet.
- `config/settings.py` includes `apps.listings`, SQLite settings, `MEDIA_URL`, and `MEDIA_ROOT`.
- `config/urls.py` currently includes core, accounts, admin, and debug media serving; it does not yet include Listing URLs.
- `templates/base.html` provides the French shell, skip link, header, messages, and `{% block content %}`.
- `static_src/css/input.css` contains Maison design tokens, focus styles, button styles, form-control styles, and a `max-width: 700px` breakpoint.

The developer must implement or work from completed Stories 2.1, 2.2, and 2.3 before implementing this detail surface.

### Previous Story Intelligence

- Story 2.3 preserved browse/filter URLs as the source of truth. Detail links should preserve a return URL or query context so users can return to filtered results.
- Story 2.3 enhanced filtering with partial responses and local loading states, not a public API. Detail drawer enhancement should follow the same feature-header/partial-response pattern.
- Story 2.2 required card links to be normal links first. Desktop drawer JS may intercept, but no-JS and mobile must still work.
- Story 2.2 required unverified Listings to render no Verification Badge. This story extends that rule to detail pages and the Verification Box.
- Story 2.1 required real uploaded Listing photos and deterministic ordering. Gallery rendering must use those photos, not generated placeholders.

### Architecture Compliance

- Use Django 5.2 LTS server-rendered views and templates.
- Keep detail query logic in selectors.
- Keep business rules out of templates.
- Use small template includes for gallery, availability, commissionnaire block, CTA, and report action.
- Use modular JavaScript under `static_src/js/listing-detail.js` and optionally `static_src/js/gallery.js`.
- Use `data-*` hooks for progressive enhancement.
- No inline JavaScript for business behavior.
- No public `/api/` namespace and no DRF.
- Do not add React, Vue, SPA routing, Redis, external cache, or client-owned Listing state.

### Recommended Detail Contract

Recommended route contract:

```text
GET /listings/<listing_id>/
GET /listings/<listing_id>/?from=<encoded browse path>
```

Recommended names:

```python
app_name = "listings"
urlpatterns = [
    path("", views.BrowseView.as_view(), name="browse"),
    path("<int:pk>/", views.ListingDetailView.as_view(), name="detail"),
]
```

Adapt to the actual identifier chosen in Story 2.1. If Story 2.1 added a public UUID or slug, prefer that over exposing sequential ids.

Recommended selector behavior:

```python
def get_listing_detail_queryset():
    ordered_photos = ListingPhoto.objects.order_by("-is_primary", "position", "id")

    return (
        Listing.objects.exclude(
            availability_status=Listing.AvailabilityStatus.UNDER_REVIEW,
        )
        .select_related("commissionnaire_profile")
        .prefetch_related(Prefetch("photos", queryset=ordered_photos))
    )
```

Cards should still link only from available browse results. The direct detail route can render an unavailable state when a Listing has become unavailable since the card was opened.

### Content Hierarchy

Render detail content in this order:

1. Sticky header: close/back, optional share/favorite only if already implemented.
2. Gallery: main 4:3 image, thumbnails, image count.
3. Primary facts: Commune, optional neighborhood/title when implemented, monthly price, bedroom count, optional existing facts.
4. Availability block: status plus last update/freshness copy.
5. Verification Box only if explicit verified state exists and is true.
6. Description.
7. Commissionnaire block: compact identity row and handoff note.
8. Report Action: visually secondary, error-colored text/action.
9. Sticky bottom CTA: `Contacter sur WhatsApp` only if Listing is available.

Do not add property-type, bathroom, view-count, favorite, share, or verified persistence fields unless they already exist from prior implementation.

### Contact And Report Boundaries

WhatsApp Contact Action:

- Render only for available Listings.
- Do not open WhatsApp directly.
- Do not generate a WhatsApp URL.
- Do not create a Lead.
- Do not collect Lightweight Identification.
- Provide stable hooks or a future-safe route for Stories 3.1 through 3.3.

Report Action:

- Render a visually secondary action so the detail hierarchy anticipates reporting.
- Do not create `Report` records.
- Do not implement reason selection or submission.
- If a report route already exists, link to it; otherwise use a safe non-submitting affordance with a clear future hook.
- Story 4.4 owns the full Report flow.

### Desktop Drawer Accessibility

Prefer a native `<dialog>` for the desktop drawer if it can be styled as a right-side panel. If using a custom drawer, match the WAI-ARIA modal dialog pattern.

Required behavior:

- Opening moves focus inside the drawer.
- `Tab` and `Shift+Tab` cycle within the open drawer.
- Escape closes the drawer.
- A visible close button is in the tab sequence.
- The drawer has an accessible name through `aria-labelledby` or an equivalent visible title.
- Content outside the open drawer is inert or otherwise not interactive.
- Closed drawer content is not focusable.
- Closing restores focus to the card/link that opened it.
- Scrim visually obscures the browse context without destroying the browse DOM state.

### Mobile Detail Behavior

- Under `700px`, use full-screen detail through normal navigation.
- Preserve browser Back behavior.
- Keep a sticky bottom CTA only when the Listing is available.
- Keep content readable with stable image dimensions and no oversized hero treatment.
- Make close/back, gallery thumbnail, report, and contact controls at least 44px.
- Maintain visible focus for keyboard and assistive technology users.

### Trust And Copy Guardrails

Suggested French copy:

- `Retour aux résultats`
- `Disponible`
- `Indisponible`
- `Mis à jour le ...`
- `Contacter sur WhatsApp`
- `Le contact WhatsApp passe par une identification légère.`
- `Signaler cette annonce`
- `Cette annonce n'est plus disponible.`
- `Voir d'autres annonces`

Forbidden copy/implications:

- Do not say Maison guarantees availability.
- Do not say Maison guarantees transaction outcome.
- Do not imply all Listings are verified.
- Do not use vague unverified trust labels such as `sûr`, `contrôlé`, `garanti`, or `confirmé`.
- Do not imply Maison reads WhatsApp conversations.

Canonical verified copy, only when an explicit verified state exists and is true:

```text
Cette annonce a passé un contrôle supplémentaire. Le badge ne garantit pas le résultat d'une transaction hors ligne.
```

### Scope Boundaries

Implement now:

- Detail selector and route.
- Full-page/mobile detail template.
- Reusable detail panel include.
- Gallery include and optional progressive thumbnail switching.
- Availability block.
- Commissionnaire identity block.
- Contact CTA visibility rules.
- Report Action affordance.
- Desktop drawer enhancement with focus/inert/Escape/focus-return behavior.
- Tests for public eligibility, gallery, trust copy, CTA visibility, drawer hooks, and no side effects.

Do not implement now:

- Lead creation, Lightweight Identification, WhatsApp URL generation, or handoff failure states.
- Report submission, report reason form, moderation queue, or report resolution.
- Verification model, checklist, moderation decisions, verified state changes, audit events, favorites persistence, share persistence, view counts, or analytics instrumentation.
- Cloud media transforms, image CDN, SPA routing, or client-only detail data fetching.

### File Structure Requirements

Expected files to create or update, assuming prerequisite stories are implemented:

```text
apps/listings/
├── selectors.py
├── views.py
├── urls.py
└── tests/
    ├── test_detail_selectors.py
    ├── test_detail_views.py
    ├── test_detail_templates.py
    └── test_detail_accessibility.py
templates/listings/
├── detail.html
└── includes/
    ├── detail_panel.html
    ├── gallery.html
    ├── availability_block.html
    ├── commissionnaire_block.html
    ├── contact_cta.html
    └── report_action.html
static_src/js/
├── listing-detail.js
└── gallery.js              # optional if thumbnail switching needs JS
static_src/css/
└── input.css               # drawer, gallery, sticky CTA, and responsive detail styles
config/
└── urls.py                 # only if Listing URLs are not included yet
```

Read existing files before editing. Preserve the card include, browse route, filters, static asset pipeline, auth routes, and base template shell.

### Testing Requirements

Minimum tests:

- Selector:
  - available Listing is detail-eligible
  - unavailable Listing can render unavailable detail state
  - under-review Listing is not public detail-eligible
  - photos are ordered deterministically
  - query count remains bounded with photos and profile
- View:
  - available Listing detail returns 200
  - missing Listing returns 404
  - under-review Listing returns 404
  - partial response returns reusable panel content only when feature header is sent
  - no public API namespace is introduced
- Template:
  - renders all card fields plus description, availability, last update, gallery, Commissionnaire identity
  - renders report action
  - renders WhatsApp CTA only for available Listing
  - hides CTA for unavailable Listing
  - does not render badge/Verification Box for unverified Listing
  - renders canonical Verification Box copy only if explicit verified state exists and is true
  - gallery contains 4:3 main image, thumbnails, count, and alt text
  - desktop drawer hooks/attributes and mobile sticky CTA classes exist
  - no direct WhatsApp URL or Lead creation side effect is present

Browser automation is useful for focus trap/Escape/focus-return if the project already has Playwright. If not, add DOM/JS unit-level assertions plus manual QA notes; do not block the story on introducing a full browser test framework.

### Latest Technical Notes

- Django 5.2 `DetailView` is suitable for displaying a single object and exposes the object in context while allowing `get_queryset()` and `get_context_data()` customization.
- Django `render_to_string()` can render server-side partial templates for progressive enhancement responses without creating a public API.
- Native `<dialog>` opened with `showModal()` provides modal behavior and can make outside page content inert; it can be styled as a drawer when used carefully.
- The HTML `inert` attribute makes an element and its descendants non-interactive and unavailable to focus/navigation.
- WAI-ARIA APG modal dialog guidance requires focus to move inside the dialog, Tab/Shift+Tab to remain within it, Escape to close, a visible close button, and focus restoration to the invoking element.

### Anti-Patterns To Avoid

- Displaying `under_review` Listing detail publicly.
- Showing WhatsApp CTA for unavailable Listings.
- Opening WhatsApp without Lead creation.
- Creating Leads in this story.
- Implementing Report submission in this story.
- Showing a Verification Badge or Verification Box for unverified Listings.
- Using broad trust copy that implies guarantee or verification.
- Loading detail data only through client-side JSON.
- Destroying browse state when desktop drawer opens.
- Failing to restore focus to the triggering card.
- Hiding drawer content visually while leaving it focusable.
- Building an SPA router, DRF endpoint, or public `/api/` surface.

### References

- `_bmad-output/planning-artifacts/epics.md#Story-2.4-Listing-Detail-Surface`
- `_bmad-output/planning-artifacts/epics.md#UX-DR12`
- `_bmad-output/planning-artifacts/epics.md#UX-DR13`
- `_bmad-output/planning-artifacts/epics.md#UX-DR14`
- `_bmad-output/planning-artifacts/epics.md#UX-DR15`
- `_bmad-output/planning-artifacts/epics.md#UX-DR16`
- `_bmad-output/planning-artifacts/epics.md#UX-DR18`
- `_bmad-output/planning-artifacts/prds/prd-maison-2026-05-31/prd.md#FR-3-Review-Listing-details`
- `_bmad-output/planning-artifacts/prds/prd-maison-2026-05-31/prd.md#FR-14-Display-trust-signals`
- `_bmad-output/planning-artifacts/architecture.md#Primary-communication-pattern-Django-views--templates`
- `_bmad-output/planning-artifacts/architecture.md#JavaScript-architecture`
- `_bmad-output/planning-artifacts/architecture.md#Project-Structure`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/DESIGN.md#Listing-Detail-Panel`
- `_bmad-output/planning-artifacts/ux-designs/ux-maison-2026-06-01/EXPERIENCE.md#Tenant-Discovery`
- `_bmad-output/implementation-artifacts/2-3-search-filters-and-empty-states.md`
- `https://docs.djangoproject.com/en/5.2/ref/class-based-views/generic-display/#detailview`
- `https://docs.djangoproject.com/en/5.2/ref/templates/api/#django.template.loader.render_to_string`
- `https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog`
- `https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/inert`
- `https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/`

## Dev Agent Record

### Agent Model Used

Gemini 3.5 Flash

### Debug Log References

- Story created from BMAD epics, PRD, architecture, UX artifacts, previous Story 2.3 context, workspace inspection, and Django/MDN/WAI documentation.
- Developed selector `get_listing_detail_queryset()` with prefetch matching ordering.
- Implemented `PublicListingDetailView` extending `DetailView` to serve partial or full HTML based on `X-Maison-Partial` header.
- Designed CSS responsive drawer and mobile layouts.
- Created `listing-detail.js` implementing desktop drawer progressive enhancement and gallery thumbnail switches.
- Added comprehensive unit and template tests for the selector, views, template logic, and accessibility details.

### Completion Notes List

- Implemented detailed selector `get_listing_detail_queryset` excluding `under_review` and prefetching ordered photos.
- Developed `PublicListingDetailView` returning template partials or full pages.
- Created templates for the detail page, panel, gallery, availability, agent block, cta, and report.
- Added drawer backdrop close, trap focus, Escape key support, inert outside elements, and focus restoration to card triggers.
- Implemented sticky CTA for mobile views.
- Created 14 unit and template tests passing 100%.

### File List

- `_bmad-output/implementation-artifacts/2-4-listing-detail-surface.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `apps/listings/selectors.py`
- `apps/listings/views.py`
- `apps/listings/urls.py`
- `templates/listings/browse.html`
- `templates/listings/detail.html`
- `templates/listings/includes/detail_panel.html`
- `templates/listings/includes/gallery.html`
- `templates/listings/includes/availability_block.html`
- `templates/listings/includes/commissionnaire_block.html`
- `templates/listings/includes/contact_cta.html`
- `templates/listings/includes/report_action.html`
- `static_src/js/listing-detail.js`
- `static_src/css/input.css`
- `static/css/app.css`
- `apps/listings/tests/test_detail_selectors.py`
- `apps/listings/tests/test_detail_views.py`
- `apps/listings/tests/test_detail_templates.py`
- `apps/listings/tests/test_detail_accessibility.py`
