---
name: Maison
description: Rental-first marketplace for Kinshasa. Warm, grounded, mobile-first.
status: draft
updated: 2026-06-01
sources:
  - PRODUCT.md
  - EXPERIENCE.md
  - _bmad-output/planning-artifacts/prds/prd-maison-2026-05-31/prd.md
  - _bmad-output/brainstorming/brainstorming-session-2026-05-30-144517.md
  - design/stitch-imports/detail-ngaliema/screen.html
  - design/stitch-imports/detail-ngaliema/screen.png
colors:
  surface-base: '#F7F4EE'
  surface-raised: '#FEFDF9'
  surface-soft: '#EEE8DC'
  surface-muted: '#E3DCCF'
  ink-primary: '#1D2A25'
  ink-secondary: '#64706A'
  ink-muted: '#89928E'
  accent: '#276A52'
  accent-strong: '#1E5642'
  accent-soft: '#DCEDE4'
  trust-soft: '#EEFDF5'
  trust-border: '#B5EFD4'
  warm: '#C77742'
  warning-soft: '#F8E7D8'
  border-hairline: '#DED8CC'
  border-strong: '#C8C0B3'
  error: '#B8473D'
  error-soft: '#FBE2DE'
  scrim: 'rgba(29, 42, 37, 0.40)'
  inverse-surface: '#26332E'
  inverse-ink: '#E5F4EC'
typography:
  family: '"Manrope", "Segoe UI", sans-serif'
  display-desktop: '700 40px/48px "Manrope", "Segoe UI", sans-serif'
  display-mobile: '700 32px/38px "Manrope", "Segoe UI", sans-serif'
  heading-lg: '700 28px/36px "Manrope", "Segoe UI", sans-serif'
  heading-md: '600 24px/32px "Manrope", "Segoe UI", sans-serif'
  heading-sm: '600 20px/28px "Manrope", "Segoe UI", sans-serif'
  body-lg: '400 18px/28px "Manrope", "Segoe UI", sans-serif'
  body-md: '400 16px/24px "Manrope", "Segoe UI", sans-serif'
  body-sm: '400 14px/20px "Manrope", "Segoe UI", sans-serif'
  label-md: '600 14px/16px "Manrope", "Segoe UI", sans-serif'
  label-sm: '500 12px/14px "Manrope", "Segoe UI", sans-serif'
rounded:
  sm: 10px
  md: 16px
  lg: 24px
  pill: 999px
spacing:
  '1': 4px
  '2': 8px
  '3': 12px
  '4': 16px
  '5': 24px
  '6': 32px
  '7': 40px
  '8': 64px
components:
  button-primary: 'Deep Leaf background, inverse ink, 10px radius, 48px minimum height'
  button-secondary: 'Raised or accent-soft background, Deep Leaf ink, hairline border where needed'
  listing-card: 'Image-forward fast-scan surface with 16px image radius and no decorative shadow'
  detail-panel: 'Full-screen mobile surface; right-side desktop drawer with sticky header and sticky CTA'
  verification-box: 'trust-soft background, trust-border hairline, shield icon, narrow defensible copy'
  status-chip: 'Text plus icon where needed; color never carries meaning alone'
---

## Brand & Style

Maison is a practical rental marketplace for Kinshasa with calm, locally grounded confidence. The interface should feel useful before it feels polished: listings are easy to scan, verification language is precise, and WhatsApp is treated as the familiar continuation of the journey.

The physical scene is a tenant reviewing rental options on a phone in late-afternoon light, with limited patience for stale inventory and exaggerated promises. The visual language is **warm modern-organic product UI**: sun-warmed neutral surfaces, deep green actions, hairline borders, real housing photography, and restrained depth.

This document is the visual contract. The local prototype and Stitch artifacts are composition references. This document wins when a generated mock introduces conflicting colors, copy, imagery, or component behavior.

## Colors

### Strategy

Use a restrained palette. Warm neutrals carry most of the surface. Deep green is the primary action and trust anchor. Terracotta is a minor cue for attention states, never a competing CTA color.

| Role | Token | Value | Usage |
|---|---|---|---|
| Main canvas | `{colors.surface-base}` | `#F7F4EE` | Page background, browse surfaces |
| Raised paper | `{colors.surface-raised}` | `#FEFDF9` | Inputs, drawers, cards when a distinct surface is required |
| Soft neutral | `{colors.surface-soft}` | `#EEE8DC` | Skeletons, neutral status chips, supporting surfaces |
| Primary ink | `{colors.ink-primary}` | `#1D2A25` | Headings and high-priority text |
| Secondary ink | `{colors.ink-secondary}` | `#64706A` | Descriptions, timestamps, helper text |
| Primary action | `{colors.accent}` | `#276A52` | Primary buttons, active navigation, verified icon |
| Strong action | `{colors.accent-strong}` | `#1E5642` | Hover and pressed states, dark confidence section |
| Soft action | `{colors.accent-soft}` | `#DCEDE4` | Selected filters, secondary actions, positive status |
| Trust surface | `{colors.trust-soft}` | `#EEFDF5` | Verification explanation only |
| Trust border | `{colors.trust-border}` | `#B5EFD4` | Verification explanation border |
| Warm cue | `{colors.warm}` | `#C77742` | Small secondary emphasis, never primary actions |
| Warning surface | `{colors.warning-soft}` | `#F8E7D8` | Availability reconfirmation |
| Error | `{colors.error}` | `#B8473D` | Report action, validation and recoverable errors |
| Scrim | `{colors.scrim}` | `rgba(29, 42, 37, 0.40)` | Drawer and modal backdrop |

