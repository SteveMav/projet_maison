from urllib.parse import urlencode

from allauth.socialaccount.adapter import get_adapter as get_socialaccount_adapter
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.google.views import oauth2_login
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import FormView, TemplateView

from apps.accounts.decorators import whatsapp_phone_required
from apps.accounts.forms import (
    EmailAuthenticationForm,
    LightweightIdentificationForm,
    RegistrationForm,
    WhatsAppPhoneCompletionForm,
)


def google_provider_is_configured(request):
    try:
        get_socialaccount_adapter().get_provider(request, "google")
    except SocialApp.DoesNotExist:
        return False
    return True


def redirect_to_login_with_safe_next(request):
    redirect_to = request.POST.get("next") or request.GET.get("next")
    login_url = reverse_lazy("accounts:login")
    if redirect_to and url_has_allowed_host_and_scheme(
        redirect_to,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(f"{login_url}?{urlencode({'next': redirect_to})}")
    return redirect(login_url)


def google_login_start(request):
    if request.method != "POST":
        return redirect_to_login_with_safe_next(request)
    if not google_provider_is_configured(request):
        messages.error(
            request,
            "La connexion Google n'est pas encore configuree. "
            "Utilisez votre adresse e-mail pour le moment.",
        )
        return redirect_to_login_with_safe_next(request)
    return oauth2_login(request)


@whatsapp_phone_required
def phone_required_probe(request):
    return HttpResponse("Action WhatsApp protegee")


class RegisterView(FormView):
    form_class = RegistrationForm
    template_name = "accounts/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def get_safe_redirect_to(self):
        redirect_to = self.request.POST.get("next") or self.request.GET.get("next")
        if redirect_to and url_has_allowed_host_and_scheme(
            redirect_to,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        ):
            return redirect_to
        return ""

    def get_success_url(self):
        redirect_to = self.get_safe_redirect_to()
        if redirect_to:
            return redirect_to
        return reverse_lazy("accounts:dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.get_safe_redirect_to()
        return context

    def form_valid(self, form):
        try:
            user = form.save()
        except IntegrityError:
            form.add_error("email", "Un compte existe deja avec cette adresse e-mail.")
            return self.form_invalid(form)
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect(self.get_success_url())


class MaisonLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True
    template_name = "accounts/login.html"


class MaisonLogoutView(LogoutView):
    next_page = reverse_lazy("core:home")


class AccountDashboardView(LoginRequiredMixin, TemplateView):
    login_url = settings.LOGIN_URL
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = getattr(self.request.user, "commissionnaire_profile", None)
        context["commissionnaire_profile"] = profile
        context["listing_count"] = profile.listings.count() if profile else 0
        context["lead_count"] = profile.leads.count() if profile else 0
        context["is_whatsapp_ready"] = self.request.user.is_whatsapp_ready
        return context


class PhoneCompleteView(LoginRequiredMixin, FormView):
    form_class = WhatsAppPhoneCompletionForm
    login_url = settings.LOGIN_URL
    template_name = "accounts/phone_complete.html"

    def get_safe_next(self):
        redirect_to = self.request.POST.get("next") or self.request.GET.get("next")
        if redirect_to and url_has_allowed_host_and_scheme(
            redirect_to,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        ):
            return redirect_to
        return ""

    def get_success_url(self):
        return self.get_safe_next() or reverse_lazy("accounts:dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.get_safe_next()
        return context

    def form_valid(self, form):
        self.request.user.whatsapp_phone = form.cleaned_data["whatsapp_phone"]
        self.request.user.save(update_fields=["whatsapp_phone"])
        return redirect(self.get_success_url())


@login_required
def identify_tenant(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "errors": {"__all__": [{"message": "Méthode non autorisée", "code": "invalid_method"}]}}, status=405)
    
    form = LightweightIdentificationForm(request.POST)
    if form.is_valid():
        user = request.user
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        user.whatsapp_phone = form.cleaned_data["whatsapp_phone"]
        user.whatsapp_consent = True
        user.whatsapp_consent_given_at = timezone.now()
        user.save(update_fields=[
            "first_name",
            "last_name",
            "whatsapp_phone",
            "whatsapp_consent",
            "whatsapp_consent_given_at",
        ])
        return JsonResponse({"success": True})
    
    return JsonResponse({
        "success": False,
        "errors": form.errors.get_json_data()
    }, status=400)
