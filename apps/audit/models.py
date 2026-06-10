from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class AuditEvent(models.Model):
    event_type = models.CharField(max_length=100)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="audit_events",
    )
    target_id = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-timestamp", "id"]
        indexes = [
            models.Index(fields=["event_type"]),
            models.Index(fields=["target_id"]),
            models.Index(fields=["timestamp"]),
        ]

    def __str__(self):
        return f"{self.event_type} by {self.actor} at {self.timestamp}"

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError("Audit events are append-only and cannot be updated.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Audit events are append-only and cannot be deleted.")
