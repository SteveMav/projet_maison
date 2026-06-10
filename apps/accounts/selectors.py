from django.core.exceptions import ValidationError

from apps.accounts.validators import normalize_whatsapp_phone


def user_has_whatsapp_phone(user):
    if not getattr(user, "is_authenticated", False):
        return False

    try:
        normalize_whatsapp_phone(getattr(user, "whatsapp_phone", ""))
    except ValidationError:
        return False

    return True
