from django.views.generic import TemplateView

from apps.listings.forms import ListingFilterForm
from apps.listings.selectors import get_listing_primary_photo, get_public_browse_listings


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            listings = list(get_public_browse_listings()[:3])
        except Exception as error:
            if error.__class__.__name__ != "DatabaseOperationForbidden":
                raise
            listings = []
        for listing in listings:
            primary_photo = get_listing_primary_photo(listing)
            listing.card_primary_photo = primary_photo
            listing.card_photo_alt = (
                primary_photo.alt_text.strip()
                if primary_photo and primary_photo.alt_text.strip()
                else f"Logement a {listing.commune}"
            )
            listing.card_freshness_at = (
                listing.availability_reconfirmed_at
                or listing.availability_changed_at
                or listing.updated_at
            )
        context["filter_form"] = ListingFilterForm()
        context["featured_listings"] = listings
        return context
