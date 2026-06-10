---
name: Maison
status: final
updated: 2026-06-01
sources:
  - ../../../../PRODUCT.md
  - DESIGN.md
  - ../../prds/prd-maison-2026-05-31/prd.md
  - ../../../brainstorming/brainstorming-session-2026-05-30-144517.md
  - imports/design/README.md
  - imports/design/index.html
  - imports/design/styles.css
  - imports/design/app.js
  - imports/design/STITCH-REVIEW.md
  - imports/design/stitch-imports/detail-ngaliema/screen.html
  - imports/design/stitch-imports/detail-ngaliema/screen.png
---

# Maison Experience Spine

## Foundation

Maison is a mobile-first responsive web marketplace for Kinshasa rentals. It helps tenants scan credible options quickly and continue through a familiar WhatsApp conversation while preserving Lead provenance. Commissionnaires use the same responsive product to publish inventory, maintain freshness, and understand attributable demand. Moderators protect publication quality and apply verification selectively.

`DESIGN.md` owns visual identity. This document owns information architecture, behavior, states, interactions, accessibility, and journeys.

No production UI system is named yet. The framework-free local prototype deliberately leaves implementation architecture open.

The local [prototype](imports/design/index.html), its [behavior layer](imports/design/app.js), the [source map](imports/design/README.md), the [Stitch reconciliation](imports/design/STITCH-REVIEW.md), and the imported Stitch detail [screenshot](imports/design/stitch-imports/detail-ngaliema/screen.png) illustrate decisions. The spines win if a mock conflicts with these documents.

## Product Experience Principles

1. **Fast scan before deep reading.** A tenant should reject irrelevant listings without opening each detail screen.
2. **Trust through evidence, not slogans.** Verification, freshness, reporting, and moderation are distinct signals.
3. **WhatsApp is a measured boundary.** Maison creates the Lead before handoff but does not claim to observe the conversation.
4. **Quality beats catalogue theater.** Stale or unclear inventory is more damaging than a smaller catalogue.
5. **Commissionnaire discipline needs visible value.** Freshness updates and Lead status changes must clearly reduce wasted effort or improve response quality.

## Information Architecture

### Public Tenant Surfaces

| Surface | Reached From | Purpose | MVP |
|---|---|---|---|
| Browse home | Product open | Scan recent available rentals and understand Maison's trust posture | Yes |
| Filtered results | Browse search and filters | Narrow by Commune, budget, and bedroom count | Yes |
| Listing detail | Listing card | Review media, price, facts, freshness, commissionnaire identity, and verification where earned | Yes |
| Lightweight identification | WhatsApp CTA | Collect minimum tenant identity and consent before Lead creation | Yes |
| WhatsApp handoff result | Identification success or failure | Open WhatsApp only after Lead success; recover cleanly on failure | Yes |
| Report form | Listing detail | Submit a suspicious, misleading, or stale Listing signal | Yes |
| Favorites | Header or mobile navigation | Save listings for later comparison | Useful follow-on; prototype placeholder |

### Commissionnaire Surfaces

| Surface | Reached From | Purpose | MVP |
|---|---|---|---|
| Commissionnaire overview | `Espace pro` | See inventory freshness, new Leads, and response discipline | Yes |
| My listings | Overview | Review visible, draft, under-review, and unavailable listings | Yes |
| Publication flow | `Publier un bien` | Create a valid listing from a phone | Yes |
| Listing preview | Publication flow | Review the future fast-scan card before submission | Yes |
| Lead list | Overview | See Leads attributed to the signed-in Commissionnaire Profile | Yes |
| Lead detail/status | Lead list | Review listing provenance and update basic status | `[ASSUMPTION]` Confirm for MVP |
| Profile maintenance | Overview | Maintain display name and WhatsApp number | Yes |

### Moderator Surfaces

| Surface | Reached From | Purpose | MVP |
|---|---|---|---|
| Listing moderation queue | Moderator access | Publish, request correction, reject, or remove a listing | Yes |
| Verification checklist | Moderation detail | Apply or remove the badge for one specific listing | Yes |
| Report queue | Moderator access | Resolve suspicious or stale-content reports | Yes |
| Audit timeline | Moderation detail | See actor and timestamp history | Yes |

## Surface Coverage

