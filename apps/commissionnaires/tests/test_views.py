from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.commissionnaires.models import CommissionnaireProfile


class CommissionnaireProfileViewTests(TestCase):
    def create_user(self, email="pro@example.com", whatsapp_phone="+243990000000"):
        return get_user_model().objects.create_user(
            email=email,
            password="StrongPass123!",
            whatsapp_phone=whatsapp_phone,
        )

    def test_profile_entry_redirects_user_without_profile_to_creation(self):
        self.client.force_login(self.create_user())

        response = self.client.get(reverse("commissionnaires:profile"))

        self.assertRedirects(
            response,
            reverse("commissionnaires:profile_create"),
            fetch_redirect_response=False,
        )

    def test_profile_entry_redirects_user_with_profile_to_detail(self):
        user = self.create_user()
        profile = CommissionnaireProfile.objects.create(
            user=user,
            display_name="Maison Pro",
            whatsapp_phone="+243990000000",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("commissionnaires:profile"))

        self.assertRedirects(
            response,
            reverse("commissionnaires:profile_detail", args=[profile.pk]),
            fetch_redirect_response=False,
        )

    def test_create_profile_get_prefills_user_whatsapp_phone(self):
        user = self.create_user(whatsapp_phone="+243991111111")
        self.client.force_login(user)

        response = self.client.get(reverse("commissionnaires:profile_create"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Profil commissionnaire")
        self.assertContains(response, 'value="+243991111111"')

    def test_valid_profile_post_creates_profile_and_redirects_to_detail(self):
        user = self.create_user()
        self.client.force_login(user)

        response = self.client.post(
            reverse("commissionnaires:profile_create"),
            {
                "display_name": "  Maison Pro  ",
                "whatsapp_phone": "0990000000",
            },
        )

        profile = CommissionnaireProfile.objects.get(user=user)
        self.assertRedirects(
            response,
            reverse("commissionnaires:profile_detail", args=[profile.pk]),
            fetch_redirect_response=False,
        )
        self.assertEqual(profile.display_name, "Maison Pro")
        self.assertEqual(profile.whatsapp_phone, "+243990000000")

    def test_invalid_profile_post_shows_field_errors_and_does_not_create_profile(self):
        self.client.force_login(self.create_user())

        response = self.client.post(
            reverse("commissionnaires:profile_create"),
            {"display_name": "   ", "whatsapp_phone": "not-a-phone"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nom affiche requis.")
        self.assertContains(response, "Ce numero ne semble pas valide.")
        self.assertEqual(CommissionnaireProfile.objects.count(), 0)

    def test_create_route_redirects_existing_profile_without_duplicate(self):
        user = self.create_user()
        profile = CommissionnaireProfile.objects.create(
            user=user,
            display_name="Maison Pro",
            whatsapp_phone="+243990000000",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("commissionnaires:profile_create"))

        self.assertRedirects(
            response,
            reverse("commissionnaires:profile_detail", args=[profile.pk]),
            fetch_redirect_response=False,
        )
        self.assertEqual(CommissionnaireProfile.objects.count(), 1)

    def test_edit_profile_updates_same_row_and_redirects_to_detail(self):
        user = self.create_user()
        profile = CommissionnaireProfile.objects.create(
            user=user,
            display_name="Maison Pro",
            whatsapp_phone="+243990000000",
        )
        original_pk = profile.pk
        self.client.force_login(user)

        response = self.client.post(
            reverse("commissionnaires:profile_edit", args=[profile.pk]),
            {
                "display_name": "Maison Pro Kin",
                "whatsapp_phone": "+243991111111",
            },
        )

        profile.refresh_from_db()
        self.assertRedirects(
            response,
            reverse("commissionnaires:profile_detail", args=[profile.pk]),
            fetch_redirect_response=False,
        )
        self.assertEqual(profile.pk, original_pk)
        self.assertEqual(CommissionnaireProfile.objects.count(), 1)
        self.assertEqual(profile.display_name, "Maison Pro Kin")
        self.assertEqual(profile.whatsapp_phone, "+243991111111")

    def test_edit_get_renders_existing_profile_values(self):
        user = self.create_user()
        profile = CommissionnaireProfile.objects.create(
            user=user,
            display_name="Maison Pro",
            whatsapp_phone="+243990000000",
        )
        self.client.force_login(user)

        response = self.client.get(
            reverse("commissionnaires:profile_edit", args=[profile.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Maison Pro")
        self.assertContains(response, 'value="+243990000000"')

    def test_profile_detail_uses_compact_french_profile_copy(self):
        user = self.create_user()
        profile = CommissionnaireProfile.objects.create(
            user=user,
            display_name="Maison Pro",
            whatsapp_phone="+243990000000",
        )
        self.client.force_login(user)

        response = self.client.get(
            reverse("commissionnaires:profile_detail", args=[profile.pk])
        )

        self.assertContains(response, "Espace pro")
        self.assertContains(response, "Profil commissionnaire")
        self.assertContains(response, "Nom affiche")
        self.assertContains(response, "Numero WhatsApp professionnel")
        self.assertContains(response, "profile-summary")
        self.assertContains(
            response,
            reverse("commissionnaires:profile_edit", args=[profile.pk]),
        )
