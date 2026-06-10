# Maison Visual Proposal

This folder contains a static, interactive HTML/CSS/JS proposal for Maison. It is intentionally framework-free so the product direction can be reviewed before implementation architecture is chosen.

The durable product and UX context lives in `../PRODUCT.md`, `../DESIGN.md`, and `../EXPERIENCE.md`.

The inspected Stitch export and its reconciliation notes live in `stitch-imports/detail-ngaliema/` and `STITCH-REVIEW.md`.

## Included surfaces

- Tenant browse and filter experience
- Listing detail panel with trust signals
- Lightweight identification before the WhatsApp handoff
- Commissionnaire overview for listings and attributed leads
- Loading, empty, and recoverable feedback states

## Run

Open `index.html` directly in a browser, or serve the folder locally:

```powershell
python -m http.server 4173 --directory design
```

Then visit `http://localhost:4173`.

## Notes

- The listings and leads are fictional sample data for the visual proposal.
- Remote property images are used only to make the prototype easier to evaluate.
- The interface copy is in French because the first launch context is Kinshasa.
