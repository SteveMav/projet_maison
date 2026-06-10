from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from apps.commissionnaires.models import CommissionnaireProfile


class CommissionnaireProfileModelTests(TestCase):
    def create_user(self, email="pro@example.com", whatsapp_phone="+243990000000"):
        return get_user_model().objects.create_user(
            email=email,
            password="StrongPass123!",
            whatsapp_phone=whatsapp_phone,
        )

    def test_profile_belongs_to_exactly_one_user(self):
        user = self.create_user()

        profile = CommissionnaireProfile.objects.create(
            user=user,
            display_name="Maison Pro",
            whatsapp_phone="+243990000000",
        )

        self.assertEqual(user.commissionnaire_profile, profile)

        with self.assertRaises(IntegrityError):
            CommissionnaireProfile.objects.create(
                user=user,
                display_name="Duplicate",
                whatsapp_phone="+243991111111",
            )

    def test_required_display_name_rejects_blank_after_trimming(self):
        user = self.create_user()
        profile = CommissionnaireProfile(
            user=user,
            display_name="   ",
            whatsapp_phone="+243990000000",
        )

        with self.assertRaisesMessage(ValidationError, "Nom affiche requis."):
            profile.full_clean()

    def test_profile_phone_is_required_and_normalized(self):
        user = self.create_user()
        profile = CommissionnaireProfile(
            user=user,
            display_name="Maison Pro",
            whatsapp_phone="0990000000",
        )

        profile.full_clean()

        self.assertEqual(profile.whatsapp_phone, "+243990000000")

    def test_invalid_profile_phone_is_rejected(self):
        user = self.create_user()
        profile = CommissionnaireProfile(
            user=user,
            display_name="Maison Pro",
            whatsapp_phone="not-a-phone",
        )

        with self.assertRaisesMessage(ValidationError, "Ce numero ne semble pas valide."):
            profile.full_clean()

    def test_publication_eligibility_requires_owner_and_profile_contact_data(self):
        ready_user = self.create_user()
        profile = CommissionnaireProfile.objects.create(
            user=ready_user,
            display_name="Maison Pro",
            whatsapp_phone="+243990000000",
        )

        self.assertTrue(profile.is_publication_eligible)

        ready_user.whatsapp_phone = ""
        ready_user.save(update_fields=["whatsapp_phone"])
        profile.refresh_from_db()

        self.assertFalse(profile.is_publication_eligible)

    def test_profile_update_preserves_primary_key_and_updates_timestamp(self):
        user = self.create_user()
        profile = CommissionnaireProfile.objects.create(
            user=user,
            display_name="Maison Pro",
            whatsapp_phone="+243990000000",
        )
        original_pk = profile.pk
        original_updated_at = profile.updated_at

        profile.display_name = "Maison Pro Kin"
        profile.save()
        profile.refresh_from_db()

        self.assertEqual(profile.pk, original_pk)
        self.assertGreaterEqual(profile.updated_at, original_updated_at)
        self.assertLessEqual(profile.updated_at, timezone.now())


class CommissionnaireProfileAdminTests(TestCase):
    def test_profile_model_is_registered_in_admin_with_safe_search_fields(self):
        model_admin = admin.site._registry[CommissionnaireProfile]

        self.assertIn("display_name", model_admin.list_display)
        self.assertIn("whatsapp_phone", model_admin.list_display)
        self.assertIn("display_name", model_admin.search_fields)
        self.assertIn("whatsapp_phone", model_admin.search_fields)
        self.assertIn("user__email", model_admin.search_fields)
