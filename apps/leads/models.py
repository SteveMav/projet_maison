from django.conf import settings
from django.db import models

class Lead(models.Model):
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="leads",
    )
    listing = models.ForeignKey(
        "listings.Listing",
        on_delete=models.CASCADE,
        related_name="leads",
    )
    commissionnaire_profile = models.ForeignKey(
        "commissionnaires.CommissionnaireProfile",
        on_delete=models.CASCADE,
        related_name="leads",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    acquisition_context = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at", "id"]
        indexes = [
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Lead by {self.tenant} for Listing {self.listing.id} at {self.created_at}"


class LeadStatusEvent(models.Model):
    STATUS_CHOICES = [
        ("new", "Nouveau"),
        ("contacted", "Contacté"),
        ("closed", "Fermé"),
    ]

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="status_events",
    )
    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default="new",
    )
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-changed_at", "id"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["changed_at"]),
        ]

    def __str__(self):
        return f"Status event {self.status} for Lead {self.lead.id} at {self.changed_at}"


class WhatsAppHandoffAttempt(models.Model):
    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="handoff_attempts",
    )
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-attempted_at", "id"]
        indexes = [
            models.Index(fields=["attempted_at"]),
        ]

    def __str__(self):
        return f"Handoff attempt for Lead {self.lead.id} at {self.attempted_at}"

