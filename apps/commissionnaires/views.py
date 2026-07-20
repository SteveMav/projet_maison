from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from urllib.parse import urlencode
from django.conf import settings

from apps.accounts.mixins import WhatsAppPhoneRequiredMixin
from apps.commissionnaires.forms import CommissionnaireProfileForm
from apps.commissionnaires.models import CommissionnaireProfile
from apps.listings.forms import ListingSubmissionForm
from apps.listings.services import submit_listing_for_commissionnaire
from apps.listings.models import Listing


class CommissionnaireProfileEntryView(WhatsAppPhoneRequiredMixin, View):
    def get(self, request):
        profile = CommissionnaireProfile.objects.filter(user=request.user).first()
        if profile:
            return redirect("commissionnaires:profile_detail", pk=profile.pk)
        return redirect("commissionnaires:profile_create")


class CommissionnaireProfileCreateView(WhatsAppPhoneRequiredMixin, View):
    template_name = "commissionnaires/profile_form.html"

    def dispatch(self, request, *args, **kwargs):
        existing_profile = CommissionnaireProfile.objects.filter(user=request.user).first()
        if existing_profile:
            return redirect("commissionnaires:profile_detail", pk=existing_profile.pk)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                "form": CommissionnaireProfileForm(user=request.user),
                "title": "Profil commissionnaire",
                "submit_label": "Enregistrer le profil",
            },
        )

    def post(self, request):
        form = CommissionnaireProfileForm(data=request.POST, user=request.user)
        if form.is_valid():
            profile = form.save()
            next_url = request.GET.get("next") or request.POST.get("next")
            if next_url:
                return redirect(next_url)
            return redirect("commissionnaires:profile_detail", pk=profile.pk)
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "title": "Profil commissionnaire",
                "submit_label": "Enregistrer le profil",
            },
        )


class OwnedCommissionnaireProfileView(WhatsAppPhoneRequiredMixin, View):
    permission_template_name = "commissionnaires/permission_denied.html"

    def get_owned_profile(self):
        return CommissionnaireProfile.objects.filter(
            pk=self.kwargs["pk"],
            user=self.request.user,
        ).first()

    def render_no_profile_access(self):
        return render(
            self.request,
            self.permission_template_name,
            {"profile_url": reverse("commissionnaires:profile")},
            status=404,
        )


class CommissionnaireProfileDetailView(OwnedCommissionnaireProfileView):
    template_name = "commissionnaires/profile_detail.html"

    def get(self, request, pk):
        profile = self.get_owned_profile()
        if not profile:
            return self.render_no_profile_access()
        return render(request, self.template_name, {"profile": profile})


class CommissionnaireProfileEditView(OwnedCommissionnaireProfileView):
    template_name = "commissionnaires/profile_form.html"

    def get(self, request, pk):
        profile = self.get_owned_profile()
        if not profile:
            return self.render_no_profile_access()
        return render(
            request,
            self.template_name,
            {
                "form": CommissionnaireProfileForm(instance=profile, user=request.user),
                "profile": profile,
                "title": "Mettez a jour votre profil",
                "submit_label": "Enregistrer",
            },
        )

    def post(self, request, pk):
        profile = self.get_owned_profile()
        if not profile:
            return self.render_no_profile_access()
        form = CommissionnaireProfileForm(
            data=request.POST,
            instance=profile,
            user=request.user,
        )
        if form.is_valid():
            updated_profile = form.save()
            next_url = request.GET.get("next") or request.POST.get("next")
            if next_url:
                return redirect(next_url)
            return redirect("commissionnaires:profile_detail", pk=updated_profile.pk)
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "profile": profile,
                "title": "Mettez a jour votre profil",
                "submit_label": "Enregistrer",
            },
        )