The Stitch-generated design system also exposed mint surfaces such as `#EEFDF5`. Treat those as trust-specific surfaces, not as the global canvas. A mint-drenched application feels more clinical and less grounded than Maison's intended warm-paper base.

### Semantic States

| State | Background | Foreground | Additional signal |
|---|---|---|---|
| Verified | `{colors.trust-soft}` | `{colors.accent-strong}` | Shield icon plus `Annonce vérifiée` |
| Available | `{colors.accent-soft}` | `{colors.accent-strong}` | Text label |
| Reconfirm soon | `{colors.warning-soft}` | `#97532E` | Clock icon plus text |
| Draft | `{colors.surface-soft}` | `{colors.ink-secondary}` | Text label |
| Error | `{colors.error-soft}` | `{colors.error}` | Inline explanation and recovery action |
| Disabled | `{colors.surface-soft}` | `{colors.ink-muted}` | Reduced contrast, no shadow |

## Typography

Use Manrope throughout the product. The geometric softness complements the rounded visual language while remaining readable in task-heavy surfaces. Use Segoe UI only as the fallback.

| Role | Token | Usage |
|---|---|---|
| Display desktop | `{typography.display-desktop}` | Browse hero and rare top-level product moments |
| Display mobile | `{typography.display-mobile}` | Mobile hero only |
| Heading large | `{typography.heading-lg}` | Major section headings |
| Heading medium | `{typography.heading-md}` | Listing detail title |
| Heading small | `{typography.heading-sm}` | Drawer sections and panel headings |
| Body medium | `{typography.body-md}` | Standard descriptions and form copy |
| Body small | `{typography.body-sm}` | Supporting copy, timestamps, privacy notes |
| Label medium | `{typography.label-md}` | Buttons and fields |
| Label small | `{typography.label-sm}` | Chips, metadata, photo counters |

Rules:

- Use sentence case in visible French copy.
- Use uppercase sparingly for eyebrows and compact metadata only.
- Keep body text at least `16px` where reading is expected.
- Avoid oversized headings in operational surfaces.
- Keep paragraph lines near `65ch` maximum.

## Layout & Spacing

Maison follows a mobile-first fluid grid based on a `4px` spacing baseline.

| Breakpoint | Layout |
|---|---|
| Mobile, `< 700px` | Single column, `16px` side margins, bottom navigation, stacked search controls |
| Tablet, `700px–920px` | Two-column listing grid, compact navigation, `24px–32px` margins |
| Desktop, `> 920px` | Twelve-column grid, max content width around `1280px–1420px`, three-column listing grid |

Spacing priorities:

- Use `{spacing.4}` (`16px`) for standard internal component padding.
- Use `{spacing.5}` (`24px`) between related content blocks.
- Use `{spacing.7}` (`40px`) and `{spacing.8}` (`64px`) between major sections.
- Avoid nesting several padded card containers. Prefer whitespace and hairline dividers.

### Listing Detail Composition

The inspected Stitch screen at `design/stitch-imports/detail-ngaliema/screen.png` is a useful composition reference:

- Full-screen detail surface on mobile.
- Right-side drawer on desktop, approximately `480px–620px` wide.
- `40%` ink-colored backdrop on desktop.
- Sticky top controls.
- Main image with a `4:3` ratio.
- Horizontal thumbnail strip below the main image.
- Compact image counter such as `1/8`.
- Location, title, price, facts, verification explanation, description, commissionnaire, report action.
- Sticky WhatsApp CTA at the bottom.

On desktop, preserve browse context behind the drawer. On mobile, prioritize an immersive full-screen detail surface.

## Elevation & Depth

Use tonal layering instead of heavy shadows.

| Level | Treatment | Usage |
|---|---|---|
| Level 0 | `{colors.surface-base}` | Global canvas |
| Level 1 | `{colors.surface-raised}` plus `{colors.border-hairline}` | Cards, inputs, panels |
| Level 2 | `0 4px 12px rgba(29, 42, 37, 0.05)` | Hovered or floating interactive elements |
| Level 3 | `{colors.scrim}` plus `0 30px 90px rgba(34, 44, 39, 0.18)` | Drawer and modal overlays |

Do not apply shadows to every listing card. Cards should mostly rely on photography, spacing, and borders.

