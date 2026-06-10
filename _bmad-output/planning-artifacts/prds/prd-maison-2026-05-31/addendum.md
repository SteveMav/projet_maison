# Maison Rental Marketplace PRD Addendum

## Purpose

This addendum preserves implementation-adjacent and market-context notes that informed the PRD but do not belong in the product contract.

## Source Input

Primary discovery source:

- `_bmad-output/brainstorming/brainstorming-session-2026-05-30-144517.md`

The brainstorming session identified the product's central tension: Maison must create useful demand for Commissionnaires while preventing stale, low-quality Inventory from eroding Tenant trust.

## Market Context Snapshot

Reviewed on 2026-05-31:

- [Immo Congo](https://www.immocongo.org/) positions around manually reviewed Listings, moderation, protected contact disclosure, Verification Badges, and Reports.
- [SmartImmo](https://www.smartimmo-app.com/) exposes rental search, active Listings, agent positioning, qualified-lead language, WhatsApp links, and broader property-management tools.
- [Congo Ndaku](https://congondaku.com/) and [MaisonCongo](https://www.maisoncongo.com/about) were identified during discovery, but their public pages did not expose enough readable detail during extraction to support stronger claims here.

Product implication: Maison should not differentiate itself as another generic Listings catalogue. Its more specific thesis is fast rental discovery plus traceable Lead attribution for Commissionnaires in an informal Inventory market.

## Tracked WhatsApp Handoff Notes

The PRD specifies product behavior rather than an implementation mechanism. A practical implementation may:

1. Persist the Lead before redirecting out of Maison.
2. Generate a WhatsApp deep link targeting the Listing's Commissionnaire phone number.
3. Prefill a short message containing a Listing reference and a human-readable Lead reference.
4. Record the handoff event separately from the Lead record.

The platform should not imply that it can observe WhatsApp conversation contents or the downstream offline transaction.

## Verification Checklist Design Notes

The Verification Badge needs an operational definition before build planning. Candidate checks:

- Required Listing fields are complete and internally consistent.
- Listing media appears usable and relevant to the represented Property.
- The Commissionnaire contact route is reachable.
- Additional evidence supports a stronger claim than ordinary publication.

The final additional evidence check remains a PM and operations decision. Options may include a recent video, a moderator call, a location-specific proof, or another lightweight method that can be applied consistently.

## Deferred Concepts Worth Preserving

- Video as a stronger evidence mechanism where operations can support it.
- Rich Commissionnaire reputation and responsiveness signals.
- Duplicate and reuse detection across Commissionnaires.
- Advanced Lead distribution or ranking.
- Agency and partner workflows.
