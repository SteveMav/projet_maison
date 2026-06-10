from django.contrib import admin
from apps.audit.models import AuditEvent


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ("event_type", "actor", "target_id", "timestamp")
    list_filter = ("event_type", "timestamp")
    search_fields = ("target_id", "actor__email", "actor__username")
    readonly_fields = ("event_type", "actor", "target_id", "timestamp", "metadata")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