| Surface | Visual Reference | Coverage |
|---|---|---|
| Browse home | Local prototype `imports/design/index.html`; Stitch project screen `Maison - Accueil et Recherche` | Mocked |
| Filtered results | Local prototype; Stitch project screen `États de recherche` | Mocked, including loading and empty |
| Listing detail | Stitch import `imports/design/stitch-imports/detail-ngaliema/screen.png`; local drawer prototype | Mocked and reconciled |
| Lightweight identification | Local prototype; Stitch project screen `Identification avant WhatsApp` | Mocked |
| WhatsApp handoff result | No final visual reference | Spine-only |
| Report form | No final visual reference | Spine-only |
| Favorites | Local prototype placeholder | Placeholder only; follow-on |
| Commissionnaire overview | Local prototype; Stitch project screen `Tableau de bord - Patrick Ilunga` | Mocked |
| My listings | Local prototype commissionnaire overview | Mocked as overview rows |
| Publication flow | Stitch project screen `Publier un bien` | Mocked in Stitch, needs final UX review |
| Listing preview | Publication flow reference | Partially mocked |
| Lead list | Local prototype commissionnaire overview | Mocked as overview rows |
| Lead detail/status | No final visual reference | Spine-only, `[ASSUMPTION]` pending MVP confirmation |
| Profile maintenance | No final visual reference | Spine-only |
| Listing moderation queue | No final visual reference | Spine-only |
| Verification checklist | No final visual reference | Spine-only |
| Report queue | No final visual reference | Spine-only |
| Audit timeline | No final visual reference | Spine-only |

## Trust Contract

Trust is layered. Do not collapse these concepts into a single badge.

| Signal | Meaning | Must Not Imply |
|---|---|---|
| Published listing | Required fields and usable media meet publication standard | Verification, guaranteed availability, guaranteed transaction |
| Last updated | Shows when availability information was most recently refreshed | Real-time availability |
| Verified listing | Listing passed an additional operational checklist | Guaranteed property outcome, legal guarantee, complete offline validation |
| View count | Secondary activity signal if retained in MVP | Popularity equals credibility |
| Report action | Tenant can surface misleading, suspicious, or stale content | Immediate enforcement or public accusation |

Canonical verified explanation:

> Cette annonce a passé un contrôle supplémentaire. Le badge ne garantit pas le résultat d'une transaction hors ligne.

The imported Stitch detail reference uses stronger copy about guaranteeing availability and accuracy. Do not use that generated wording.

## Voice And Tone

Use concise French UI copy. Maison is calm and direct. It does not manufacture urgency.

| Do | Don't |
|---|---|
| `Annonce vérifiée` | `100% garanti` |
| `Mise à jour hier` | `Toujours disponible` |
| `Disponibilité reconfirmée il y a 3 jours` | `Bien disponible immédiatement` unless operations support it |
| `Maison ne lit pas vos conversations WhatsApp.` | Imply downstream WhatsApp tracking |
| `Nous n'avons pas pu créer votre demande. Réessayez.` | Vague `Une erreur est survenue` without recovery |
| `Signaler cette annonce` | Publicly accuse the Commissionnaire |

## Component Patterns

Behavioral rules only. Visual rules live in `DESIGN.md.Components`.

| Component | Use | Behavioral Rules |
|---|---|---|
| Button primary | Global actions | Advance the main task. Support loading and disabled behavior where submission is possible. |
| Button secondary | Global actions | Keep supporting actions subordinate to the primary path. |
| Status chip | Cards and operational rows | Pair text with an icon where needed. Never rely on color alone. |
| Listing card | Browse and results | Whole card opens detail. Favorite remains independent. Show only `available` listings. |
| Search form | Browse | Combine Commune, budget range, and bedroom minimum. Preserve chosen values after refresh. |
| Filter chip | Filter panel | Removable individually. Clear-all remains reachable. Announce result-count updates. |
| Listing-shaped skeleton | Search loading | Match card geometry. Never replace the full page with a spinner. |
| Listing detail drawer | Desktop detail | Open above browse context. Trap focus, support Escape, restore focus on close, and make closed content inert. |
| Listing detail screen | Mobile detail | Full-screen surface with sticky bottom CTA and familiar Back behavior. |
| Gallery | Detail | Main `4:3` image, horizontal thumbnails, visible image count, usable alt text. |
| Availability block | Detail | Show status plus last-update timestamp. Hide contact CTA when unavailable. |
| Verification box | Detail | Appear only when verified. Use canonical narrow copy. |
| Commissionnaire block | Detail | Show profile identity and explain that WhatsApp contact follows lightweight identification. |
| Report action | Detail | Open reason selection with optional notes. Confirm receipt without exposing internal moderation. |
| Lightweight identification | WhatsApp handoff | Collect minimum required fields and explicit consent. Create Lead before opening WhatsApp. |
| Recoverable Lead error | Identification | Preserve inputs. Explain failure. Offer retry. Do not open WhatsApp. |
| Inventory row | Commissionnaire overview | Show moderation, availability, and freshness state. Surface reconfirmation action. |
| Lead row | Commissionnaire overview | Show tenant, originating listing, timestamp, and optional Lead status. Never show WhatsApp contents. |
| Publication stepper | Commissionnaire publication | Keep steps short and mobile-friendly. Identify correction fields precisely. |
| Verification checklist | Moderator detail | Require every operational checklist item before badge application. Record actor and timestamp. |

