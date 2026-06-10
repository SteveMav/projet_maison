from django.contrib import admin

from apps.commissionnaires.models import CommissionnaireProfile


@admin.register(CommissionnaireProfile)
class CommissionnaireProfileAdmin(admin.ModelAdmin):
    list_display = ("display_name", "whatsapp_phone", "user", "updated_at")
    search_fields = ("display_name", "whatsapp_phone", "user__email")
    readonly_fields = ("created_at", "updated_at")
