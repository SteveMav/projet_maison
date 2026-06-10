from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

from django.conf import settings
from django.test import SimpleTestCase

import config.settings as project_settings


class GoogleAuthConfigurationTests(SimpleTestCase):
    def test_allauth_and_google_provider_apps_are_installed(self):
        expected_apps = {
            "django.contrib.sites",
            "allauth",
            "allauth.account",
            "allauth.socialaccount",
            "allauth.socialaccount.providers.google",
        }

        self.assertTrue(expected_apps.issubset(set(settings.INSTALLED_APPS)))

    def test_allauth_middleware_is_configured_after_messages_middleware(self):
        allauth_middleware = "allauth.account.middleware.AccountMiddleware"
        message_middleware = "django.contrib.messages.middleware.MessageMiddleware"

        self.assertIn(allauth_middleware, settings.MIDDLEWARE)
        self.assertGreater(
            settings.MIDDLEWARE.index(allauth_middleware),
            settings.MIDDLEWARE.index(message_middleware),
        )

    def test_model_backend_and_allauth_backend_are_configured(self):
        self.assertEqual(
            settings.AUTHENTICATION_BACKENDS,
            [
                "django.contrib.auth.backends.ModelBackend",
                "allauth.account.auth_backends.AuthenticationBackend",
            ],
        )

    def test_site_id_is_configured(self):
        self.assertEqual(settings.SITE_ID, 1)

    def test_google_provider_uses_minimal_scopes_pkce_and_online_access(self):
        google_settings = settings.SOCIALACCOUNT_PROVIDERS["google"]

        self.assertEqual(google_settings["SCOPE"], ["profile", "email"])
        self.assertTrue(google_settings["OAUTH_PKCE_ENABLED"])
        self.assertEqual(google_settings["AUTH_PARAMS"], {"access_type": "online"})
        self.assertNotIn("offline", str(google_settings).lower())

    def test_google_social_app_credentials_are_loaded_from_environment(self):
        with mock.patch.dict(
            "os.environ",
            {
                "GOOGLE_OAUTH_CLIENT_ID": "client-id-from-env",
                "GOOGLE_OAUTH_CLIENT_SECRET": "secret-from-env",
            },
        ):
            apps = project_settings.google_social_apps_from_env()

        self.assertEqual(
            apps,
            [{"client_id": "client-id-from-env", "secret": "secret-from-env"}],
        )

    def test_google_social_app_is_absent_without_environment_credentials(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            apps = project_settings.google_social_apps_from_env()

        self.assertEqual(apps, [])

    def test_google_social_app_ignores_placeholder_environment_credentials(self):
        with mock.patch.dict(
            "os.environ",
            {
                "GOOGLE_OAUTH_CLIENT_ID": "replace-with-google-client-id",
                "GOOGLE_OAUTH_CLIENT_SECRET": "replace-with-google-client-secret",
            },
            clear=True,
        ):
            apps = project_settings.google_social_apps_from_env()

        self.assertEqual(apps, [])

    def test_local_env_file_loader_sets_missing_values_without_overwriting(self):
        with TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text(
                "\n".join(
                    [
                        "GOOGLE_OAUTH_CLIENT_ID=client-id-from-file",
                        "GOOGLE_OAUTH_CLIENT_SECRET=\"secret-from-file\"",
                        "DJANGO_DEBUG=False",
                    ]
                )
            )
            with mock.patch.dict(
                "os.environ",
                {"GOOGLE_OAUTH_CLIENT_ID": "already-set"},
                clear=True,
            ):
                project_settings.load_local_env_file(env_path)

                self.assertEqual(
                    project_settings.os.environ["GOOGLE_OAUTH_CLIENT_ID"],
                    "already-set",
                )
                self.assertEqual(
                    project_settings.os.environ["GOOGLE_OAUTH_CLIENT_SECRET"],
                    "secret-from-file",
                )
                self.assertEqual(project_settings.os.environ["DJANGO_DEBUG"], "False")

    def test_google_setup_is_documented_with_placeholder_values_only(self):
        readme = (Path(settings.BASE_DIR) / "README.md").read_text()
        env_example = (Path(settings.BASE_DIR) / ".env.example").read_text()

        self.assertIn("GOOGLE_OAUTH_CLIENT_ID=replace-with-google-client-id", env_example)
        self.assertIn(
            "GOOGLE_OAUTH_CLIENT_SECRET=replace-with-google-client-secret",
            env_example,
        )
        self.assertIn("/accounts/google/login/callback/", readme)
        self.assertNotIn("AIza", readme + env_example)