## State Patterns

### Tenant Discovery

| State | Surface | Treatment |
|---|---|---|
| Default browse | Browse home | Recent available listings ordered by recency |
| Filtering | Results | Card-shaped skeletons and live result-count announcement |
| Empty result | Results | `Aucune annonce ne correspond exactement.` plus one reset action |
| Listing available | Detail | Show availability, freshness, and WhatsApp CTA |
| Listing unavailable | Detail | Remove WhatsApp CTA; explain state and route back to filtered results |
| Listing under review | Public surfaces | Remove from visible public search |
| Verified | Card and detail | Shield icon plus explicit label; full explanation in detail |
| Published but unverified | Card and detail | No verified badge |
| Report submitted | Report flow | Thank the tenant and avoid revealing moderation internals |

### WhatsApp Handoff

| State | Surface | Treatment |
|---|---|---|
| Identification required | Lightweight identification | Name, phone number, consent, explanation |
| Invalid input | Identification | Inline field error below the relevant control |
| Creating Lead | Identification | Disable CTA, preserve content, show a short progress label |
| Lead created | Handoff result | Open WhatsApp with listing reference and human-readable Lead reference |
| Lead creation failed | Identification | Keep the form open, preserve values, offer retry |
| WhatsApp open failed | Handoff result | Explain that the Lead exists and provide a recoverable retry action |

### Commissionnaire Operations

| State | Surface | Treatment |
|---|---|---|
| Visible | Inventory row | Available to tenants |
| Reconfirm soon | Inventory row | Warm warning state and explicit reconfirmation action |
| Unavailable | Inventory row | Remove from public search and contact handoff |
| Draft | Inventory row | Explain incomplete fields or missing media |
| Awaiting moderation | Inventory row | Show submission timestamp and current moderation state |
| Correction required | Inventory row and publication | Identify fields to correct |
| Lead new | Lead row | Highest priority |
| Lead contacted | Lead row | Timestamp transition if Lead statuses remain in MVP |
| Lead closed | Lead row | Retain history without dominating active Leads |

### Moderator Operations

| State | Surface | Treatment |
|---|---|---|
| Submission queued | Moderation queue | Show age, Commissionnaire, listing summary |
| Publish without badge | Moderation detail | Allow ordinary publication when standard is met |
| Verify | Checklist | Require every checklist item |
| Request correction | Moderation detail | Capture actionable reason |
| Reject or remove | Moderation detail | Capture actor, timestamp, and reason |
| Report open | Report queue | Show reason and optional notes |
| Report resolved | Report queue | Record outcome without exposing private operational notes publicly |

### Access Control

| State | Surface | Treatment |
|---|---|---|
| Authentication required | Commissionnaire and Moderator surfaces | Preserve the attempted destination and route to authentication. Do not expose operational data before access is established. |
| Permission denied | Commissionnaire and Moderator surfaces | Explain that the account does not have access and offer a route back to a valid surface. Never reveal another Commissionnaire's Leads or private moderation data. |

## Interaction Primitives

- Tap or click a listing card to open detail without losing browse context.
- Keep favorite independent from card navigation.
- Use visible native-like selectors and chips for filters.
- Keep the WhatsApp CTA sticky in detail where it remains valid.
- Use `150–250ms` transitions for drawer, modal, hover, and pressed feedback.
- Use a subtle `scale(0.97)` pressed state for pressable controls.
- Avoid motion for repeated keyboard-driven actions.
- Respect reduced motion by removing positional movement while preserving comprehension.
- Do not animate layout dimensions where transform and opacity suffice.

## Accessibility Floor

- Meet WCAG 2.2 AA contrast for text, controls, and focus indicators.
- Keep tap targets at least `44px × 44px`.
- Preserve keyboard reachability and visible focus.
- Use text plus icons for verified, warning, selected, and error states.
- Do not rely on green versus terracotta alone.
- Trap focus inside open modals and drawers.
- Restore focus to the triggering element after close.
- Mark closed overlays inert so hidden controls cannot receive focus.
- Ensure gallery images have meaningful alt text in production.
- Announce result-count changes and form failures with an appropriate live region.
- Keep the mobile bottom navigation labels visible.

## Responsive And Platform

