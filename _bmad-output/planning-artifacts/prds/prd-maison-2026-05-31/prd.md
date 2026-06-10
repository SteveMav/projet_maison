---
title: "Maison Rental Marketplace PRD"
status: draft
created: 2026-05-31
updated: 2026-05-31
---

# PRD: Maison Rental Marketplace

## 0. Document Purpose

This PRD defines the first public validation release of Maison, a rental-first real-estate marketplace for Kinshasa. It is intended to guide UX design, architecture, and epic and story creation. It translates the product thesis into grouped features with stable Functional Requirement IDs, explicit assumptions, measurable Success Metrics, and an operationally credible MVP boundary. Technical implementation notes and market observations that do not belong in the product contract live in `addendum.md`.

## 1. Vision

Finding a rental in Kinshasa should not require tenants to spend days chasing scattered, stale, or unclear listings. Maison gives tenants a fast way to scan rental options, narrow the search to relevant homes, and move into a WhatsApp conversation with a commissionnaire who can help arrange the next step.

Maison is not only a listings website. Its initial product thesis is that a local marketplace can create value on both sides by turning informal inventory into a structured search experience and turning tenant intent into traceable leads for commissionnaires. The platform does not attempt to control the complete offline transaction. It captures the point where a tenant's interest becomes commercially actionable.

Trust must be earned without overpromising. Maison distinguishes Listings that meet a publication standard from Verified Listings that have passed an additional review. It gives tenants visible signals, reporting tools, and clear availability information while keeping the verification promise operationally realistic.

**Launch posture:** [ASSUMPTION: Maison v1 is a public validation launch, not a private prototype.]

## 2. Product Thesis And Strategic Choices

### 2.1 Core Bet

If Maison makes rental discovery faster for Tenants and reliably attributes qualified demand to Commissionnaires, Commissionnaires will contribute useful Inventory and Tenants will initiate more relevant conversations.

### 2.2 Chosen Trade-offs

- **Rental first:** prioritize rental search before sales, short stays, or property management.
- **Kinshasa first:** [ASSUMPTION: the launch geography is limited to Kinshasa.]
- **Mobile-first web:** [ASSUMPTION: the launch Product Surface is a responsive web application optimized for mobile devices.]
- **Tracked handoff, not transaction control:** capture a Lead before handing the Tenant to WhatsApp; do not attempt to manage visits, negotiation, payment, or contract execution in v1.
- **Selective Verification:** show the Verification Badge only when the specific Listing has passed the Verification Checklist.
- **Lead attribution before property exclusivity:** the same Property may appear through multiple Commissionnaires. v1 preserves the origin of each Lead instead of attempting to establish exclusive Property ownership.
- **Quality before catalogue breadth:** [ASSUMPTION: when volume conflicts with trust, the MVP prioritizes publication quality and credible availability over the largest possible Inventory.]

## 3. Target Users

### 3.1 Primary Users

#### Tenant

A person searching for a rental home in Kinshasa who wants to reduce wasted time and quickly identify realistic options.

**Jobs To Be Done**

- Scan the essential details of a Listing without opening every page.
- Narrow Inventory by location, budget, and bedroom count.
- Understand whether a Listing is credible enough to pursue.
- Reach the relevant Commissionnaire through a familiar channel.
- Report suspicious or stale content when the experience does not match the Listing.

#### Commissionnaire

An independent local intermediary who knows available rental Inventory and wants qualified prospective tenants rather than visibility alone.

**Jobs To Be Done**

- Publish a Listing quickly from a mobile device.
- Receive attributable tenant interest.
- Understand which Listing generated a Lead.
- Avoid repeated enquiries for a Listing that is no longer available.
- Build a minimum level of credibility on the platform.

### 3.2 Supporting User

#### Moderator

An internal operator responsible for publication quality, selective Verification, and Report handling.

### 3.3 Non-Users In v1

- Property buyers and sellers.
- Short-stay guests and hosts.
- Agencies that need team workflows, portfolio administration, or revenue reporting.
- Owners seeking rent collection, contracts, or property-management tools.

