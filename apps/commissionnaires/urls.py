from django.urls import path

from apps.commissionnaires.views import (
    CommissionnaireProfileCreateView,
    CommissionnaireProfileDetailView,
    CommissionnaireProfileEditView,
    CommissionnaireProfileEntryView,
    ListingSubmissionView,
    ListingSubmittedView,
    ListingInventoryView,
    ListingUpdateAvailabilityView,
    ListingReconfirmAvailabilityView,
)

app_name = "commissionnaires"

urlpatterns = [
    path("", CommissionnaireProfileEntryView.as_view(), name="profile"),
    path("profile/new/", CommissionnaireProfileCreateView.as_view(), name="profile_create"),
    path(
        "profile/<int:pk>/",
        CommissionnaireProfileDetailView.as_view(),
        name="profile_detail",
    ),
    path(
        "profile/<int:pk>/edit/",
        CommissionnaireProfileEditView.as_view(),
        name="profile_edit",
    ),
    path(
        "listings/",
        ListingInventoryView.as_view(),
        name="listing_inventory",
    ),
    path(
        "listings/new/",
        ListingSubmissionView.as_view(),
        name="listing_submit",
    ),
    path(
        "listings/<int:pk>/submitted/",
        ListingSubmittedView.as_view(),
        name="listing_submitted",
    ),
    path(
        "listings/<int:pk>/availability/",
        ListingUpdateAvailabilityView.as_view(),
        name="listing_availability",
    ),
    path(
        "listings/<int:pk>/reconfirm/",
        ListingReconfirmAvailabilityView.as_view(),
        name="listing_reconfirm",
    ),
]
