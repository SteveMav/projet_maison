from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from pathlib import Path


class AccessBoundaryTests(TestCase):
    def test_public_home_is_accessible_to_anonymous_visitors(self):
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)

    def test_anonymous_account_dashboard_redirects_to_login_with_next(self):
        response = self.client.get(reverse("accounts:dashboard"))

        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('accounts:dashboard')}",
        )

    def test_authenticated_account_dashboard_succeeds(self):
        user = get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("accounts:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Votre compte")

    def test_auth_gate_include_exists_for_later_gated_surfaces(self):
        include_path = (
            Path(settings.BASE_DIR)
            / "templates"
            / "accounts"
            / "includes"
            / "auth_gate.html"
        )

        self.assertTrue(include_path.exists())
        include_source = include_path.read_text()
        self.assertIn("data-auth-gate", include_source)
        self.assertIn("auth_gate_next", include_source)