@method_decorator(csrf_protect, name="dispatch")
class ListingSubmissionView(WhatsAppPhoneRequiredMixin, View):
    template_name = "commissionnaires/listing_submission.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        from apps.accounts.selectors import user_has_whatsapp_phone
        from apps.accounts.decorators import redirect_to_phone_completion
        if not user_has_whatsapp_phone(request.user):
            return redirect_to_phone_completion(request, "accounts:phone_complete")

        profile = CommissionnaireProfile.objects.filter(user=request.user).first()
        if not profile:
            completion_url = reverse("commissionnaires:profile_create")
            return redirect(f"{completion_url}?{urlencode({'next': request.get_full_path()})}")

        if not profile.is_publication_eligible:
            completion_url = reverse("commissionnaires:profile_edit", kwargs={"pk": profile.pk})
            return redirect(f"{completion_url}?{urlencode({'next': request.get_full_path()})}")

        return super().dispatch(request, *args, **kwargs)

    def get_valid_draft(self, request, profile_id):
        draft = request.session.get("listing_draft")
        if not draft:
            return None
        if draft.get("profile_id") != profile_id:
            return None
        
        from django.utils.dateparse import parse_datetime
        from django.utils import timezone
        import shutil
        from pathlib import Path
        
        timestamp = parse_datetime(draft.get("timestamp", ""))
        if not timestamp or (timezone.now() - timestamp).total_seconds() > 3600:
            draft_dir = Path(settings.MEDIA_ROOT) / "listing-preview-drafts" / str(profile_id) / draft["token"]
            shutil.rmtree(draft_dir, ignore_errors=True)
            request.session.pop("listing_draft", None)
            return None
            
        return draft

    def cleanup_draft_files(self, profile_id, token):
        import shutil
        from pathlib import Path
        draft_dir = Path(settings.MEDIA_ROOT) / "listing-preview-drafts" / str(profile_id) / token
        if draft_dir.exists():
            shutil.rmtree(draft_dir, ignore_errors=True)

    def cleanup_all_profile_drafts(self, profile_id):
        import shutil
        from pathlib import Path
        drafts_dir = Path(settings.MEDIA_ROOT) / "listing-preview-drafts" / str(profile_id)
        if drafts_dir.exists():
            shutil.rmtree(drafts_dir, ignore_errors=True)

    def get(self, request):
        profile = CommissionnaireProfile.objects.get(user=request.user)
        draft = self.get_valid_draft(request, profile.id)
        if draft:
            form = ListingSubmissionForm(
                initial={
                    "monthly_price_amount": draft["monthly_price_amount"],
                    "commune": draft["commune"],
                    "neighborhood": draft.get("neighborhood", ""),
                    "property_type": draft.get("property_type", Listing.PropertyType.APARTMENT),
                    "bedroom_count": draft["bedroom_count"],
                    "bathroom_count": draft.get("bathroom_count", 1),
                    "description": draft["description"],
                },
                has_draft_photos=True,
            )
        else:
            form = ListingSubmissionForm()
        return render(
            request,
            self.template_name,
            {"form": form, "state": "entry", "draft": draft},
        )

    def post(self, request):
        profile = CommissionnaireProfile.objects.get(user=request.user)
        action = request.POST.get("action", "preview")
        
        previous_draft = self.get_valid_draft(request, profile.id)
        has_draft_photos = previous_draft is not None and len(previous_draft.get("photos", [])) >= 3

        if action == "edit":
            if not previous_draft:
                return redirect("commissionnaires:listing_submit")
            form = ListingSubmissionForm(
                initial={
                    "monthly_price_amount": previous_draft["monthly_price_amount"],
                    "commune": previous_draft["commune"],
                    "neighborhood": previous_draft.get("neighborhood", ""),
                    "property_type": previous_draft.get("property_type", Listing.PropertyType.APARTMENT),
                    "bedroom_count": previous_draft["bedroom_count"],
                    "bathroom_count": previous_draft.get("bathroom_count", 1),
                    "description": previous_draft["description"],
                },
                has_draft_photos=has_draft_photos,
            )
            return render(
                request,
                self.template_name,
                {"form": form, "state": "entry", "draft": previous_draft},
            )

        elif action == "preview":
            form = ListingSubmissionForm(
                data=request.POST,
                files=request.FILES,
                has_draft_photos=has_draft_photos,
            )
            if form.is_valid():
                import uuid
                from pathlib import Path
                from django.utils import timezone
                
                uploaded_photos = form.cleaned_data.get("photos")
                if uploaded_photos:
                    self.cleanup_all_profile_drafts(profile.id)
                    
                    draft_token = uuid.uuid4().hex
                    photo_paths = []
                    for index, photo in enumerate(uploaded_photos):
                        relative_path = f"listing-preview-drafts/{profile.id}/{draft_token}/{index}_{photo.name}"
                        full_path = Path(settings.MEDIA_ROOT) / relative_path
                        full_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(full_path, "wb+") as destination:
                            for chunk in photo.chunks():
                                destination.write(chunk)
                        photo_paths.append(relative_path)
                else:
                    draft_token = previous_draft["token"]
                    photo_paths = previous_draft["photos"]

                draft_data = {
                    "token": draft_token,
                    "profile_id": profile.id,
                    "monthly_price_amount": form.cleaned_data["monthly_price_amount"],
                    "commune": form.cleaned_data["commune"],
                    "neighborhood": form.cleaned_data.get("neighborhood", ""),
                    "property_type": form.cleaned_data.get("property_type", Listing.PropertyType.APARTMENT),
                    "bedroom_count": form.cleaned_data["bedroom_count"],
                    "bathroom_count": form.cleaned_data.get("bathroom_count", 1),
                    "description": form.cleaned_data["description"],
                    "photos": photo_paths,
                    "timestamp": timezone.now().isoformat(),
                }
                request.session["listing_draft"] = draft_data
                
                photo_url = settings.MEDIA_URL + photo_paths[0]
                preview_listing = PreviewListing(
                    monthly_price_amount=draft_data["monthly_price_amount"],
                    commune=draft_data["commune"],
                    neighborhood=draft_data["neighborhood"],
                    property_type=draft_data["property_type"],
                    bedroom_count=draft_data["bedroom_count"],
                    bathroom_count=draft_data["bathroom_count"],
                    description=draft_data["description"],
                    photo_url=photo_url,
                )
                
                return render(
                    request,
                    self.template_name,
                    {
                        "state": "preview",
                        "listing": preview_listing,
                        "draft": draft_data,
                    },
                )
            else:
                return render(
                    request,
                    self.template_name,
                    {"form": form, "state": "entry", "draft": previous_draft},
                )

        elif action == "submit":
            if not previous_draft:
                form = ListingSubmissionForm(data={})
                form.is_valid()
                form.add_error(None, "Votre session de brouillon a expiré ou est invalide. Veuillez recommencer.")
                return render(
                    request,
                    self.template_name,
                    {"form": form, "state": "entry"},
                )

            form = ListingSubmissionForm(
                data={
                    "monthly_price_amount": previous_draft["monthly_price_amount"],
                    "commune": previous_draft["commune"],
                    "neighborhood": previous_draft.get("neighborhood", ""),
                    "property_type": previous_draft.get("property_type", Listing.PropertyType.APARTMENT),
                    "bedroom_count": previous_draft["bedroom_count"],
                    "bathroom_count": previous_draft.get("bathroom_count", 1),
                    "description": previous_draft["description"],
                },
                has_draft_photos=True,
            )
            if not previous_draft.get("photos") or len(previous_draft["photos"]) < 3:
                form.add_error(None, "Les photos du brouillon sont manquantes ou insuffisantes.")
                
            if form.is_valid() and not form.errors:
                from django.core.files import File
                from pathlib import Path
                
                opened_files = []
                success = False
                listing = None
                try:
                    django_files = []
                    for path in previous_draft["photos"]:
                        full_path = Path(settings.MEDIA_ROOT) / path
                        if not full_path.exists():
                            raise FileNotFoundError(f"Le fichier photo {full_path.name} est manquant.")
                        f = open(full_path, "rb")
                        opened_files.append(f)
                        django_files.append(File(f, name=Path(path).name))

                    listing = submit_listing_for_commissionnaire(
                        profile=profile,
                        listing_data=form.cleaned_data,
                        uploaded_photos=django_files,
                    )
                    success = True
                except Exception as e:
                    from django.core.exceptions import ValidationError as DjangoValidationError
                    if isinstance(e, DjangoValidationError):
                        if hasattr(e, "message_dict"):
                            for field, errors in e.message_dict.items():
                                for error in errors:
                                    form.add_error(field, error)
                        else:
                            form.add_error(None, e.message)
                    else:
                        form.add_error(None, f"Erreur lors de la soumission : {str(e)}")
                finally:
                    for f in opened_files:
                        f.close()

                if success and listing:
                    self.cleanup_draft_files(profile.id, previous_draft["token"])
                    request.session.pop("listing_draft", None)
                    return redirect("commissionnaires:listing_submitted", pk=listing.pk)
            return render(
                request,
                self.template_name,
                {"form": form, "state": "entry", "draft": previous_draft},
            )


