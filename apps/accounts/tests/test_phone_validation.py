from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from apps.accounts.validators import normalize_whatsapp_phone


class WhatsAppPhoneValidationTests(SimpleTestCase):
    def test_blank_phone_is_rejected(self):
        with self.assertRaisesMessage(ValidationError, "Entrez un numero WhatsApp valide."):
            normalize_whatsapp_phone("")

    def test_malformed_phone_is_rejected(self):
        with self.assertRaisesMessage(
            ValidationError,
            "Ce numero ne semble pas valide. Verifiez l'indicatif et reessayez.",
        ):
            normalize_whatsapp_phone("not-a-phone")

    def test_valid_international_drc_phone_normalizes_to_e164(self):
        self.assertEqual(
            normalize_whatsapp_phone("+243990000000"),
            "+243990000000",
        )

    def test_valid_local_drc_phone_normalizes_to_e164(self):
        self.assertEqual(
            normalize_whatsapp_phone("0990000000"),
            "+243990000000",
        )

    def test_valid_non_drc_international_phone_is_accepted(self):
        self.assertEqual(
            normalize_whatsapp_phone("+33612345678"),
            "+33612345678",
        )