| Range | Requirements |
|---|---|
| `< 700px` | One-column listings, stacked search fields, bottom navigation, full-screen detail, sticky CTA |
| `700px–920px` | Two-column listings, compact navigation, comfortable touch spacing |
| `> 920px` | Three-column listings, desktop header, asymmetric browse hero, right-side detail drawer |

Current mobile browsers are the MVP target. No native application is required.

## Privacy And Access

- Collect only the tenant information required for Lead creation and disclosed marketplace operations.
- Record explicit consent for lightweight identification.
- A Commissionnaire sees only Leads attributed to their own Commissionnaire Profile.
- Moderator actions require Moderator access.
- Sensitive moderation notes and verification evidence never appear on public detail screens.
- Never imply access to WhatsApp conversation contents.

## Instrumentation

Instrument these experience boundaries from launch:

| Event | Purpose |
|---|---|
| Browse viewed | Establish discovery sessions |
| Filters applied or cleared | Understand narrowing behavior |
| Listing detail opened | Measure search-to-detail engagement |
| WhatsApp CTA tapped | Identify handoff intent |
| Lightweight identification submitted | Measure identification friction |
| Lead created | Measure attributable conversion |
| WhatsApp handoff attempted | Separate Lead success from external-app transition |
| Report submitted | Measure trust feedback |
| Availability changed | Measure freshness discipline |
| Listing reconfirmed | Measure useful inventory freshness |
| Lead status changed | Measure response discipline if retained |

## Inspiration & Anti-patterns

- **Lifted from familiar marketplace patterns:** image-first cards, native-like selectors, removable chips, a sticky detail CTA, and a lightweight sheet before an external handoff.
- **Rejected - dense generic property portals:** walls of listings with weak hierarchy slow down fast triage.
- **Rejected - luxury-property theatre:** glossy villas and aspirational polish can make ordinary rental inventory feel less credible.
- **Rejected - inflated fintech trust language:** verification claims must remain specific, selective, and reversible.
- **Rejected - neon startup dashboards and decorative card stacks:** operational surfaces should be compact, calm, and phone-friendly.
- **Rejected - silent WhatsApp tracking implication:** Maison measures the handoff boundary, not the private conversation.

## Key Flows

### UJ-1. Aline finds a credible rental option before spending her evening on calls

1. Aline opens Browse on her phone without signing in.
2. She filters by Commune, budget, and bedroom count.
3. She scans price, location, freshness, and selective verification directly on cards.
4. She opens the Ngaliema listing detail and reviews photos, facts, last update, and Patrick Ilunga's profile.
5. She taps `Contacter sur WhatsApp`.
6. Maison explains why her name and phone number are needed.
7. She enters lightweight identification and gives explicit consent.
8. Maison persists the Lead before attempting the external handoff.
9. **Climax:** WhatsApp opens with listing context and a human-readable Lead reference.

Failure: Lead creation fails. Maison preserves Aline's entries, explains the problem, and offers retry without opening WhatsApp.

Edge case: the listing becomes unavailable before contact. Maison removes the CTA and routes Aline back to her filtered results.

### UJ-2. Patrick publishes a useful rental Listing from his phone

1. Patrick opens `Espace pro`.
2. He taps `Publier un bien`.
3. He enters monthly price, Commune, bedroom count, description, and availability.
4. He uploads at least three real photos.
5. Maison identifies missing or unusable media precisely.
6. Patrick previews the fast-scan Listing Card.
7. He submits the Listing.
8. **Climax:** Maison confirms `Envoyée pour modération` and shows the next operational state.

Failure: photos are missing or unusable. Maison blocks submission and identifies the correction.

### UJ-3. Mireille selectively verifies a Listing without promising more than operations can support

1. Mireille opens the moderation queue.
2. She reviews required fields and media.
3. She chooses ordinary publication, correction request, rejection, or removal.
4. For stronger verification, she completes every operational checklist item.
5. **Climax:** Mireille applies the badge to this specific listing only.
6. Maison records actor, timestamp, and resulting state.

### UJ-4. Serge reports a suspicious Listing

1. Serge opens a listing detail.
2. He taps `Signaler cette annonce`.
3. He selects a reason and optionally adds notes.
4. Maison confirms receipt without exposing internal moderation.
5. **Climax:** The report enters the Moderator queue with listing and Commissionnaire provenance.

## Open Decisions

These product decisions remain explicit and should not be silently invented by the design agent:

1. Exact operational Verification Checklist, especially the additional evidence check.
2. Freshness period that triggers availability reconfirmation.
3. Whether three photos remain the exact minimum publication standard.
4. Whether public view count remains in MVP.
5. Whether manual Lead statuses `new`, `contacted`, and `closed` remain in MVP.
6. Moderator turnaround expectations at launch.
