from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.views import View

from apps.accounts.decorators import whatsapp_phone_required
from apps.accounts.mixins import WhatsAppPhoneRequiredMixin
from apps.accounts.selectors import user_has_whatsapp_phone


def protected_view(request):
    return HttpResponse("protected")


class ProtectedClassView(WhatsAppPhoneRequiredMixin, View):
    phone_complete_url = "/accounts/phone-complete/"

    def get(self, request):
        return HttpResponse("protected")


class WhatsAppPhoneReadinessTests(TestCase):
    def test_user_has_whatsapp_phone_requires_authenticated_valid_stored_number(self):
        self.assertFalse(user_has_whatsapp_phone(AnonymousUser()))

        user = get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
            whatsapp_phone="",
        )
        self.assertFalse(user_has_whatsapp_phone(user))
        self.assertFalse(user.is_whatsapp_ready)

        user.whatsapp_phone = "not-a-phone"
        self.assertFalse(user_has_whatsapp_phone(user))
        self.assertFalse(user.is_whatsapp_ready)

        user.whatsapp_phone = "+243990000000"
        self.assertTrue(user_has_whatsapp_phone(user))
        self.assertTrue(user.is_whatsapp_ready)


class WhatsAppPhoneRequiredDecoratorTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.decorated_view = whatsapp_phone_required(
            protected_view,
            phone_complete_url="/accounts/phone-complete/",
        )

    def test_anonymous_user_redirects_to_login_with_next(self):
        request = self.factory.get("/phone-action/")
        request.user = AnonymousUser()

        response = self.decorated_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/phone-action/")

    def test_authenticated_user_without_phone_redirects_to_phone_completion(self):
        request = self.factory.get("/phone-action/")
        request.user = get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
        )

        response = self.decorated_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/phone-complete/?next=%2Fphone-action%2F")

    def test_authenticated_user_with_valid_phone_reaches_view(self):
        request = self.factory.get("/phone-action/")
        request.user = get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
            whatsapp_phone="+243990000000",
        )

        response = self.decorated_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"protected")


class WhatsAppPhoneRequiredMixinTests(TestCase):
    def test_mixin_redirects_authenticated_user_without_phone(self):
        request = RequestFactory().get("/class-phone-action/")
        request.user = get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
        )

        response = ProtectedClassView.as_view()(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/accounts/phone-complete/?next=%2Fclass-phone-action%2F",
        )


class WhatsAppPhoneGateRouteTests(TestCase):
    def test_anonymous_access_to_phone_dependent_route_redirects_to_login(self):
        response = self.client.get(reverse("accounts:phone_required_probe"))

        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('accounts:phone_required_probe')}",
        )

    def test_authenticated_user_without_phone_redirects_to_completion_route(self):
        user = get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("accounts:phone_required_probe"))

        self.assertRedirects(
            response,
            (
                f"{reverse('accounts:phone_complete')}"
                f"?next={reverse('accounts:phone_required_probe')}"
            ),
            fetch_redirect_response=False,
        )

    def test_authenticated_user_with_valid_phone_reaches_phone_dependent_route(self):
        user = get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
            whatsapp_phone="+243990000000",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("accounts:phone_required_probe"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Action WhatsApp protegee")
