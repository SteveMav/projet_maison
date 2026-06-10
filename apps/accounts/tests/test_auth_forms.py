from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.accounts.forms import RegistrationForm


class RegistrationFormTests(TestCase):
    def test_valid_registration_creates_custom_user_with_hashed_password(self):
        form = RegistrationForm(
            data={
                "email": "Tenant@Example.COM",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()

        self.assertEqual(user.email, "tenant@example.com")
        self.assertNotEqual(user.password, "StrongPass123!")
        self.assertTrue(user.check_password("StrongPass123!"))

    def test_duplicate_email_returns_field_error(self):
        get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
        )

        form = RegistrationForm(
            data={
                "email": "TENANT@example.com",
                "password1": "AnotherPass123!",
                "password2": "AnotherPass123!",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertIn("Un compte existe deja", form.errors["email"][0])

    def test_invalid_password_returns_password_field_error(self):
        form = RegistrationForm(
            data={
                "email": "tenant@example.com",
                "password1": "123",
                "password2": "123",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)

    def test_password_similar_to_email_returns_password_field_error(self):
        form = RegistrationForm(
            data={
                "email": "tenant@example.com",
                "password1": "tenant@example.com",
                "password2": "tenant@example.com",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)