### 3.4 Key User Journeys

#### UJ-1. Aline finds a credible rental option before spending her evening on calls

**Persona + context:** Aline is looking for an apartment in Kinshasa and wants to avoid contacting Commissionnaires about homes that do not fit her budget or are no longer available.

**Entry state:** Aline opens the mobile web Product Surface without being signed in.

**Path:**

1. She browses recent Listings and sets filters for Commune, monthly budget, and bedroom count.
2. She scans Listing Cards showing the price, Commune, bedrooms, primary photo, availability, and Verification Badge where applicable.
3. She opens a Listing Detail Page and reviews its media and additional details.
4. She taps the WhatsApp Contact Action.
5. She completes Lightweight Identification and is handed off to a WhatsApp conversation linked to that Listing and Commissionnaire.

**Climax:** Aline reaches a relevant Commissionnaire through WhatsApp with the Listing context already attached.

**Resolution:** Maison records a Lead with enough provenance to attribute the conversation.

**Edge case:** If the Listing becomes unavailable before contact, Aline sees that state and can return to filtered results rather than creating a new Lead.

#### UJ-2. Patrick publishes a useful rental Listing from his phone

**Persona + context:** Patrick is a Commissionnaire who wants tenant enquiries but does not want a lengthy administrative process.

**Entry state:** Patrick has a Commissionnaire Profile and opens the mobile web Product Surface.

**Path:**

1. He starts the publication flow.
2. He enters the required rental details and uploads real photos.
3. He previews the Listing Card and submits the Listing.
4. The Product Surface confirms whether the Listing is published, awaiting moderation, or requires correction.

**Climax:** Patrick gets a visible Listing that can generate attributed Leads.

**Resolution:** He can return later to change its Availability Status.

**Edge case:** If mandatory information or usable media is missing, Maison prevents publication and identifies the fields to correct.

#### UJ-3. Mireille selectively verifies a Listing without promising more than operations can support

**Persona + context:** Mireille is a Moderator protecting tenant trust while keeping Inventory publication practical.

**Entry state:** Mireille opens the moderation queue.

**Path:**

1. She opens a submitted Listing and reviews its required information and media.
2. She corrects permitted editorial issues, requests changes, rejects the Listing, or publishes it without a Verification Badge.
3. When the Verification Checklist is fully satisfied, she marks the Listing as verified.
4. Maison displays the Verification Badge only for that Listing.

**Climax:** Mireille can make the trust signal specific and defensible.

**Resolution:** The Listing has an auditable moderation state and, where earned, a Verification Badge.

#### UJ-4. Serge reports a suspicious Listing

**Persona + context:** Serge finds a Listing whose content appears misleading or stale.

**Entry state:** Serge is viewing a Listing Detail Page.

**Path:**

1. He opens the Report Action.
2. He selects a reason and optionally adds a short explanation.
3. Maison acknowledges the Report and places it in the moderation queue.

**Climax:** Serge has a simple way to signal a trust problem.

**Resolution:** A Moderator can review the Report and act on the Listing or Commissionnaire.

## 4. Glossary

- **Availability Status** — The current state of a Listing: `available`, `unavailable`, or `under_review`.
- **Commissionnaire** — A local intermediary who publishes Listings and receives Leads.
- **Commissionnaire Profile** — The minimum account identity and contact record required for a Commissionnaire to publish Listings.
- **Commune** — The Kinshasa administrative area used as the primary location filter in v1.
- **Inventory** — The set of Listings visible or under moderation in Maison.
- **Lead** — A timestamped record created when an identified Tenant initiates a WhatsApp Contact Action for a specific Listing and Commissionnaire.
- **Lightweight Identification** — The minimum Tenant information collected immediately before a WhatsApp Handoff. [ASSUMPTION: v1 collects name and phone number with consent, without requiring a password-based account.]
- **Listing** — A Commissionnaire's structured publication of a rental Property.
- **Listing Card** — The compact representation of a Listing used for rapid scanning in search results.
- **Listing Detail Page** — The expanded representation of a Listing with media, additional details, trust signals, and the WhatsApp Contact Action.
- **Moderator** — An internal operator who reviews Listings and Reports.
- **Product Surface** — The Maison responsive web application.
- **Property** — The physical rental home represented by one or more Listings.
- **Report** — A Tenant-submitted signal that a Listing or Commissionnaire may be suspicious, misleading, or stale.
- **Verification Badge** — A visible trust signal applied only to a Verified Listing.
- **Verification Checklist** — The operational review criteria a Moderator must satisfy before applying a Verification Badge.
- **Verified Listing** — A Listing that has passed the Verification Checklist.
- **WhatsApp Contact Action** — The action on a Listing Detail Page that creates a Lead and begins the WhatsApp Handoff.
- **WhatsApp Handoff** — The transition from Maison to a WhatsApp conversation with Listing context and Lead provenance.

