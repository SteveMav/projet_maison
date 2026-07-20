from django import forms
from django.utils.datastructures import MultiValueDict

from apps.listings.models import Listing
from apps.listings.validators import validate_listing_photo_upload


class ListingFilterForm(forms.Form):
    CITY_ALIASES = {"kinshasa", "ville de kinshasa"}

    commune = forms.CharField(
        label="Commune",
        required=False,
        strip=True,
    )
    budget_min = forms.IntegerField(
        label="Budget minimum",
        min_value=0,
        required=False,
    )
    budget_max = forms.IntegerField(
        label="Budget maximum",
        min_value=0,
        required=False,
    )
    bedrooms_min = forms.IntegerField(
        label="Chambres minimum",
        min_value=0,
        required=False,
    )

    def clean_commune(self):
        commune = self.cleaned_data["commune"].strip()
        if commune.lower() in self.CITY_ALIASES:
            return ""
        return commune

    def clean(self):
        cleaned_data = super().clean()
        budget_min = cleaned_data.get("budget_min")
        budget_max = cleaned_data.get("budget_max")
        if (
            budget_min is not None
            and budget_max is not None
            and budget_max < budget_min
        ):
            self.add_error(
                "budget_max",
                "Le budget maximum doit etre superieur ou egal au budget minimum.",
            )
        return cleaned_data


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def value_from_datadict(self, data, files, name):
        if isinstance(files, MultiValueDict):
            return files.getlist(name)
        return files.get(name)


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            if not data and self.required:
                raise forms.ValidationError("Ce champ est obligatoire.")
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class ListingSubmissionForm(forms.ModelForm):
    photos = MultipleFileField(
        label="Photos du logement",
        required=True,
        help_text="Ajoutez au moins 3 photos réelles du logement.",
        widget=MultipleFileInput(attrs={"class": "form-control", "accept": "image/jpeg,image/png,image/webp"}),
    )

    class Meta:
        model = Listing
        fields = [
            "monthly_price_amount",
            "commune",
            "neighborhood",
            "property_type",
            "bedroom_count",
            "bathroom_count",
            "description",
        ]
        labels = {
            "monthly_price_amount": "Prix mensuel en USD",
            "commune": "Commune",
            "neighborhood": "Quartier",
            "property_type": "Type de bien",
            "bedroom_count": "Nombre de chambres",
            "bathroom_count": "Salles d'eau",
            "description": "Description",
        }
        widgets = {
            "monthly_price_amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: 450",
                    "min": "1",
                }
            ),
            "commune": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: Gombe, Ngaliema...",
                }
            ),
            "neighborhood": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: Ma Campagne, Socimat...",
                }
            ),
            "property_type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "bedroom_count": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: 2",
                    "min": "0",
                }
            ),
            "bathroom_count": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: 1",
                    "min": "0",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Décrivez le logement en quelques phrases...",
                    "rows": 4,
                }
            ),
        }

    def __init__(self, *args, has_draft_photos=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["property_type"].required = False
        self.fields["property_type"].initial = Listing.PropertyType.APARTMENT
        self.fields["bathroom_count"].required = False
        self.fields["bathroom_count"].initial = 1
        if has_draft_photos:
            self.fields["photos"].required = False

    def clean_monthly_price_amount(self):
        price = self.cleaned_data.get("monthly_price_amount")
        if price is None or price <= 0:
            raise forms.ValidationError("Le prix mensuel doit être supérieur à 0.")
        return price

    def clean_commune(self):
        commune = self.cleaned_data.get("commune", "").strip()
        if not commune:
            raise forms.ValidationError("Ce champ est obligatoire.")
        return commune

    def clean_neighborhood(self):
        return self.cleaned_data.get("neighborhood", "").strip()

    def clean_property_type(self):
        return self.cleaned_data.get("property_type") or Listing.PropertyType.APARTMENT

    def clean_bathroom_count(self):
        count = self.cleaned_data.get("bathroom_count")
        if count is None:
            return 1
        return count

    def clean_description(self):
        description = self.cleaned_data.get("description", "").strip()
        if not description:
            raise forms.ValidationError("Ce champ est obligatoire.")
        return description

    def clean_photos(self):
        photos = self.cleaned_data.get("photos")
        if not photos:
            if self.fields["photos"].required:
                raise forms.ValidationError("Vous devez fournir au moins 3 photos.")
            return None
        if len(photos) < 3:
            raise forms.ValidationError("Vous devez fournir au moins 3 photos.")
        for photo in photos:
            try:
                validate_listing_photo_upload(photo)
            except forms.ValidationError as e:
                raise forms.ValidationError(e.message)
        return photos


class ListingAvailabilityForm(forms.Form):
    availability_status = forms.ChoiceField(
        choices=[
            (Listing.AvailabilityStatus.AVAILABLE, "Disponible"),
            (Listing.AvailabilityStatus.UNAVAILABLE, "Non disponible"),
        ],
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Statut de disponibilite",
    )
