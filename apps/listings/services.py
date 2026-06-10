from dataclasses import dataclass

from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Max
from django.db import transaction
from django.utils import timezone

from apps.commissionnaires.models import CommissionnaireProfile
from apps.listings.selectors import get_listing_for_commissionnaire
from apps.listings.validators import validate_listing_photo_upload
from apps.listings.models import Listing
from apps.listings.models import ListingPhoto


@dataclass(frozen=True)
class PublicationReadiness:
    is_ready: bool
    missing_requirements: tuple[str, ...]


def create_listing(
    *,
    commissionnaire_profile,
    monthly_price_amount,
    commune,
    bedroom_count,
    description,
    availability_status=Listing.AvailabilityStatus.UNDER_REVIEW,
    submitted_at=None,
):
    if not isinstance(commissionnaire_profile, CommissionnaireProfile):
        raise TypeError("commissionnaire_profile must be a CommissionnaireProfile.")

    now = submitted_at or timezone.now()
    listing = Listing(
        commissionnaire_profile=commissionnaire_profile,
        monthly_price_amount=monthly_price_amount,
        commune=commune,
        bedroom_count=bedroom_count,
        description=description,
        availability_status=availability_status,
        submitted_at=now,
        availability_changed_at=now,
        availability_reconfirmed_at=now,
    )
    listing.full_clean()
    listing.save()
    return listing


def _next_photo_position(listing):
    current_max = listing.photos.aggregate(max_position=Max("position"))["max_position"]
    if current_max is None:
        return 0
    return current_max + 1


def add_listing_photo(
    listing,
    uploaded_file,
    position=None,
    is_primary=False,
    alt_text="",
):
    if not isinstance(listing, Listing):
        raise TypeError("listing must be a Listing.")

    validate_listing_photo_upload(uploaded_file)
    should_be_primary = is_primary or not listing.photos.filter(is_primary=True).exists()
    photo = ListingPhoto(
        listing=listing,
        image=uploaded_file,
        position=_next_photo_position(listing) if position is None else position,
        is_primary=False,
        alt_text=alt_text,
    )
    photo.full_clean()
    photo.save()

    if should_be_primary:
        set_primary_photo(photo)
        photo.refresh_from_db()

    return photo


def add_listing_photo_for_profile(
    *,
    commissionnaire_profile,
    listing_id,
    uploaded_file,
    position=None,
    is_primary=False,
    alt_text="",
):
    try:
        listing = get_listing_for_commissionnaire(commissionnaire_profile, listing_id)
    except Listing.DoesNotExist as error:
        raise PermissionDenied("Ce listing n'appartient pas a ce commissionnaire.") from error

    return add_listing_photo(
        listing,
        uploaded_file,
        position=position,
        is_primary=is_primary,
        alt_text=alt_text,
    )


def set_primary_photo(photo):
    if not photo.pk:
        raise ValueError("A saved ListingPhoto is required.")

    with transaction.atomic():
        ListingPhoto.objects.select_for_update().filter(
            listing_id=photo.listing_id,
            is_primary=True,
        ).exclude(pk=photo.pk).update(is_primary=False)
        photo.is_primary = True
        photo.save(update_fields=["is_primary", "updated_at"])

    return photo


def get_publication_readiness(listing):
    if not isinstance(listing, Listing):
        raise TypeError("listing must be a Listing.")

    missing = []
    required_values = {
        "commissionnaire_profile": listing.commissionnaire_profile_id,
        "monthly_price_amount": listing.monthly_price_amount,
        "commune": listing.commune.strip(),
        "bedroom_count": listing.bedroom_count,
        "description": listing.description.strip(),
        "submitted_at": listing.submitted_at,
    }
    for field_name, value in required_values.items():
        if value in {None, ""}:
            missing.append(field_name)

    if listing.availability_status not in Listing.AvailabilityStatus.values:
        missing.append("availability_status")

    if listing.photos.count() < 3:
        missing.append("minimum_photos")

    return PublicationReadiness(
        is_ready=not missing,
        missing_requirements=tuple(missing),
    )


