from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("apps.core.urls")),
    path("", include("apps.listings.urls")),
    path("", include("apps.leads.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("pro/", include("apps.commissionnaires.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
