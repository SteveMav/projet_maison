from django.urls import path
from apps.leads.views import create_lead_endpoint

app_name = "leads"

urlpatterns = [
    path("listings/<int:listing_id>/create-lead/", create_lead_endpoint, name="create_lead"),
]