class MockPhoto:
    def __init__(self, url):
        self._url = url
    @property
    def image(self):
        class ImageFieldMock:
            url = self._url
        return ImageFieldMock()


class PreviewListing:
    monthly_price_currency = "USD"
    is_verified = False
    view_count = 0

    def __init__(
        self,
        monthly_price_amount,
        commune,
        neighborhood,
        property_type,
        bedroom_count,
        bathroom_count,
        description,
        photo_url,
    ):
        self.monthly_price_amount = monthly_price_amount
        self.commune = commune
        self.neighborhood = neighborhood
        self.property_type = property_type
        self.bedroom_count = bedroom_count
        self.bathroom_count = bathroom_count
        self.description = description
        self.photo_url = photo_url

    @property
    def location_label(self):
        if self.neighborhood:
            return f"{self.neighborhood}, {self.commune}"
        return self.commune

    @property
    def property_type_label(self):
        return dict(Listing.PropertyType.choices).get(self.property_type, "Logement")

    @property
    def card_freshness_at(self):
        from django.utils import timezone
        return timezone.now()

    @property
    def card_photo_alt(self):
        return f"Aperçu non publié de l'annonce à {self.commune}"

    @property
    def card_primary_photo(self):
        return MockPhoto(self.photo_url)


class ListingSubmittedView(WhatsAppPhoneRequiredMixin, View):
    template_name = "commissionnaires/listing_submitted.html"

    def get(self, request, pk):
        profile = CommissionnaireProfile.objects.filter(user=request.user).first()
        if not profile:
            return render(
                request,
                "commissionnaires/permission_denied.html",
                {"profile_url": reverse("commissionnaires:profile")},
                status=404,
            )
        
        listing = Listing.objects.filter(pk=pk, commissionnaire_profile=profile).first()
        if not listing:
            return render(
                request,
                "commissionnaires/permission_denied.html",
                {"profile_url": reverse("commissionnaires:profile")},
                status=404,
            )

        return render(
            request,
            self.template_name,
            {"listing": listing},
        )