@transaction.atomic
def submit_listing_for_commissionnaire(*, profile, listing_data, uploaded_photos):
    if not isinstance(profile, CommissionnaireProfile):
        raise TypeError("profile must be a CommissionnaireProfile.")

    if not profile.is_publication_eligible:
        raise ValidationError("Le profil commissionnaire n'est pas eligible pour publier.")

    if not uploaded_photos or len(uploaded_photos) < 3:
        raise ValidationError("Vous devez fournir au moins 3 photos.")

    # Validate all photo files first
    for photo in uploaded_photos:
        validate_listing_photo_upload(photo)

    created_photos = []
    try:
        # Create Listing
        listing = create_listing(
            commissionnaire_profile=profile,
            monthly_price_amount=listing_data.get("monthly_price_amount"),
            commune=listing_data.get("commune"),
            bedroom_count=listing_data.get("bedroom_count"),
            description=listing_data.get("description"),
            availability_status=Listing.AvailabilityStatus.UNDER_REVIEW,
        )

        for index, photo_file in enumerate(uploaded_photos):
            is_primary = (index == 0)
            photo = add_listing_photo(
                listing=listing,
                uploaded_file=photo_file,
                position=index,
                is_primary=is_primary,
            )
            created_photos.append(photo)

        # Double check publication readiness to ensure everything is valid
        readiness = get_publication_readiness(listing)
        if not readiness.is_ready:
            missing_fields = ", ".join(readiness.missing_requirements)
            raise ValidationError(
                f"Le listing n'est pas pret pour publication. Manquant: {missing_fields}"
            )

        return listing

    except Exception as e:
        # Clean up any files saved on disk in case of database rollback
        for photo in created_photos:
            if photo.image:
                try:
                    photo.image.storage.delete(photo.image.name)
                except Exception:
                    pass
        raise e


@transaction.atomic
def update_listing_availability(profile, listing_id, actor, new_status):
    if new_status not in [Listing.AvailabilityStatus.AVAILABLE, Listing.AvailabilityStatus.UNAVAILABLE]:
        raise ValidationError("Statut de disponibilite invalide.")

    try:
        listing = Listing.objects.select_for_update().get(
            pk=listing_id,
            commissionnaire_profile=profile,
        )
    except Listing.DoesNotExist as error:
        raise PermissionDenied("Ce listing n'appartient pas a ce commissionnaire.") from error

    old_status = listing.availability_status
    if old_status == new_status:
        return listing

    now = timezone.now()
    listing.availability_status = new_status
    listing.availability_changed_at = now
    if new_status == Listing.AvailabilityStatus.AVAILABLE:
        listing.availability_reconfirmed_at = now

    listing.save(update_fields=["availability_status", "availability_changed_at", "availability_reconfirmed_at", "updated_at"])

    from apps.audit.services import create_audit_event
    create_audit_event(
        event_type="listing.availability_changed",
        actor=actor,
        target_id=listing.id,
        metadata={
            "listing_id": listing.id,
            "commissionnaire_profile_id": profile.id,
            "previous_status": old_status,
            "new_status": new_status,
            "availability_changed_at": now.isoformat(),
        }
    )
    return listing


@transaction.atomic
def reconfirm_listing_availability(profile, listing_id, actor):
    try:
        listing = Listing.objects.select_for_update().get(
            pk=listing_id,
            commissionnaire_profile=profile,
        )
    except Listing.DoesNotExist as error:
        raise PermissionDenied("Ce listing n'appartient pas a ce commissionnaire.") from error

    if listing.availability_status != Listing.AvailabilityStatus.AVAILABLE:
        raise ValidationError("Seuls les listings disponibles peuvent etre reconfirmes.")

    now = timezone.now()
    listing.availability_reconfirmed_at = now
    listing.save(update_fields=["availability_reconfirmed_at", "updated_at"])

    from apps.audit.services import create_audit_event
    create_audit_event(
        event_type="listing.availability_reconfirmed",
        actor=actor,
        target_id=listing.id,
        metadata={
            "listing_id": listing.id,
            "commissionnaire_profile_id": profile.id,
            "availability_reconfirmed_at": now.isoformat(),
        }
    )
    return listing
