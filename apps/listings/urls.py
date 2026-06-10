from django.urls import path

from apps.listings.views import PublicBrowseView, PublicListingDetailView

app_name = "listings"

urlpatterns = [
    path("annonces/", PublicBrowseView.as_view(), name="browse"),
    path("annonces/<int:pk>/", PublicListingDetailView.as_view(), name="detail"),
]
