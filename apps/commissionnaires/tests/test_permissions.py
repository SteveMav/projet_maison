from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.commissionnaires.models import CommissionnaireProfile


class CommissionnaireProfilePermissionTests(TestCase):
    def create_user(self, email="pro@example.com", whatsapp_phone="+243990000000"):
        return get_user_model().objects.create_user(
            email=email,
            password="StrongPass123!",
            whatsapp_phone=whatsapp_phone,
        )

    def test_profile_routes_require_authentication_with_next(self):
        response = self.client.get(reverse("commissionnaires:profile"))

        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('commissionnaires:profile')}",
        )

    def test_user_without_whatsapp_phone_is_routed_to_completion(self):
        user = self.create_user(whatsapp_phone="")
        self.client.force_login(user)

        response = self.client.get(reverse("commissionnaires:profile_create"))

        self.assertRedirects(
            response,
            (
                f"{reverse('accounts:phone_complete')}"
                f"?next={reverse('commissionnaires:profile_create')}"
            ),
            fetch_redirect_response=False,
        )

    def test_user_cannot_access_another_profile_edit_route(self):
        owner = self.create_user(email="owner@example.com")
        other_profile = CommissionnaireProfile.objects.create(
            user=owner,
            display_name="Owner Pro",
            whatsapp_phone="+243990000000",
        )
        intruder = self.create_user(email="intruder@example.com")
        self.client.force_login(intruder)

        response = self.client.get(
            reverse("commissionnaires:profile_edit", args=[other_profile.pk])
        )

        self.assertContains(
            response,
            "Vous n'avez pas acces a ce profil.",
            status_code=404,
        )
        self.assertNotContains(response, "Owner Pro", status_code=404)
        self.assertNotContains(response, "+243990000000", status_code=404)

    def test_user_cannot_access_another_profile_detail_route(self):
        owner = self.create_user(email="owner@example.com")
        other_profile = CommissionnaireProfile.objects.create(
            user=owner,
            display_name="Owner Pro",
            whatsapp_phone="+243990000000",
        )
        intruder = self.create_user(email="intruder@example.com")
        self.client.force_login(intruder)

        response = self.client.get(
            reverse("commissionnaires:profile_detail", args=[other_profile.pk])
        )

        self.assertContains(
            response,
            "Vous n'avez pas acces a ce profil.",
            status_code=404,
        )
        self.assertNotContains(response, "Owner Pro", status_code=404)
        self.assertNotContains(response, "+243990000000", status_code=404)

    def test_whatsapp_ready_user_reaches_profile_creation_surface(self):
        self.client.force_login(self.create_user())

        response = self.client.get(reverse("commissionnaires:profile_create"))

        self.assertEqual(response.status_code, 200)
