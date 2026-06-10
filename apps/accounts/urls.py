from django.urls import path

from apps.accounts.views import (
    AccountDashboardView,
    google_login_start,
    identify_tenant,
    MaisonLoginView,
    MaisonLogoutView,
    PhoneCompleteView,
    phone_required_probe,
    RegisterView,
)

app_name = "accounts"

urlpatterns = [
    path("", AccountDashboardView.as_view(), name="dashboard"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", MaisonLoginView.as_view(), name="login"),
    path("phone-complete/", PhoneCompleteView.as_view(), name="phone_complete"),
    path("phone-required-probe/", phone_required_probe, name="phone_required_probe"),
    path("google/start/", google_login_start, name="google_start"),
    path("logout/", MaisonLogoutView.as_view(), name="logout"),
    path("identify/", identify_tenant, name="identify"),
]
