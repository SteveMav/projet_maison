from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.accounts.selectors import user_has_whatsapp_phone
from apps.accounts.validators import normalize_whatsapp_phone


class CommissionnaireProfile(models.Model):
    """Stable attribution target for future Listing and Lead foreign keys."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="commissionnaire_profile",
    )
    display_name = models.CharField(max_length=120)
    whatsapp_phone = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_name", "id"]
        verbose_name = "Commissionnaire profile"
        verbose_name_plural = "Commissionnaire profiles"

    def __str__(self):
        return self.display_name

    @property
    def is_publication_eligible(self):
        if not user_has_whatsapp_phone(self.user):
            return False
        if not self.display_name.strip():
            return False
        try:
            normalize_whatsapp_phone(self.whatsapp_phone)
        except ValidationError:
            return False
        return True

    def clean(self):
        super().clean()
        self.display_name = self.display_name.strip()
        if not self.display_name:
            raise ValidationError({"display_name": "Nom affiche requis."})
        self.whatsapp_phone = normalize_whatsapp_phone(self.whatsapp_phone)

    def save(self, *args, **kwargs):
        self.display_name = self.display_name.strip()
        self.whatsapp_phone = normalize_whatsapp_phone(self.whatsapp_phone)
        super().save(*args, **kwargs)