## 5. Information Architecture

The MVP Product Surface contains:

- Home and recent Listings.
- Search results with filters.
- Listing Detail Page.
- Lightweight Identification step before WhatsApp Handoff.
- Commissionnaire Profile.
- Commissionnaire publication and Listing management.
- Commissionnaire Lead view.
- Moderator queue for Listings and Reports.

## 6. Features

### 6.1 Rental Inventory Discovery

**Description:** Tenants browse and filter rental Inventory through Listing Cards designed for rapid scanning. Listing Detail Pages expose additional context without slowing down initial comparison. Realizes UJ-1.

#### FR-1: Browse rental Listings

A Tenant can browse available rental Listings ordered by recency.

**Consequences (testable):**

- Search results display only Listings with Availability Status `available`.
- Each Listing Card displays monthly price, Commune, bedroom count, primary photo, and Verification Badge when applicable.
- Each Listing Card opens its Listing Detail Page.

#### FR-2: Filter rental Listings

A Tenant can narrow rental Listings by Commune, monthly budget range, and bedroom count.

**Consequences (testable):**

- Combining filters returns Listings satisfying every active filter.
- A Tenant can remove individual filters or clear all active filters.
- When no Listing matches, the Product Surface shows an explicit empty state.

#### FR-3: Review Listing details

A Tenant can review the information needed to decide whether to contact a Commissionnaire.

**Consequences (testable):**

- The Listing Detail Page displays all Listing Card fields, Listing media, description, Availability Status, and Commissionnaire Profile identity.
- The Listing Detail Page displays a WhatsApp Contact Action only while Availability Status is `available`.
- The Listing Detail Page displays the Report Action.

### 6.2 Commissionnaire Publication And Availability

**Description:** Commissionnaires contribute structured Inventory through a publication flow that is lightweight enough for mobile use while enforcing a minimum Listing standard. Realizes UJ-2.

#### FR-4: Create a Commissionnaire Profile

A Commissionnaire can create and maintain the minimum Profile required to publish Listings.

**Consequences (testable):**

- Maison requires a display name and reachable WhatsApp phone number before publication.
- Maison associates each submitted Listing with exactly one Commissionnaire Profile.
- A Commissionnaire can update Profile information without losing existing Listings or Leads.

#### FR-5: Submit a valid rental Listing

A Commissionnaire can submit a rental Listing that meets the publication standard.

**Consequences (testable):**

- Maison requires monthly price, Commune, bedroom count, description, Availability Status, and at least three photos before submission. [ASSUMPTION: three real photos are the minimum publication standard.]
- Maison rejects unsupported or unusable media and identifies what the Commissionnaire must correct.
- Maison stores the submission time and last update time.
- Each Listing is associated with exactly one Commissionnaire Profile.

#### FR-6: Maintain Listing Availability Status

A Commissionnaire can change a Listing's Availability Status after publication.

**Consequences (testable):**

- A Commissionnaire can mark a Listing as `unavailable`.
- A Listing marked `unavailable` disappears from search results and no longer exposes the WhatsApp Contact Action.
- Maison records the time of each Availability Status change.
- [ASSUMPTION: Maison prompts a Commissionnaire to reconfirm availability after a defined freshness period.]

