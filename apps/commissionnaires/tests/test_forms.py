from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.commissionnaires.forms import CommissionnaireProfileForm
from apps.commissionnaires.models import CommissionnaireProfile


class CommissionnaireProfileFormTests(TestCase):
    def create_user(self, email="pro@example.com", whatsapp_phone="+243990000000"):
        return get_user_model().objects.create_user(
            email=email,
            password="StrongPass123!",
            whatsapp_phone=whatsapp_phone,
        )

    def test_valid_data_creates_profile_with_trimmed_name_and_normalized_phone(self):
        user = self.create_user()
        form = CommissionnaireProfileForm(
            data={
                "display_name": "  Maison Pro  ",
                "whatsapp_phone": "0990000000",
            },
            user=user,
        )

        self.assertTrue(form.is_valid(), form.errors)
        profile = form.save(commit=False)
        profile.user = user
        profile.save()

        self.assertEqual(profile.display_name, "Maison Pro")
        self.assertEqual(profile.whatsapp_phone, "+243990000000")
        self.assertTrue(profile.is_publication_eligible)

    def test_initial_phone_uses_user_whatsapp_phone_when_creating_profile(self):
        user = self.create_user(whatsapp_phone="+243991111111")

        form = CommissionnaireProfileForm(user=user)

        self.assertEqual(form.initial["whatsapp_phone"], "+243991111111")

    def test_valid_data_updates_existing_profile_without_recreating_it(self):
        user = self.create_user()
        profile = CommissionnaireProfile.objects.create(
            user=user,
            display_name="Maison Pro",
            whatsapp_phone="+243990000000",
        )
        form = CommissionnaireProfileForm(
            data={
                "display_name": "Maison Pro Kin",
                "whatsapp_phone": "+243991111111",
            },
            instance=profile,
            user=user,
        )

        self.assertTrue(form.is_valid(), form.errors)
        updated_profile = form.save()

        self.assertEqual(updated_profile.pk, profile.pk)
        self.assertEqual(CommissionnaireProfile.objects.count(), 1)
        self.assertEqual(updated_profile.display_name, "Maison Pro Kin")
        self.assertEqual(updated_profile.whatsapp_phone, "+243991111111")

    def test_blank_display_name_returns_field_level_error(self):
        form = CommissionnaireProfileForm(
            data={"display_name": "   ", "whatsapp_phone": "+243990000000"},
            user=self.create_user(),
        )

        self.assertFalse(form.is_valid())
        self.assertIn("display_name", form.errors)
        self.assertIn("Nom affiche requis.", form.errors["display_name"])
        self.assertEqual(CommissionnaireProfile.objects.count(), 0)

    def test_invalid_phone_returns_field_level_error(self):
        form = CommissionnaireProfileForm(
            data={"display_name": "Maison Pro", "whatsapp_phone": "not-a-phone"},
            user=self.create_user(),
        )

        self.assertFalse(form.is_valid())
        self.assertIn("whatsapp_phone", form.errors)
        self.assertIn("Ce numero ne semble pas valide.", form.errors["whatsapp_phone"][0])
        self.assertEqual(CommissionnaireProfile.objects.count(), 0)

    def test_blank_phone_returns_required_field_level_error(self):
        form = CommissionnaireProfileForm(
            data={"display_name": "Maison Pro", "whatsapp_phone": ""},
            user=self.create_user(),
        )

        self.assertFalse(form.is_valid())
        self.assertIn("whatsapp_phone", form.errors)
        self.assertIn("Entrez un numero WhatsApp valide.", form.errors["whatsapp_phone"])
        self.assertEqual(CommissionnaireProfile.objects.count(), 0)
