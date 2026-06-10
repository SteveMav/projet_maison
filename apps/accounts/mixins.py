from django.contrib.auth.mixins import AccessMixin

from apps.accounts.decorators import redirect_to_phone_completion
from apps.accounts.selectors import user_has_whatsapp_phone


class WhatsAppPhoneRequiredMixin(AccessMixin):
    phone_complete_url = "accounts:phone_complete"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if user_has_whatsapp_phone(request.user):
            return super().dispatch(request, *args, **kwargs)
        return redirect_to_phone_completion(request, self.phone_complete_url)