### 6.3 Traceable WhatsApp Lead Handoff

**Description:** Maison converts tenant intent into a Lead immediately before opening WhatsApp. This creates a minimal attribution record without attempting to manage the full offline transaction. Realizes UJ-1.

#### FR-7: Identify a Tenant before handoff

A Tenant can complete Lightweight Identification before initiating a WhatsApp Handoff.

**Consequences (testable):**

- Maison explains that the submitted information is used to connect the Tenant with the Commissionnaire and attribute the enquiry.
- Maison requires explicit consent before creating a Lead.
- Maison blocks the WhatsApp Handoff until required Lightweight Identification fields are valid.

#### FR-8: Create an attributable Lead

Maison creates a Lead when an identified Tenant confirms the WhatsApp Contact Action.

**Consequences (testable):**

- The Lead records the Tenant identifier, Listing, Commissionnaire Profile, creation timestamp, and acquisition context available to Maison.
- Maison creates the Lead before opening WhatsApp.
- Repeated contact attempts remain distinguishable in event history even when they relate to the same Tenant and Listing.

#### FR-9: Hand off to WhatsApp with Listing context

Maison opens a WhatsApp conversation with the Commissionnaire after Lead creation.

**Consequences (testable):**

- The WhatsApp Handoff targets the phone number associated with the Listing's Commissionnaire Profile.
- The handoff includes a prefilled message identifying the Listing and a Lead reference. [ASSUMPTION: a human-readable Lead reference is included in the WhatsApp message.]
- Maison does not claim to track conversation contents, visits, negotiation, payment, or contract execution.

#### FR-10: View attributable Leads

A Commissionnaire can view the Leads attributed to their Listings.

**Consequences (testable):**

- A Commissionnaire sees only Leads associated with their own Commissionnaire Profile.
- Each Lead entry identifies the Listing and creation timestamp.
- [ASSUMPTION: v1 exposes a basic Lead Status with `new`, `contacted`, and `closed` values.]
- [ASSUMPTION: Maison timestamps Lead Status changes so the team can measure Commissionnaire response discipline without reading WhatsApp conversations.]

### 6.4 Selective Verification And Community Reporting

**Description:** Maison separates publication quality from stronger Verification. Moderators can apply a Verification Badge to individual Listings and respond to Reports. Realizes UJ-3 and UJ-4.

#### FR-11: Moderate submitted Listings

A Moderator can review Listing submissions and control whether they become visible.

**Consequences (testable):**

- A Moderator can publish, request correction, reject, or remove a Listing.
- Maison records the Moderator action, timestamp, and resulting moderation state.
- A Listing removed by a Moderator disappears from search results.

#### FR-12: Apply Verification selectively

A Moderator can apply or remove a Verification Badge for a specific Listing.

**Consequences (testable):**

- Maison displays the Verification Badge only when the Listing is marked as verified.
- Applying the Verification Badge requires completion of the Verification Checklist.
- Removing verified state removes the Verification Badge immediately.
- [ASSUMPTION: the initial Verification Checklist covers required-field review, media review, Commissionnaire contact confirmation, and an additional evidence check to be defined operationally.]

#### FR-13: Report a Listing or Commissionnaire

A Tenant can submit a Report from a Listing Detail Page.

**Consequences (testable):**

- A Report identifies the Listing and its associated Commissionnaire Profile.
- A Tenant selects a reason and can provide optional notes.
- Maison confirms Report receipt without exposing internal moderation details.
- A Moderator can review and resolve the Report.

### 6.5 Basic Trust Signals

**Description:** Maison provides modest, defensible trust signals that help Tenants decide whether to pursue a Listing without creating a false guarantee.

#### FR-14: Display trust signals

A Tenant can distinguish basic publication information from stronger Verification.

**Consequences (testable):**

- A Verified Listing displays the Verification Badge consistently on its Listing Card and Listing Detail Page.
- An unverified Listing never displays the Verification Badge.
- The Listing Detail Page displays its last update time.
- [ASSUMPTION: the MVP displays a Listing view count as a secondary trust signal.]

