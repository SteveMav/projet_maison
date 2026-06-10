from django import forms
from django.core.exceptions import ValidationError

from apps.accounts.validators import BLANK_WHATSAPP_PHONE_ERROR, normalize_whatsapp_phone
from apps.commissionnaires.models import CommissionnaireProfile


class CommissionnaireProfileForm(forms.ModelForm):
    class Meta:
        model = CommissionnaireProfile
        fields = ("display_name", "whatsapp_phone")
        labels = {
            "display_name": "Nom affiche",
            "whatsapp_phone": "Numero WhatsApp professionnel",
        }
        error_messages = {
            "display_name": {
                "required": "Nom affiche requis.",
            },
            "whatsapp_phone": {
                "required": BLANK_WHATSAPP_PHONE_ERROR,
            },
        }
        widgets = {
            "display_name": forms.TextInput(
                attrs={
                    "autocomplete": "organization",
                    "class": "form-control",
                    "aria-describedby": "display-name-help display-name-error",
                }
            ),
            "whatsapp_phone": forms.TextInput(
                attrs={
                    "autocomplete": "tel",
                    "class": "form-control",
                    "inputmode": "tel",
                    "placeholder": "Exemple : +243...",
                    "type": "tel",
                    "aria-describedby": "whatsapp-phone-help whatsapp-phone-error",
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        if not self.instance.pk and user and getattr(user, "whatsapp_phone", ""):
            self.initial.setdefault("whatsapp_phone", user.whatsapp_phone)

    def clean_display_name(self):
        display_name = self.cleaned_data.get("display_name", "").strip()
        if not display_name:
            raise ValidationError("Nom affiche requis.", code="required")
        return display_name

    def clean_whatsapp_phone(self):
        return normalize_whatsapp_phone(self.cleaned_data.get("whatsapp_phone", ""))

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user and not profile.user_id:
            profile.user = self.user
        if commit:
            profile.save()
            self.save_m2m()
        return profile
