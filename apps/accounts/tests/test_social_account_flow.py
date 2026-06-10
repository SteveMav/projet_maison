from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialLogin
from allauth.socialaccount.providers.google.provider import GoogleProvider
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase


class SocialAccountFlowTests(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        app = SocialApp.objects.create(
            provider="google",
            name="Google",
            client_id="placeholder-client-id",
            secret="",
        )
        app.sites.add(Site.objects.get_current())
        self.provider = GoogleProvider(self.request, app=app)

    def make_google_social_login(self, email="Tenant@Example.COM", verified=True):
        normalized_email = get_user_model().objects.normalize_email(email).lower()
        user = get_user_model()(email=normalized_email, whatsapp_phone="")
        account = SocialAccount(
            provider="google",
            uid="google-user-123",
            extra_data={"email": email},
        )
        email_address = EmailAddress(
            email=normalized_email,
            verified=verified,
            primary=True,
        )
        return SocialLogin(
            user=user,
            account=account,
            email_addresses=[email_address],
            provider=self.provider,
        )

    def test_google_email_authentication_is_explicit_and_auto_connects(self):
        google_settings = settings.SOCIALACCOUNT_PROVIDERS["google"]

        self.assertTrue(google_settings["EMAIL_AUTHENTICATION"])
        self.assertTrue(settings.SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT)

    def test_verified_google_email_links_existing_local_user_without_duplicate(self):
        existing_user = get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
        )
        social_login = self.make_google_social_login()

        social_login.lookup()

        self.assertEqual(social_login.user.pk, existing_user.pk)
        self.assertEqual(
            get_user_model().objects.filter(email__iexact="tenant@example.com").count(),
            1,
        )

    def test_unverified_google_email_does_not_link_existing_local_user(self):
        get_user_model().objects.create_user(
            email="tenant@example.com",
            password="StrongPass123!",
        )
        social_login = self.make_google_social_login(verified=False)

        social_login.lookup()

        self.assertIsNone(social_login.user.pk)

    def test_google_social_signup_uses_custom_user_and_keeps_whatsapp_blank(self):
        social_login = self.make_google_social_login(email="new@example.com")

        self.assertIsInstance(social_login.user, get_user_model())
        self.assertEqual(social_login.user.email, "new@example.com")
        self.assertEqual(social_login.user.whatsapp_phone, "")
        self.assertFalse(social_login.user.is_whatsapp_ready)