## 7. Cross-Cutting Non-Functional Requirements

### NFR-1: Mobile usability

- The Product Surface must support the Tenant and Commissionnaire journeys on current mobile browsers without requiring a native application.

### NFR-2: Performance

- [ASSUMPTION: search results should become usable within 3 seconds on a typical mobile connection in Kinshasa under expected MVP load.]
- The WhatsApp Contact Action must not open WhatsApp until Lead creation succeeds or Maison presents a recoverable error.

### NFR-3: Privacy and access control

- Maison must collect only the Tenant and Commissionnaire data required for the defined journeys.
- A Commissionnaire must not view Leads attributed to another Commissionnaire Profile.
- Moderator-only actions must require Moderator access.
- Maison must record consent for Lightweight Identification.

### NFR-4: Auditability

- Maison must retain timestamps and actor identity for Listing moderation, Verification Badge changes, Availability Status changes, and Report resolution.

### NFR-5: Reliability

- A failed WhatsApp Handoff must not silently discard the Lead creation outcome.
- A Tenant must receive a recoverable error state if Lead creation fails.

## 8. Constraints And Guardrails

### 8.1 Trust Guardrails

- Never state or imply that every Listing is verified.
- Never use the Verification Badge for a Listing that has not completed the Verification Checklist.
- Do not imply that a Verification Badge guarantees the outcome of an offline transaction.

### 8.2 Marketplace Guardrails

- The same Property may be represented by multiple Listings from different Commissionnaires.
- v1 does not attempt sophisticated duplicate detection or exclusive ownership adjudication.
- Lead attribution must preserve the Commissionnaire Profile selected by the Tenant's Listing path.

### 8.3 Data Guardrails

- Tenant contact data must be used only for the Lead and marketplace-operational purposes disclosed at Lightweight Identification.
- Sensitive operational notes and moderation evidence must not appear on public Listing Detail Pages.

## 9. Non-Goals

- Becoming a general real-estate portal for rentals, sales, and short stays in v1.
- Managing offline visits, negotiation, payment, contracts, deposits, or rent collection.
- Providing an agency CRM or property-management suite.
- Guaranteeing Property availability or transaction success.
- Building sophisticated Property deduplication or cross-Commissionnaire conflict resolution.
- Ranking or auctioning Leads among Commissionnaires.
- Launching a native mobile application.

## 10. MVP Scope

### 10.1 In Scope

- Kinshasa rental Inventory.
- Mobile-first responsive web Product Surface.
- Listing Cards, Listing Detail Pages, and search filters.
- Commissionnaire Profile and mobile-friendly publication.
- Availability Status updates.
- Lightweight Identification and traceable WhatsApp Handoff.
- Basic Commissionnaire Lead view.
- Listing moderation, selective Verification Badge, and Reports.
- Last-update time and [ASSUMPTION: Listing view count].

### 10.2 Out Of Scope For MVP

- Sales and short stays.
- Systematic Listing video requirements.
- Advanced Lead ranking or distribution.
- Rich Commissionnaire reputation scoring.
- Sophisticated duplicate detection.
- Agency and partner workflows.
- Property-management capabilities.

## 11. Success Metrics

Targets must be confirmed before implementation planning. The MVP must instrument the definitions below from launch.

### Primary

- **SM-1: Attributed Lead creation rate** — percentage of Listing Detail Page visits that produce a Lead through the WhatsApp Contact Action. Validates FR-7, FR-8, and FR-9.
- **SM-2: Useful Inventory freshness** — percentage of visible Listings reconfirmed as available within the agreed freshness period. Validates FR-6.

### Secondary

