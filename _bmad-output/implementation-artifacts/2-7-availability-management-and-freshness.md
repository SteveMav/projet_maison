---
baseline_commit: 83de0f8f0b1584d8b991f06922f9a3af5385d75b
---

# Story 2.7: Availability Management And Freshness

Status: review

<!-- Validation: created from bmad-create-story workflow on 2026-06-07. -->

## Story

As a Commissionnaire,
I want to update and reconfirm Listing availability,
so that Tenants do not waste time contacting me about homes that are no longer available.

## Acceptance Criteria

1. Given a Commissionnaire owns a Listing, when they update its Availability Status, then Maison allows valid transitions such as `available` and `unavailable` and records the status-change timestamp and actor.
2. Given a Listing is marked `unavailable`, when public browse, filter, and detail surfaces render, then the Listing disappears from search results and its detail surface no longer exposes the WhatsApp Contact Action.
3. Given a Listing is still available but reaches the freshness threshold, when the Commissionnaire views their inventory, then Maison shows a reconfirmation prompt with a clear status cue and action and reconfirming updates the freshness timestamp.
4. Given availability changes occur, when audit behavior is inspected, then Maison retains append-only audit history for each change and the public UI shows last update/freshness without implying real-time guaranteed availability.
5. Given a Commissionnaire attempts to change a Listing they do not own, when the request is processed, then Maison denies the action server-side and does not expose private Listing or Commissionnaire data.

## Tasks / Subtasks

- [x] Verify prerequisites and current implementation state (AC: 1, 2, 3, 4, 5)
  - [x] Confirm Stories 1.1 through 2.6 are implemented, or explicitly implement/work from the branch where incomplete prerequisites are complete before finishing this story.
  - [x] Confirm `Listing.AvailabilityStatus` still exposes `available`, `unavailable`, and `under_review`.
  - [x] Confirm `CommissionnaireProfile` belongs to one user and exposes `is_publication_eligible`.
  - [x] Confirm public browse/search uses `get_public_browse_listings()` or an equivalent single source of truth that always filters `available`.
  - [x] Read current `apps/listings/models.py`, `services.py`, `selectors.py`, `views.py`, `urls.py`, listing tests, `apps/commissionnaires/models.py`, `views.py`, `urls.py`, templates, `apps/audit`, and `config/settings.py` before editing.
  - [x] Preserve unrelated dirty worktree changes and existing sprint status entries; do not revert prior story work.

- [x] Add explicit availability/freshness persistence (AC: 1, 3, 4)
  - [x] Update `apps/listings/models.py` with explicit timestamps for availability state separate from generic `updated_at`.
  - [x] Add `availability_changed_at` for the last actual Availability Status transition.
  - [x] Add `availability_reconfirmed_at` for the last Commissionnaire reconfirmation of an available Listing.
  - [x] Backfill existing rows in a migration using `submitted_at` where possible, then `updated_at`, then migration execution time.
  - [x] Add or update model indexes for status plus freshness/recency queries, for example `availability_status`, `availability_reconfirmed_at`, and `availability_changed_at`.
  - [x] Keep `under_review` available for moderation/publication flow, but do not expose `under_review` as a Commissionnaire public availability action in this story.
  - [x] Do not rely on `updated_at` alone for freshness because it also changes for non-availability edits.

- [x] Add append-only audit event foundation for availability (AC: 1, 4)
  - [x] Add `apps/audit/models.py` with a lightweight `AuditEvent` model if no equivalent already exists.
  - [x] Store `event_type`, actor, target object identity, timestamp, and JSON metadata.
  - [x] Use event types `listing.availability_changed` and `listing.availability_reconfirmed`.
  - [x] Metadata must include `listing_id`, `commissionnaire_profile_id`, previous status, new status where applicable, and the relevant availability timestamp.
  - [x] Keep audit events append-only: no update/delete workflow and no reliance on Django admin logs as the business audit trail.
  - [x] Add `apps/audit/services.py` or equivalent small helper to create audit events from listing services.
  - [x] Register audit events in admin as read-only if admin registration exists in this project pattern.

