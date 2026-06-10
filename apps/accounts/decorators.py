from functools import wraps
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect, resolve_url

from apps.accounts.selectors import user_has_whatsapp_phone


def redirect_to_phone_completion(request, phone_complete_url="accounts:phone_complete"):
    completion_url = resolve_url(phone_complete_url)
    separator = "&" if "?" in completion_url else "?"
    return redirect(
        f"{completion_url}{separator}{urlencode({'next': request.get_full_path()})}"
    )


def whatsapp_phone_required(view_func=None, phone_complete_url="accounts:phone_complete"):
    def decorator(func):
        @wraps(func)
        def wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(
                    request.get_full_path(),
                    login_url=settings.LOGIN_URL,
                )
            if user_has_whatsapp_phone(request.user):
                return func(request, *args, **kwargs)
            return redirect_to_phone_completion(request, phone_complete_url)

        return wrapped

    if view_func is None:
        return decorator
    return decorator(view_func)
