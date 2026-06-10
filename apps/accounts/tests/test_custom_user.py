from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase


class CustomUserFoundationTests(TestCase):
    def test_auth_user_model_points_to_custom_user(self):
        self.assertEqual(settings.AUTH_USER_MODEL, "accounts.CustomUser")
        self.assertEqual(get_user_model().__name__, "CustomUser")

    def test_user_can_store_email_and_optional_whatsapp_phone(self):
        user = get_user_model().objects.create_user(
            email="Tenant@Example.COM",
            password="StrongPass123!",
            whatsapp_phone="",
        )

        self.assertEqual(user.email, "tenant@example.com")
        self.assertEqual(user.whatsapp_phone, "")
        self.assertTrue(user.check_password("StrongPass123!"))

    def test_user_without_whatsapp_phone_is_not_whatsapp_ready(self):
        user = get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
            whatsapp_phone="",
        )

        self.assertFalse(user.is_whatsapp_ready)

    def test_user_with_whatsapp_phone_is_whatsapp_ready(self):
        user = get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
            whatsapp_phone="+243990000000",
        )

        self.assertTrue(user.is_whatsapp_ready)

    def test_first_accounts_migration_contains_custom_user_fields(self):
        migration_path = (
            Path(settings.BASE_DIR) / "apps" / "accounts" / "migrations" / "0001_initial.py"
        )

        self.assertTrue(migration_path.exists())
        migration_source = migration_path.read_text()
        self.assertIn("CustomUser", migration_source)
        self.assertIn("email", migration_source)
        self.assertIn("whatsapp_phone", migration_source)

    def test_user_consent_fields(self):
        user = get_user_model().objects.create_user(
            email="consent@example.com",
            password="StrongPass123!",
        )
        self.assertFalse(user.whatsapp_consent)
        self.assertIsNone(user.whatsapp_consent_given_at)
