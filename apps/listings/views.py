from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import escape
from django.views import View
from django.views.generic import ListView, DetailView

from apps.listings.forms import ListingFilterForm
from apps.listings.selectors import (
    filter_public_listings,
    get_listing_primary_photo,
    get_public_browse_listings,
    get_listing_detail_queryset,
)


FILTER_FIELDS = ("commune", "budget_min", "budget_max", "bedrooms_min")


def compact_filter_values(cleaned_data):
    return {
        field: cleaned_data[field]
        for field in FILTER_FIELDS
        if cleaned_data.get(field) not in ("", None)
    }


def build_filter_url(path, filters, *, remove=None, page=None):
    query = QueryDict(mutable=True)
    for field in FILTER_FIELDS:
        if field == remove or field not in filters:
            continue
        query[field] = str(filters[field])
    if page is not None:
        query["page"] = str(page)

    querystring = query.urlencode()
    if not querystring:
        return path
    return f"{path}?{querystring}"


def build_filter_chip(field, value, path, filters):
    labels = {
        "commune": f"Commune: {value}",
        "budget_min": f"Min: {value} USD",
        "budget_max": f"Max: {value} USD",
        "bedrooms_min": f"{value}+ chambres",
    }
    return {
        "param": field,
        "label": labels[field],
        "url": build_filter_url(path, filters, remove=field),
    }


def format_result_count(count):
    if count == 1:
        return "1 annonce trouvée"
    return f"{count} annonces trouvées"


def serialize_form_errors(form):
    return {
        field: [str(error) for error in errors]
        for field, errors in form.errors.items()
    }


class PublicBrowseView(ListView):
    context_object_name = "listings"
    paginate_by = 12
    template_name = "listings/browse.html"

    def get_filter_form(self):
        if not hasattr(self, "filter_form"):
            self.filter_form = ListingFilterForm(data=self.request.GET)
            self.filter_form_is_valid = self.filter_form.is_valid()
            self.active_filters = (
                compact_filter_values(self.filter_form.cleaned_data)
                if self.filter_form_is_valid
                else {}
            )
        return self.filter_form

    def get_queryset(self):
        filter_form = self.get_filter_form()
        if filter_form.is_valid():
            return filter_public_listings(filter_form.cleaned_data)
        return get_public_browse_listings()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for listing in context["listings"]:
            primary_photo = get_listing_primary_photo(listing)
            listing.card_primary_photo = primary_photo
            listing.card_photo_alt = (
                primary_photo.alt_text.strip()
                if primary_photo and primary_photo.alt_text.strip()
                else f"Logement a {listing.commune}"
            )
            listing.card_freshness_at = listing.availability_reconfirmed_at or listing.availability_changed_at or listing.updated_at
        active_filters = self.active_filters
        path = self.request.path
        page_obj = context["page_obj"]
        context["filter_form"] = self.get_filter_form()
        context["active_filters"] = active_filters
        context["active_filter_chips"] = [
            build_filter_chip(field, active_filters[field], path, active_filters)
            for field in FILTER_FIELDS
            if field in active_filters
        ]
        context["clear_filters_url"] = path
        context["result_count"] = context["paginator"].count
        context["result_count_text"] = format_result_count(context["result_count"])
        context["filter_querystring"] = QueryDict(mutable=True)
        for field in FILTER_FIELDS:
            if field in active_filters:
                context["filter_querystring"][field] = str(active_filters[field])
        context["filter_querystring"] = context["filter_querystring"].urlencode()
        context["pagination_urls"] = {
            "previous": (
                build_filter_url(
                    path,
                    active_filters,
                    page=page_obj.previous_page_number(),
                )
                if page_obj.has_previous()
                else None
            ),
            "next": (
                build_filter_url(path, active_filters, page=page_obj.next_page_number())
                if page_obj.has_next()
                else None
            ),
        }
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("X-Maison-Partial") != "filters":
            return super().render_to_response(context, **response_kwargs)

        filter_form = self.get_filter_form()
        if not filter_form.is_valid():
            return JsonResponse(
                {
                    "ok": False,
                    "error": {
                        "message": "Certains filtres sont invalides.",
                        "fields": serialize_form_errors(filter_form),
                    },
                },
                status=400,
            )

        page_obj = context["page_obj"]
        page_number = page_obj.number if page_obj.number > 1 else None
        return JsonResponse(
            {
                "ok": True,
                "data": {
                    "results_html": render_to_string(
                        "listings/includes/results_grid.html",
                        context,
                        request=self.request,
                    ),
                    "chips_html": render_to_string(
                        "listings/includes/filter_chips.html",
                        context,
                        request=self.request,
                    ),
                    "result_count": context["result_count"],
                    "result_count_text": context["result_count_text"],
                    "url": build_filter_url(
                        self.request.path,
                        context["active_filters"],
                        page=page_number,
                    ),
                },
            }
        )


class PublicListingDetailView(DetailView):
    context_object_name = "listing"

    def get_queryset(self):
        return get_listing_detail_queryset()

    def get_template_names(self):
        if self.request.headers.get("X-Maison-Partial") == "listing-detail":
            return ["listings/includes/detail_panel.html"]
        return ["listings/detail.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listing = context["listing"]
        
        photos = list(listing.photos.all())
        context["photos"] = photos
        context["photos_count"] = len(photos)
        context["main_photo"] = photos[0] if photos else None

        from_url = self.request.GET.get("from")
        if from_url:
            context["from_url"] = from_url

        return context