## Shapes

- Controls: `{rounded.sm}` (`10px`).
- Listing cards and grouped operational surfaces: `{rounded.md}` (`16px`).
- Hero surfaces, drawers, and large sections: `{rounded.lg}` (`24px`).
- Pills: `{rounded.pill}` only for filters, status chips, and compact badges.
- Icon buttons may be circular where the action is universally familiar: close, favorite, share.
- Use a single rounded outlined icon family. Do not mix multiple visual icon styles on the same surface.

## Photography

Housing photography is part of the trust model, not decoration.

Rules:

- Production listings must use real property photos supplied for the represented home.
- Require at least three usable photos before submission.
- Prefer honest, well-lit photos over aggressively retouched imagery.
- Show exterior, principal living space, and at least one relevant interior detail when available.
- Use consistent cropping in cards, but preserve complete context in the detail gallery.
- Do not let AI-generated villas or architectural renders silently become production listing media.
- For mockups only, aspirational placeholder images are acceptable when clearly treated as placeholders.

The imported Stitch images under `design/stitch-imports/detail-ngaliema/property-*.jpg` are useful for layout review but skew upscale. The production design agent should deliberately test ordinary, credible rental inventory as well.

## Components

### Header And Navigation

- Desktop header: compact `M` mark, `maison` wordmark, tenant navigation, `Espace pro`, and `Publier un bien`.
- Mobile navigation: `Explorer`, `Favoris`, `Espace pro`.
- Active mobile navigation uses `{colors.accent}` and a visible text label.
- Navigation stays familiar. Do not invent custom gestures or decorative navigation.

### Buttons

| Variant | Visual rule | Usage |
|---|---|---|
| Primary | `{colors.accent}` background, inverse text, `48px` minimum height, `{rounded.sm}` | Search, WhatsApp handoff, publish submission |
| Secondary | Raised or `{colors.accent-soft}` background, accent text | Favorites, neutral supporting actions |
| Text | Accent or error text, no enclosing surface unless needed | Report, clear filters, learn more |
| Icon | At least `44px × 44px`, circular only for familiar controls | Close, share, favorite, overflow |

Every pressable control requires default, hover, focus, active, loading, and disabled states. Use a subtle `scale(0.97)` press response.

### Search Form

- Use visible labels above controls.
- Combine Commune, budget maximum, and bedroom minimum.
- Desktop may group fields into one raised search surface.
- Mobile stacks the fields vertically.
- Use listing-shaped skeletons while results refresh.

### Listing Card

- Image-first composition.
- Expose Commune, neighborhood, price, bedroom count, property type, freshness, favorite action, and optional verified label.
- Entire card opens detail. Favorite remains an independent action.
- Never show a verification badge on an unverified listing.

### Listing Detail Panel

- Sticky header: close, optional share, favorite.
- Main gallery: primary image, thumbnails, count.
- Primary facts: Commune, neighborhood, title, monthly price, bedrooms, bathrooms, views.
- Show availability and last update explicitly.
- Verification box appears only for verified listings.
- Commissionnaire block contains identity and the handoff note.
- Report action remains visible but visually secondary.
- Sticky bottom CTA: `Contacter sur WhatsApp`.
- Hide the WhatsApp CTA when availability is not `available`.

### Verification Box

Canonical copy:

> Cette annonce a passé un contrôle supplémentaire. Le badge ne garantit pas le résultat d'une transaction hors ligne.

Do not reuse the imported Stitch copy that claims Maison guarantees availability or information accuracy. That statement exceeds the PRD trust boundary.

### Lightweight Identification

- Explain why name and phone number are requested.
- Require explicit consent before Lead creation.
- Show recoverable inline error if Lead creation fails.
- Do not open WhatsApp until Lead creation succeeds.
- Include the privacy reassurance: `Maison ne lit pas vos conversations WhatsApp.`

### Commissionnaire Operations

- Prefer compact rows and dividers over nested dashboard cards.
- Lead rows expose tenant identity, originating listing, timestamp, and status where enabled.
- Inventory rows expose listing identity, availability state, freshness prompt, and moderation state.
- Numbers may use tighter letter spacing, but avoid oversized hero metrics.

## Do's And Don'ts

| Do | Don't |
|---|---|
| Make trust claims specific, narrow, and reversible | Imply that Maison guarantees an offline transaction |
| Show freshness next to the decision context | Hide stale-listing risk behind a generic trust badge |
| Use warm neutrals for the primary canvas | Turn the entire interface mint green |
| Let real listing photography carry the product | Fill production inventory with polished AI renders |
| Use green for primary action and verified state | Introduce competing purple, neon blue, or gradient accents |
| Keep mobile controls generous and direct | Compress the mobile experience into desktop leftovers |
| Preserve familiar product patterns | Add decorative motion, glass cards, or custom affordances |
| Use one outlined icon language | Mix icon families and inconsistent stroke weights |