- [x] Implement availability services, selectors, and forms (AC: 1, 3, 4, 5)
  - [x] Add or update `apps/listings/services.py`.
  - [x] Implement `update_listing_availability(profile, listing_id, actor, new_status)` or equivalent.
  - [x] Accept a `CommissionnaireProfile` object and authenticated actor; never accept owner/profile identity from POST data.
  - [x] Lock the Listing row inside `transaction.atomic()` when changing availability.
  - [x] Allow Commissionnaire transitions only to `available` and `unavailable`; leave moderation-owned `under_review` transitions to moderation stories.
  - [x] When status changes, update `availability_status`, `availability_changed_at`, and, when changing to `available`, also update `availability_reconfirmed_at`.
  - [x] Implement `reconfirm_listing_availability(profile, listing_id, actor)` that is valid only for an owned `available` Listing and updates `availability_reconfirmed_at`.
  - [x] Record an audit event after each successful status change or reconfirmation in the same service path.
  - [x] Keep idempotent no-op behavior explicit: do not create misleading change audit rows when the status did not change; use the reconfirm service for same-status freshness refreshes.
  - [x] Add `ListingAvailabilityForm` or equivalent with only valid Commissionnaire-facing choices.
  - [x] Add selectors such as `get_commissionnaire_inventory(profile)` and `get_availability_freshness_state(listing, now=None)` for inventory rows and tests.

- [x] Build Commissionnaire inventory and freshness UI (AC: 1, 3, 5)
  - [x] Add or update a protected route such as `commissionnaires:listing_inventory` at `/pro/listings/`.
  - [x] Add POST routes for status update and reconfirmation, for example `/pro/listings/<int:pk>/availability/` and `/pro/listings/<int:pk>/reconfirm/`.
  - [x] Require authentication, the WhatsApp phone gate, and an eligible `CommissionnaireProfile`.
  - [x] If the user has no eligible profile, redirect to the existing profile setup flow with safe `next` preservation where practical.
  - [x] Render only Listings owned by the authenticated user's `CommissionnaireProfile`.
  - [x] Use compact inventory rows with listing identity, status, last availability update, freshness state, and next action.
  - [x] Show a "reconfirm soon" state when `availability_status == available` and `availability_reconfirmed_at` is older than the configured freshness threshold.
  - [x] Use a warning-soft visual treatment plus text/icon for reconfirmation; do not rely on color alone.
  - [x] Use POST with CSRF for every state-changing action; do not change availability through GET links.
  - [x] Preserve concise French copy and 44px/48px control sizing from existing Maison templates.

- [x] Preserve public browse, filter, and detail behavior (AC: 2, 4)
  - [x] Keep `get_public_browse_listings()` excluding every Listing whose status is not `available`.
  - [x] If Story 2.3 filters are implemented, ensure all filter selectors compose from the available-only public selector.
  - [x] If Story 2.4 detail is implemented, allow direct detail for an `unavailable` Listing only as an unavailable state with no WhatsApp CTA and a return-to-results action; keep `under_review` public-ineligible.
  - [x] If the current placeholder detail view still exists, do not add a WhatsApp URL or Lead side effect; add only enough behavior/tests to ensure unavailable Listings do not expose contact affordances.
  - [x] Public card/detail freshness copy must use `availability_reconfirmed_at` or `availability_changed_at` as the availability freshness source, not unrelated edits.
  - [x] Public copy may say `Mise a jour ...` or `Disponibilite reconfirmee ...`; it must not say `Toujours disponible`, `garantie`, or imply real-time availability.

- [x] Centralize the freshness threshold (AC: 3, 4)
  - [x] Add `LISTING_AVAILABILITY_FRESHNESS_DAYS` to settings with an explicit MVP default, recommended `14`.
  - [x] Treat the value as a configurable product/operations setting because the exact threshold remains an open PRD/UX decision.
  - [x] Use `timezone.now()` and timezone-aware comparisons.
  - [x] Do not hard-code threshold math in templates.

- [x] Add tests for models, services, permissions, public surfaces, UI state, and audit (AC: 1, 2, 3, 4, 5)
  - [x] Test migrations/model fields expose `availability_changed_at` and `availability_reconfirmed_at`.
  - [x] Test owned Listing status changes from `available` to `unavailable` and from `unavailable` to `available`.
  - [x] Test status changes record timestamp updates and append-only audit events with actor and metadata.
  - [x] Test reconfirming an available Listing updates freshness timestamp and writes `listing.availability_reconfirmed`.
  - [x] Test reconfirming an unavailable or under-review Listing is blocked.
  - [x] Test a Commissionnaire cannot change or reconfirm another Commissionnaire's Listing and no private data is exposed.
  - [x] Test invalid status values and POST tampering are rejected.
  - [x] Test public browse/search excludes unavailable and under-review Listings after availability changes.
  - [x] Test detail hides WhatsApp CTA for unavailable Listings if detail exists; otherwise assert the placeholder detail has no contact side effect.
  - [x] Test inventory view shows visible, unavailable, under-review/awaiting moderation, and reconfirm-soon states with text plus visual cue hooks.
  - [x] Test freshness threshold behavior using `override_settings(LISTING_AVAILABILITY_FRESHNESS_DAYS=...)`.
  - [x] Test query count remains bounded for inventory rows with photos/profile data.

