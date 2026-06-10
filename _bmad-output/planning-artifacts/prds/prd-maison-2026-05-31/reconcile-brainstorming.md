# Input Reconciliation — Brainstorming Session

## Source

`_bmad-output/brainstorming/brainstorming-session-2026-05-30-144517.md`

## Coverage Summary

The PRD preserves the brainstorming session's central product thesis: Maison is a rental-first marketplace that helps Tenants search faster and gives Commissionnaires attributable demand through a tracked WhatsApp Handoff.

### Must-Have Coverage

- Catalogue with scannable cards, price, Commune, bedroom count, real photos, and details: covered by FR-1, FR-3, and FR-5.
- Base filters for Commune, budget, and bedrooms: covered by FR-2.
- Commissionnaire publication with media: covered by FR-4 and FR-5.
- Tracked WhatsApp contact with Lead creation: covered by FR-7 through FR-9.
- Selective Verification Badge: covered by FR-12.
- Listing or Commissionnaire reporting: covered by FR-13.

### Should-Have Coverage

- Commissionnaire Listing and Lead management: covered by FR-6 and FR-10.
- Basic Lead Status: covered by FR-10 with an explicit assumption.
- Commissionnaire Profile: covered by FR-4.
- Listing view count: covered by FR-14 with an explicit assumption.
- Simple moderation: covered by FR-11 through FR-13.

### Deferred Scope Coverage

- Systematic video, advanced Lead distribution, rich Commissionnaire reputation, sophisticated duplicate handling, and agency workflows are explicitly out of scope in §10.2.

## Gaps And Tensions

1. The Verification Checklist needs an operational definition before the Verification Badge is implementation-ready.
2. Listing freshness needs a reconfirmation period.
3. The brainstorming source emphasized Commissionnaire response speed. The PRD now proposes measuring Lead Status transition to `contacted`, but this depends on Commissionnaire discipline and requires confirmation.
4. The desired reassuring visual tone belongs in the downstream UX specification; it is intentionally not over-specified in the PRD.

## Verdict

No brainstorming Must Have was silently dropped. The remaining gaps are explicit Open Questions or assumptions in the PRD.