- **SM-3: Search-to-detail engagement** — percentage of search-result sessions that open at least one Listing Detail Page. Validates FR-1, FR-2, and FR-3.
- **SM-4: Valid Listing submission rate** — percentage of publication attempts that produce a Listing eligible for moderation without correction. Validates FR-5.
- **SM-5: Verification coverage** — percentage of visible Listings with a Verification Badge, reported alongside verification turnaround time. Validates FR-12.
- **SM-6: Report rate and resolution time** — Reports per 100 visible Listings and median time to Moderator resolution. Validates FR-13.
- **SM-7: Commissionnaire response discipline** — percentage of Leads moved to Lead Status `contacted` and median time from Lead creation to that change. Validates FR-10.

### Counter-Metrics

- **SM-C1: Stale-contact rate** — percentage of Leads created for Listings subsequently found unavailable. Prevents optimization of Lead volume at the expense of Inventory freshness.
- **SM-C2: Report-confirmation rate** — percentage of Reports that lead to corrective Moderator action. Prevents optimization of Inventory volume at the expense of trust.
- **SM-C3: Commissionnaire publication burden** — median time to submit a valid Listing. Prevents quality controls from making supply contribution impractical.

## 12. Risks And Mitigations

| Risk | Why it matters | MVP mitigation |
|---|---|---|
| Stale Listings | Tenants lose trust quickly when contact attempts waste time. | Availability Status, freshness reconfirmation, last-update display, and Reports. |
| Verification overpromise | A badge can damage trust if its meaning is vague or operationally inconsistent. | Selective Verification Badge, explicit Verification Checklist, and Moderator audit trail. |
| Commissionnaire adoption friction | Inventory will remain thin if publication feels administrative. | Mobile-friendly publication standard with a limited mandatory field set. |
| Lead attribution disputes | Multiple Commissionnaires may carry the same Property. | Timestamped Lead tied to the selected Listing and Commissionnaire Profile. |
| WhatsApp dependency | Maison cannot observe the full downstream journey. | Treat handoff as the measurable conversion boundary and avoid claims beyond it. |
| Catalogue-quality trade-off | More Listings can increase noise instead of usefulness. | Prioritize valid Listings and visible freshness over uncontrolled volume. |

## 13. Open Questions

1. Is the MVP a public validation launch, an investor/demo prototype, or an internal experiment?
2. Is Kinshasa the only launch geography?
3. Is mobile-first responsive web the only launch Product Surface?
4. When catalogue breadth conflicts with quality and response speed, which operating priority wins?
5. What exact fields and evidence satisfy the Verification Checklist?
6. What freshness period triggers Commissionnaire availability reconfirmation?
7. Are three photos the correct minimum publication standard?
8. Does Lightweight Identification require name and phone number only, or additional information?
9. Should Lead Status be included in MVP, and if so which values are operationally useful?
10. Should Listing view count be public in MVP?
11. What launch targets should apply to SM-1 through SM-6?
12. Who performs Moderator duties at launch, and what turnaround time is realistic?
13. Is manual Lead Status sufficiently reliable to measure Commissionnaire response discipline during the MVP?

## 14. Assumptions Index

- §1 — Maison v1 is a public validation launch, not a private prototype.
- §2.2 — Launch geography is limited to Kinshasa.
- §2.2 — Launch Product Surface is a responsive web application optimized for mobile devices.
- §2.2 — Publication quality and credible availability take priority over maximum Inventory volume.
- §4 — Lightweight Identification collects name and phone number with consent without requiring a password-based account.
- §6.2 FR-5 — Three real photos are the minimum publication standard.
- §6.2 FR-6 — Maison prompts Commissionnaires to reconfirm availability after a defined freshness period.
- §6.3 FR-9 — A human-readable Lead reference is included in the WhatsApp message.
- §6.3 FR-10 — Basic Lead Status values are `new`, `contacted`, and `closed`.
- §6.3 FR-10 — Maison timestamps Lead Status changes to measure Commissionnaire response discipline without reading WhatsApp conversations.
- §6.4 FR-12 — The initial Verification Checklist covers required-field review, media review, Commissionnaire contact confirmation, and an additional operational evidence check.
- §6.5 FR-14 — The MVP displays a Listing view count as a secondary trust signal.
- §7 NFR-2 — Search results should become usable within 3 seconds on a typical mobile connection in Kinshasa under expected MVP load.