class ListingInventoryView(WhatsAppPhoneRequiredMixin, View):
    template_name = "commissionnaires/listing_inventory.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        from apps.accounts.selectors import user_has_whatsapp_phone
        from apps.accounts.decorators import redirect_to_phone_completion
        if not user_has_whatsapp_phone(request.user):
            return redirect_to_phone_completion(request, "accounts:phone_complete")

        profile = CommissionnaireProfile.objects.filter(user=request.user).first()
        if not profile:
            completion_url = reverse("commissionnaires:profile_create")
            return redirect(f"{completion_url}?{urlencode({'next': request.get_full_path()})}")

        if not profile.is_publication_eligible:
            completion_url = reverse("commissionnaires:profile_edit", kwargs={"pk": profile.pk})
            return redirect(f"{completion_url}?{urlencode({'next': request.get_full_path()})}")

        self.profile = profile
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        from apps.listings.selectors import get_commissionnaire_inventory, get_availability_freshness_state
        listings = get_commissionnaire_inventory(self.profile)
        
        for listing in listings:
            listing.freshness_state = get_availability_freshness_state(listing)
            listing.card_primary_photo = listing.get_primary_photo()
            listing.card_photo_alt = (
                listing.card_primary_photo.alt_text.strip()
                if listing.card_primary_photo and listing.card_primary_photo.alt_text.strip()
                else f"Logement a {listing.commune}"
            )

        return render(
            request,
            self.template_name,
            {
                "profile": self.profile,
                "listings": listings,
                "listing_count": len(listings),
                "lead_count": self.profile.leads.count(),
                "available_count": sum(
                    1 for listing in listings
                    if listing.availability_status == Listing.AvailabilityStatus.AVAILABLE
                ),
            },
        )


class ListingUpdateAvailabilityView(WhatsAppPhoneRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        from apps.accounts.selectors import user_has_whatsapp_phone
        from apps.accounts.decorators import redirect_to_phone_completion
        if not user_has_whatsapp_phone(request.user):
            return redirect_to_phone_completion(request, "accounts:phone_complete")

        profile = CommissionnaireProfile.objects.filter(user=request.user).first()
        if not profile:
            completion_url = reverse("commissionnaires:profile_create")
            return redirect(f"{completion_url}?{urlencode({'next': request.get_full_path()})}")

        if not profile.is_publication_eligible:
            completion_url = reverse("commissionnaires:profile_edit", kwargs={"pk": profile.pk})
            return redirect(f"{completion_url}?{urlencode({'next': request.get_full_path()})}")

        self.profile = profile
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, pk):
        from apps.listings.services import update_listing_availability
        from django.core.exceptions import PermissionDenied, ValidationError

        status = request.POST.get("availability_status")
        try:
            update_listing_availability(
                profile=self.profile,
                listing_id=pk,
                actor=request.user,
                new_status=status,
            )
        except (PermissionDenied, ValidationError) as e:
            raise e

        return redirect("commissionnaires:listing_inventory")


class ListingReconfirmAvailabilityView(WhatsAppPhoneRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        from apps.accounts.selectors import user_has_whatsapp_phone
        from apps.accounts.decorators import redirect_to_phone_completion
        if not user_has_whatsapp_phone(request.user):
            return redirect_to_phone_completion(request, "accounts:phone_complete")

        profile = CommissionnaireProfile.objects.filter(user=request.user).first()
        if not profile:
            completion_url = reverse("commissionnaires:profile_create")
            return redirect(f"{completion_url}?{urlencode({'next': request.get_full_path()})}")

        if not profile.is_publication_eligible:
            completion_url = reverse("commissionnaires:profile_edit", kwargs={"pk": profile.pk})
            return redirect(f"{completion_url}?{urlencode({'next': request.get_full_path()})}")

        self.profile = profile
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, pk):
        from apps.listings.services import reconfirm_listing_availability
        from django.core.exceptions import PermissionDenied, ValidationError

        try:
            reconfirm_listing_availability(
                profile=self.profile,
                listing_id=pk,
                actor=request.user,
            )
        except (PermissionDenied, ValidationError) as e:
            raise e

        return redirect("commissionnaires:listing_inventory")