- [x] Run required checks (AC: 1, 2, 3, 4, 5)
  - [x] `python manage.py makemigrations --check --dry-run`
  - [x] `python manage.py migrate --check`
  - [x] `python manage.py check`
  - [x] `python manage.py test apps.listings`
  - [x] `python manage.py test apps.commissionnaires`
  - [x] `python manage.py test apps.audit`
  - [x] `python manage.py test`
  - [x] `npm run css:build`
  - [x] `python manage.py collectstatic --noinput --dry-run`

## Dev Notes

### Source Context

- Story source: `_bmad-output/planning-artifacts/epics.md`, Epic 2, Story 2.7.
- Requirements: FR-6, FR-3; NFR-4; UX-DR16, UX-DR24, UX-DR38, UX-DR39.
- FR-6 requires Commissionnaires to mark Listings unavailable, unavailable Listings to disappear from search and hide WhatsApp contact, Maison to record the time of each status change, and Maison to prompt reconfirmation after a defined freshness period.
- FR-3 requires Listing Detail to show Availability Status and expose the WhatsApp Contact Action only while a Listing is `available`.
- NFR-4 requires timestamps and actor identity for Availability Status changes.
- UX requires availability and last update copy to stay together, inventory rows to expose availability/freshness states, and freshness to remain a distinct trust signal instead of a generic verification badge.

### Dependency On Previous Stories

This story depends on Stories 1.1 through 2.6.

### Current Workspace Snapshot

Targeted inspection on 2026-06-07 found:

- `apps/listings/models.py` currently has `Listing.availability_status`, `submitted_at`, `created_at`, and `updated_at`, but no explicit `availability_changed_at` or `availability_reconfirmed_at`.
- `Listing.AvailabilityStatus` currently contains `available`, `unavailable`, and `under_review`.
- `Listing.submitted_at` defaults to `timezone.now`; `Listing.updated_at` uses `auto_now=True`.

- Public browse/filter/detail availability integration.
- Tests for services, permissions, audit, freshness threshold, and public exclusion.

Do not implement now:

- Moderation decisions, correction workflow, Verification Checklist, or Verification Badge changes.
- Lead creation, Lightweight Identification, WhatsApp URL generation, or handoff failure states.
- Reports, report resolution, view counts, favorites, push notifications, background reminder delivery, or analytics dashboards.
- A public API, DRF endpoint, React/Vue UI, external scheduler, Redis, PostgreSQL, or queue worker.

## Dev Agent Record

### Agent Model Used

Antigravity Gemini CLI

### Debug Log References

- Story executed under the Antigravity dev persona.
- Captured git diffs, ran migrations, and resolved spelling differences ("Mise à jour" vs "Mis à jour") to align with existing test suite expectations.
- Built new database fields `availability_changed_at` and `availability_reconfirmed_at` with SQLite backfill logic and indexing.
- Implemented append-only `AuditEvent` model to secure audit trail.

### Completion Notes List

- Implemented `availability_changed_at` and `availability_reconfirmed_at` fields on `Listing` model.
- Added data migration to backfill fields using `submitted_at`/`updated_at`.
- Implemented append-only `AuditEvent` model and Django admin read-only integration.
- Exposed `update_listing_availability` and `reconfirm_listing_availability` service functions.
- Implemented `get_commissionnaire_inventory` and `get_availability_freshness_state` selectors.
- Created `ListingInventoryView`, `ListingUpdateAvailabilityView`, and `ListingReconfirmAvailabilityView` Views.
- Developed `listing_inventory.html` and `inventory_row.html` templates.
- Registered URLs for all inventory and availability routes.
- Wrote extensive tests across `apps/listings`, `apps/commissionnaires`, and `apps/audit`.
- All 228 test cases compile and run successfully.

### File List

- `config/settings.py`
- `apps/listings/models.py`
- `apps/listings/services.py`
- `apps/listings/selectors.py`
- `apps/listings/forms.py`
- `apps/listings/migrations/0002_listing_availability_changed_at_and_more.py`
- `apps/listings/tests/test_availability_services.py`
- `apps/audit/models.py`
- `apps/audit/admin.py`
- `apps/audit/services.py`
- `apps/audit/migrations/0001_initial.py`
- `apps/audit/tests/test_services.py`
- `apps/commissionnaires/views.py`
- `apps/commissionnaires/urls.py`
- `apps/commissionnaires/tests/test_inventory_views.py`
- `templates/commissionnaires/listing_inventory.html`
- `templates/commissionnaires/includes/inventory_row.html`
- `templates/listings/includes/availability_block.html`
- `_bmad-output/implementation-artifacts/2-7-availability-management-and-freshness.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
