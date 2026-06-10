import phonenumbers
from django.core.exceptions import ValidationError


BLANK_WHATSAPP_PHONE_ERROR = "Entrez un numero WhatsApp valide."
INVALID_WHATSAPP_PHONE_ERROR = (
    "Ce numero ne semble pas valide. Verifiez l'indicatif et reessayez."
)


def normalize_whatsapp_phone(value):
    raw_value = (value or "").strip()
    if not raw_value:
        raise ValidationError(BLANK_WHATSAPP_PHONE_ERROR, code="required")

    try:
        parsed_phone = phonenumbers.parse(raw_value, "CD")
    except phonenumbers.NumberParseException as error:
        raise ValidationError(INVALID_WHATSAPP_PHONE_ERROR, code="invalid") from error

    if not (
        phonenumbers.is_possible_number(parsed_phone)
        and phonenumbers.is_valid_number(parsed_phone)
    ):
        raise ValidationError(INVALID_WHATSAPP_PHONE_ERROR, code="invalid")

    return phonenumbers.format_number(
        parsed_phone,
        phonenumbers.PhoneNumberFormat.E164,
    )
