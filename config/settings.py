import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured


BASE_DIR = Path(__file__).resolve().parent.parent


def load_local_env_file(path):
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key or not (key[0].isalpha() or key[0] == "_"):
            continue
        if not all(char.isalnum() or char == "_" for char in key):
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        os.environ.setdefault(key, value)


load_local_env_file(BASE_DIR / ".env")


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def google_social_apps_from_env():
    client_id = os.environ.get("GOOGLE_OAUTH_CLIENT_ID", "").strip()
    secret = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET", "").strip()
    placeholders = {
        "replace-with-google-client-id",
        "replace-with-google-client-secret",
    }
    if client_id in placeholders or secret in placeholders:
        return []
    if not client_id or not secret:
        return []
    return [{"client_id": client_id, "secret": secret}]


LOCAL_SECRET_KEY = "django-insecure-local-maison-dev-key-change-me"
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", LOCAL_SECRET_KEY)

DEBUG = env_bool("DJANGO_DEBUG", True)

if not DEBUG and SECRET_KEY == LOCAL_SECRET_KEY:
    raise ImproperlyConfigured("DJANGO_SECRET_KEY must be set when DJANGO_DEBUG is false.")

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "apps.core",
    "apps.accounts",
    "apps.listings",
    "apps.commissionnaires",
    "apps.leads",
    "apps.moderation",
    "apps.audit",
    "apps.pwa",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("DJANGO_SQLITE_NAME", BASE_DIR / "db.sqlite3"),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "fr-fr"

TIME_ZONE = "Africa/Kinshasa"

USE_I18N = True

USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static", BASE_DIR / "static_src"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

AUTH_USER_MODEL = "accounts.CustomUser"

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
        "OAUTH_PKCE_ENABLED": True,
        "EMAIL_AUTHENTICATION": True,
        "APPS": google_social_apps_from_env(),
    }
}
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True

LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "accounts:dashboard"
LOGOUT_REDIRECT_URL = "core:home"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LISTING_AVAILABILITY_FRESHNESS_DAYS = 14
