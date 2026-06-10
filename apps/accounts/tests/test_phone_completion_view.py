from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from allauth.socialaccount.models import SocialAccount


class PhoneCompletionViewTests(TestCase):
    def test_phone_completion_requires_authentication(self):
        response = self.client.get(reverse("accounts:phone_complete"))

        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('accounts:phone_complete')}",
        )

    def test_get_renders_form_and_preserves_safe_next(self):
        user = get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
        )
        self.client.force_login(user)

        response = self.client.get(
            f"{reverse('accounts:phone_complete')}?next=/phone-action/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Completez votre numero WhatsApp")
        self.assertContains(response, "Maison ne lit pas vos conversations WhatsApp.")
        self.assertContains(response, 'name="next" value="/phone-action/"')

    def test_valid_post_saves_normalized_phone_and_redirects_to_safe_next(self):
        user = get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("accounts:phone_complete"),
            {
                "whatsapp_phone": "0990000000",
                "next": "/phone-action/",
            },
        )

        self.assertRedirects(response, "/phone-action/", fetch_redirect_response=False)
        user.refresh_from_db()
        self.assertEqual(user.whatsapp_phone, "+243990000000")

    def test_valid_post_with_unsafe_next_redirects_to_dashboard(self):
        user = get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("accounts:phone_complete"),
            {
                "whatsapp_phone": "+243990000000",
                "next": "https://example.net/phish",
            },
        )

        self.assertRedirects(response, reverse("accounts:dashboard"))

    def test_invalid_post_returns_field_error_and_preserves_safe_next(self):
        user = get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("accounts:phone_complete"),
            {
                "whatsapp_phone": "not-a-phone",
                "next": "/phone-action/",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ce numero ne semble pas valide.")
        self.assertContains(response, 'name="next" value="/phone-action/"')
        self.assertContains(response, 'value="not-a-phone"')
        user.refresh_from_db()
        self.assertEqual(user.whatsapp_phone, "")

    def test_blank_post_returns_field_level_error(self):
        user = get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("accounts:phone_complete"),
            {"whatsapp_phone": "", "next": "/phone-action/"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Entrez un numero WhatsApp valide.")
        user.refresh_from_db()
        self.assertEqual(user.whatsapp_phone, "")

    def test_email_password_user_completion_preserves_identity_and_session(self):
        user = get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
        )
        self.client.force_login(user)
        session_user_id = self.client.session["_auth_user_id"]

        response = self.client.post(
            reverse("accounts:phone_complete"),
            {"whatsapp_phone": "+243990000000"},
        )

        self.assertRedirects(response, reverse("accounts:dashboard"))
        user.refresh_from_db()
        self.assertEqual(user.email, "tenant@example.com")
        self.assertTrue(user.check_password("StrongPass123!"))
        self.assertEqual(user.whatsapp_phone, "+243990000000")
        self.assertEqual(self.client.session["_auth_user_id"], session_user_id)

    def test_google_user_completion_preserves_social_link_and_session(self):
        user = get_user_model().objects.create_user(
            email="google-user@example.com",
            password=None,
        )
        SocialAccount.objects.create(
            user=user,
            provider="google",
            uid="google-user-123",
        )
        self.client.force_login(user)
        session_user_id = self.client.session["_auth_user_id"]

        response = self.client.post(
            reverse("accounts:phone_complete"),
            {"whatsapp_phone": "+243990000000"},
        )

        self.assertRedirects(response, reverse("accounts:dashboard"))
        user.refresh_from_db()
        self.assertFalse(user.has_usable_password())
        self.assertEqual(user.email, "google-user@example.com")
        self.assertEqual(user.whatsapp_phone, "+243990000000")
        self.assertTrue(
            SocialAccount.objects.filter(
                user=user,
                provider="google",
                uid="google-user-123",
            ).exists()
        )
        self.assertEqual(self.client.session["_auth_user_id"], session_user_id)
