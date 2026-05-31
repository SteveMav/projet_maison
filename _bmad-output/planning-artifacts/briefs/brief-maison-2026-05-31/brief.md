---
title: "Product Brief: Maison"
status: draft
created: 2026-05-31 11:04:08
updated: 2026-05-31 11:04:08
---

# Product Brief: Maison

## Executive Summary

Maison is a rental-first real estate marketplace for Kinshasa designed around how the market actually works today. Rather than starting from the assumption that landlords or tenants behave like users of a formal property portal, Maison starts with the local intermediaries already moving the market: commissionaires who source, filter, and close rentals through their personal networks.

The product’s first job is not to digitize every part of the transaction. Its job is to reduce search time for renters, create a reliable lead engine for commissionaires, and add trust signals to an opaque, fragmented market. The initial version focuses on high-quality listings, fast contact, lightweight lead attribution, and selective verification instead of broad but weak inventory.

## The Problem

Finding a rental home in Kinshasa is time-consuming, uncertain, and highly dependent on intermediaries. Renters often contact multiple commissionaires at once because searching alone across a large city is inefficient and unreliable. The real value they buy is speed, local filtering, and access to inventory that is not systematically available online.

On the supply side, commissionaires are not paid for searching. They are paid only when a deal closes. That means they will only adopt a platform if it brings them qualified demand fast enough to justify the effort of posting and maintaining listings. Traditional listing sites do not solve this well because they tend to become cluttered, stale, and low-trust.

## Who This Serves

### Primary Users

- **Renters in Kinshasa** who need to find a home quickly, filter by area and room count, and contact a relevant intermediary without wasting time.
- **Commissionaires** who already control meaningful local inventory and want more qualified inbound leads without giving up their role in the transaction.

### Secondary Users

- **Platform operators/admins** who review listings, manage trust signals, and keep the marketplace credible.

## The Solution

Maison is a mobile-friendly rental marketplace where commissionaires can publish listings and renters can discover homes quickly through clear, fast-scanning listing cards and simple filters. Each listing highlights the most decision-critical information immediately: price, commune, number of bedrooms, and real photos, with additional detail behind a “see more” view.

When a renter wants to contact a commissionaire, the platform captures a lightweight identity step and routes the interaction through a generated WhatsApp contact flow. This creates a usable lead record tied to the renter, listing, commissionaire, and timestamp. Maison does not attempt to fully control the offline transaction in V1; it focuses on proving lead origin, improving marketplace organization, and reducing wasted effort.

## What Makes This Different

- **Built around local market behavior**: the product assumes commissionaires are central actors, not a side channel.
- **Lead engine, not just listing board**: the real value to supply is qualified inbound demand.
- **Trust by layers, not slogans**: selective verification, reporting, moderation, and visible signals create confidence without overpromising.
- **Fast-scan listing standard**: the interface is optimized for rapid decision-making rather than exhaustive first-screen detail.

The core advantage is execution fit to Kinshasa’s informal rental market, not proprietary technology.  

## Product Principles

1. **Speed matters more than catalog size at launch.**
2. **High-quality listings beat large low-trust inventory.**
3. **The platform must protect lead attribution more than listing exclusivity.**
4. **Verification claims must be narrow, explicit, and operationally real.**
5. **Commissionaires must see direct commercial value from using the platform.**

## Success Criteria

### User Success Signals

- Renters can find relevant listings within minutes using basic filters.
- Renters can contact a commissionaire without friction through tracked WhatsApp flow.
- Reported fake, stale, or suspicious listings are surfaced and handled quickly.

### Supply Success Signals

- Commissionaires publish listings with the required quality standard.
- Commissionaires receive attributable inbound leads from the platform.
- A meaningful share of active listings stays current enough to remain useful.

### Business Success Signals

- Maison builds a credible starting inventory of quality rental listings in Kinshasa.
- Organic acquisition through search becomes a viable source of renter demand. [ASSUMPTION]
- Select commissionaires begin treating Maison as a useful source of leads, not just another posting channel.

## Scope

### In Scope for V1

- Rental listings only
- Listing cards with price, commune, bedrooms, and real media
- Listing detail page with additional information
- Search and filters: commune, budget, bedrooms
- Commissionaire listing submission flow
- Generated WhatsApp contact flow
- Automatic lead record creation
- “Verified” badge on selectively reviewed listings only
- User reporting for listings and commissionaires
- Lightweight admin moderation

### Explicitly Out of Scope for V1

- Property sales
- Full transaction management
- Guaranteed proof of final deal closure
- Advanced commissionaire reputation system
- Agency-grade account structures
- Sophisticated anti-duplication logic

## Trust and Operations

Maison should not claim that all listings are verified. Instead, some listings can earn a visible verification badge when they pass a defined review process. The exact definition of “verified” should be operationally manageable in V1, such as confirming the commissionaire, confirming contactability, reviewing listing quality, and checking that the listing is still active at a given point in time.

The platform should also support reporting of suspicious listings or commissionaires. This creates a feedback loop that strengthens trust over time and reduces the risk of a low-quality marketplace.

## Key Risks and Open Questions

- How much effort will commissionaires accept before posting friction becomes too high?
- What minimum status updates can be realistically expected from commissionaires?
- How should Maison handle the same property being represented by multiple commissionaires?
- What exact operational process defines a verified listing in V1?
- How fast can the platform reach the threshold where supply sees consistent lead value?

## Vision

If Maison succeeds, it becomes the most trusted digital entry point into Kinshasa’s rental market: a place where renters search faster, commissionaires convert better, and the market becomes more legible without pretending to become fully formal overnight.

Over time, Maison can evolve from a rental listings marketplace into a broader trust and transaction infrastructure for real estate in Kinshasa, potentially adding richer partner profiles, stronger lead management, agency workflows, and eventually adjacent categories beyond rental.
