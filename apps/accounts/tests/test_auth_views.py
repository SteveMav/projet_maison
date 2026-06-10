from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthViewTests(TestCase):
    def test_registration_creates_user_and_signs_in(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "email": "tenant@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertRedirects(response, reverse("accounts:dashboard"))
        self.assertTrue(
            get_user_model().objects.filter(email="tenant@example.com").exists()
        )
        self.assertIn("_auth_user_id", self.client.session)

    def test_registration_preserves_safe_next_destination(self):
        response = self.client.post(
            f"{reverse('accounts:register')}?next={reverse('accounts:dashboard')}",
            {
                "email": "tenant@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
                "next": reverse("accounts:dashboard"),
            },
        )

        self.assertRedirects(response, reverse("accounts:dashboard"))

    def test_invalid_login_displays_french_error_without_authenticating(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "missing@example.com",
                "password": "bad-password",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Connexion impossible")
        self.assertIn("username", response.context["form"].errors)
        self.assertFalse(response.context["form"].non_field_errors())
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_successful_login_establishes_session_and_honors_safe_next(self):
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
        self.assertIn("_auth_user_id", self.client.session)

    def test_successful_login_accepts_uppercase_email(self):
        get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
        )

        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "Tenant@Example.COM",
                "password": "StrongPass123!",
            },
        )

        self.assertRedirects(response, reverse("accounts:dashboard"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_unsafe_next_does_not_redirect_off_site(self):
        get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
        )

        response = self.client.post(
            f"{reverse('accounts:login')}?next=https://example.net/phish",
            {
                "username": "tenant@example.com",
                "password": "StrongPass123!",
            },
        )

        self.assertRedirects(response, reverse("accounts:dashboard"))

    def test_unsafe_registration_next_does_not_redirect_off_site(self):
        response = self.client.post(
            f"{reverse('accounts:register')}?next=https://example.net/phish",
            {
                "email": "tenant@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
                "next": "https://example.net/phish",
            },
        )

        self.assertRedirects(response, reverse("accounts:dashboard"))

    def test_invalid_registration_preserves_safe_next_destination(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "email": "tenant@example.com",
                "password1": "StrongPass123!",
                "password2": "DifferentPass123!",
                "next": reverse("accounts:dashboard"),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'name="next" value="{reverse("accounts:dashboard")}"',
        )

    def test_authenticated_user_cannot_register_second_account(self):
        user = get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("accounts:register"),
            {
                "email": "other@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertRedirects(response, reverse("accounts:dashboard"))
        self.assertFalse(
            get_user_model().objects.filter(email="other@example.com").exists()
        )

    def test_logout_clears_session_and_returns_home(self):
        user = get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
        )
        self.client.force_login(user)

        response = self.client.post(reverse("accounts:logout"))

        self.assertRedirects(response, reverse("core:home"))
        self.assertNotIn("_auth_user_id", self.client.session)
