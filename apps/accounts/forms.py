from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from apps.accounts.validators import normalize_whatsapp_phone


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Adresse e-mail",
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "class": "form-control",
            }
        ),
    )
    password = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": "form-control",
            }
        ),
    )

    error_messages = {
        "invalid_login": (
            "Connexion impossible. Verifiez email et mot de passe."
        ),
        "inactive": "Ce compte est inactif.",
    }

    def clean_username(self):
        return self.cleaned_data["username"].strip().lower()

    def clean(self):
        try:
            return super().clean()
        except ValidationError as error:
            if getattr(error, "code", "") == "invalid_login":
                self.add_error("username", error)
                return self.cleaned_data
            raise


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ("email",)
        labels = {"email": "Adresse e-mail"}
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "autocomplete": "email",
                    "class": "form-control",
                }
            )
        }
        error_messages = {
            "email": {
                "unique": "Un compte existe deja avec cette adresse e-mail.",
            }
        }

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        normalized_email = get_user_model().objects.normalize_email(email).lower()
        if get_user_model().objects.filter(email__iexact=normalized_email).exists():
            raise ValidationError("Un compte existe deja avec cette adresse e-mail.")
        return normalized_email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Les mots de passe ne correspondent pas.")

        if password1:
            try:
                user = self.Meta.model(email=cleaned_data.get("email", ""))
                validate_password(password1, user=user)
            except ValidationError as error:
                self.add_error("password1", error)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class WhatsAppPhoneCompletionForm(forms.Form):
    whatsapp_phone = forms.CharField(
        label="Numero WhatsApp",
        required=False,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "tel",
                "class": "form-control",
                "inputmode": "tel",
                "placeholder": "Exemple : +243...",
                "type": "tel",
                "aria-describedby": "whatsapp-phone-help whatsapp-phone-error",
            }
        ),
    )

    def clean_whatsapp_phone(self):
        return normalize_whatsapp_phone(self.cleaned_data.get("whatsapp_phone", ""))


class LightweightIdentificationForm(forms.Form):
    first_name = forms.CharField(
        label="Prénom",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "given-name",
            }
        ),
    )
    last_name = forms.CharField(
        label="Nom de famille",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "family-name",
            }
        ),
    )
    whatsapp_phone = forms.CharField(
        label="Numéro WhatsApp",
        required=True,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "tel",
                "class": "form-control",
                "inputmode": "tel",
                "placeholder": "Exemple : +243...",
                "type": "tel",
            }
        ),
    )
    consent = forms.BooleanField(
        label="J'accepte de partager mes coordonnées avec le Commissionnaire",
        required=True,
        error_messages={
            "required": "Vous devez cocher cette case pour continuer.",
        },
    )

    def clean_whatsapp_phone(self):
        phone = self.cleaned_data.get("whatsapp_phone", "")
        # normalize_whatsapp_phone raises ValidationError on invalid format
        return normalize_whatsapp_phone(phone)

    def clean_consent(self):
        consent = self.cleaned_data.get("consent")
        if not consent:
            raise ValidationError("Vous devez cocher cette case pour continuer.")
        return consent
