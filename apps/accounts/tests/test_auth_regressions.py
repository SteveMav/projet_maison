from unittest import mock

from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.test import TestCase
from django.urls import resolve, reverse


class AccountRouteRegressionTests(TestCase):
    def test_local_account_route_names_are_preserved(self):
        expected_routes = {
            "accounts:dashboard": "/accounts/",
            "accounts:register": "/accounts/register/",
            "accounts:login": "/accounts/login/",
            "accounts:logout": "/accounts/logout/",
            "accounts:google_start": "/accounts/google/start/",
        }

        for route_name, expected_path in expected_routes.items():
            with self.subTest(route_name=route_name):
                self.assertEqual(reverse(route_name), expected_path)

    def test_google_allauth_routes_are_available_under_accounts_prefix(self):
        self.assertEqual(reverse("google_login"), "/accounts/google/login/")
        self.assertEqual(
            reverse("google_callback"),
            "/accounts/google/login/callback/",
        )
        self.assertEqual(resolve("/accounts/google/login/").url_name, "google_login")

    def test_local_login_still_preserves_safe_next_after_allauth_mount(self):
        get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
        )

        response = self.client.post(
            f"{reverse('accounts:login')}?next={reverse('accounts:dashboard')}",
            {
                "username": "tenant@example.com",
                "password": "StrongPass123!",
            },
        )

        self.assertRedirects(response, reverse("accounts:dashboard"))

    def test_login_surface_renders_google_sign_in_and_email_fallback(self):
        response = self.client.get(
            f"{reverse('accounts:login')}?next={reverse('accounts:dashboard')}"
        )

        self.assertContains(response, "Continuer avec Google")
        self.assertContains(response, 'method="post"')
        self.assertContains(response, reverse("accounts:google_start"))
        self.assertContains(response, 'class="google-mark"')
        self.assertContains(response, "Adresse e-mail")
        self.assertContains(response, "Mot de passe")
        self.assertNotContains(response, "accounts.google.com")

    def test_register_surface_renders_google_sign_in_and_email_fallback(self):
        response = self.client.get(
            f"{reverse('accounts:register')}?next={reverse('accounts:dashboard')}"
        )

        self.assertContains(response, "Continuer avec Google")
        self.assertContains(response, 'method="post"')
        self.assertContains(response, reverse("accounts:google_start"))
        self.assertContains(response, 'class="google-mark"')
        self.assertContains(response, "Ou connectez-vous avec votre adresse e-mail")
        self.assertContains(response, "Adresse e-mail")
        self.assertNotContains(response, "accounts.google.com")

    def test_google_start_without_credentials_recovers_to_email_login(self):
        with mock.patch(
            "apps.accounts.views.google_provider_is_configured",
            return_value=False,
        ):
            response = self.client.post(
                reverse("accounts:google_start"),
                {"process": "login", "next": reverse("accounts:dashboard")},
                follow=True,
            )

        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('accounts:dashboard')}",
        )
        self.assertContains(response, "La connexion Google")
        self.assertContains(response, "pas encore configuree")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_google_start_delegates_to_allauth_when_configured(self):
        with (
            mock.patch(
                "apps.accounts.views.google_provider_is_configured",
                return_value=True,
            ),
            mock.patch("apps.accounts.views.oauth2_login") as oauth2_login,
        ):
            oauth2_login.return_value = HttpResponseRedirect("/oauth-started/")

            self.client.post(reverse("accounts:google_start"), {"process": "login"})

        oauth2_login.assert_called_once()

    def test_google_login_cancelled_page_is_recoverable_and_french(self):
        response = self.client.get(reverse("socialaccount_login_cancelled"))

        self.assertContains(response, "La connexion Google a ete annulee.")
        self.assertContains(response, reverse("accounts:login"))
        self.assertContains(response, "utiliser votre adresse e-mail")
        self.assertNotContains(response, "token")
        self.assertNotContains(response, "payload")

    def test_google_authentication_error_page_is_recoverable_and_french(self):
        response = self.client.get(reverse("socialaccount_login_error"))

        self.assertContains(
            response,
            "Nous n'avons pas pu terminer la connexion Google.",
            status_code=401,
        )
        self.assertContains(response, reverse("accounts:login"), status_code=401)
        self.assertContains(
            response,
            "utiliser votre adresse e-mail",
            status_code=401,
        )
        self.assertNotContains(response, "token", status_code=401)
        self.assertNotContains(response, "payload", status_code=401)
