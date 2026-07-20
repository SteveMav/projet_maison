from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.commissionnaires.models import CommissionnaireProfile
from apps.listings.models import Listing
from apps.listings.services import add_listing_photo, create_listing


DEMO_EMAIL = "demo.maison+commissionnaire@example.com"
DEMO_PHONE = "+243990123456"


DEMO_LISTINGS = [
    {
        "monthly_price_amount": 420,
        "commune": "Ngaliema",
        "neighborhood": "Ma Campagne",
        "property_type": Listing.PropertyType.APARTMENT,
        "bedroom_count": 2,
        "bathroom_count": 1,
        "view_count": 38,
        "is_verified": True,
        "description": "Appartement lumineux avec séjour traversant, cuisine séparée et accès rapide vers Ma Campagne.",
    },
    {
        "monthly_price_amount": 650,
        "commune": "Gombe",
        "neighborhood": "Socimat",
        "property_type": Listing.PropertyType.APARTMENT,
        "bedroom_count": 3,
        "bathroom_count": 2,
        "view_count": 64,
        "is_verified": False,
        "description": "Logement familial proche des commerces, avec balcon, parking partagé et disponibilité à reconfirmer avant visite.",
    },
    {
        "monthly_price_amount": 280,
        "commune": "Kintambo",
        "neighborhood": "Magasin",
        "property_type": Listing.PropertyType.STUDIO,
        "bedroom_count": 1,
        "bathroom_count": 1,
        "view_count": 22,
        "is_verified": True,
        "description": "Studio pratique pour une personne ou un couple, avec pièce principale claire et accès simple aux transports.",
    },
    {
        "monthly_price_amount": 900,
        "commune": "Limete",
        "neighborhood": "7e Rue",
        "property_type": Listing.PropertyType.HOUSE,
        "bedroom_count": 4,
        "bathroom_count": 2,
        "view_count": 71,
        "is_verified": False,
        "description": "Maison avec cour, chambres séparées et espace extérieur utile pour une famille cherchant plus de calme.",
    },
]


class Command(BaseCommand):
    help = "Seed a local Maison demo catalogue with realistic listings and photos."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete the existing Maison demo listings before recreating them.",
        )

    def handle(self, *args, **options):
        source_images = [
            settings.BASE_DIR
            / "design"
            / "stitch-imports"
            / "detail-ngaliema"
            / f"property-0{index}.jpg"
            for index in range(1, 5)
        ]
        missing = [str(path) for path in source_images if not path.exists()]
        if missing:
            raise CommandError("Demo source images are missing: " + ", ".join(missing))

        with transaction.atomic():
            if options["reset"]:
                self._delete_demo_data()
            profile = self._get_or_create_profile()
            created_count = self._upsert_listings(profile, source_images)

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo catalogue ready: {created_count} listings for {profile.display_name}."
            )
        )

    def _get_or_create_profile(self):
        User = get_user_model()
        user, created = User.objects.get_or_create(
            email=DEMO_EMAIL,
            defaults={
                "whatsapp_phone": DEMO_PHONE,
                "whatsapp_consent": True,
                "whatsapp_consent_given_at": timezone.now(),
            },
        )
        if created or not user.password or not user.has_usable_password():
            user.set_unusable_password()
        user.whatsapp_phone = DEMO_PHONE
        user.whatsapp_consent = True
        user.whatsapp_consent_given_at = user.whatsapp_consent_given_at or timezone.now()
        user.save()

        profile, _created = CommissionnaireProfile.objects.get_or_create(
            user=user,
            defaults={
                "display_name": "Maison Démo Kin",
                "whatsapp_phone": DEMO_PHONE,
            },
        )
        profile.display_name = "Maison Démo Kin"
        profile.whatsapp_phone = DEMO_PHONE
        profile.save()
        return profile

    def _delete_demo_data(self):
        User = get_user_model()
        try:
            profile = CommissionnaireProfile.objects.get(user__email=DEMO_EMAIL)
        except CommissionnaireProfile.DoesNotExist:
            profile = None

        if profile is not None:
            for listing in Listing.objects.filter(commissionnaire_profile=profile):
                self._delete_listing_photos(listing)
                listing.delete()
            profile.delete()

        User.objects.filter(email=DEMO_EMAIL).delete()

    def _upsert_listings(self, profile, source_images):
        now = timezone.now()
        count = 0
        for index, spec in enumerate(DEMO_LISTINGS):
            listing = (
                Listing.objects.filter(
                    commissionnaire_profile=profile,
                    commune=spec["commune"],
                    neighborhood=spec["neighborhood"],
                )
                .order_by("id")
                .first()
            )
            if listing is None:
                listing = create_listing(
                    commissionnaire_profile=profile,
                    monthly_price_amount=spec["monthly_price_amount"],
                    commune=spec["commune"],
                    neighborhood=spec["neighborhood"],
                    property_type=spec["property_type"],
                    bedroom_count=spec["bedroom_count"],
                    bathroom_count=spec["bathroom_count"],
                    view_count=spec["view_count"],
                    is_verified=spec["is_verified"],
                    verification_checked_at=now if spec["is_verified"] else None,
                    description=spec["description"],
                    availability_status=Listing.AvailabilityStatus.AVAILABLE,
                    submitted_at=now - timedelta(days=index + 1),
                )
            else:
                for field, value in spec.items():
                    setattr(listing, field, value)
                listing.availability_status = Listing.AvailabilityStatus.AVAILABLE
                listing.verification_checked_at = now if spec["is_verified"] else None
                listing.availability_changed_at = now - timedelta(days=index + 1)
                listing.availability_reconfirmed_at = now - timedelta(days=index)
                listing.full_clean()
                listing.save()

            self._delete_listing_photos(listing)
            for position in range(3):
                source = source_images[(index + position) % len(source_images)]
                with source.open("rb") as handle:
                    add_listing_photo(
                        listing=listing,
                        uploaded_file=File(handle, name=f"{spec['commune'].lower()}-{position + 1}.jpg"),
                        position=position,
                        is_primary=position == 0,
                        alt_text=f"Photo du logement à {spec['neighborhood']}, {spec['commune']}",
                    )
            count += 1
        return count

    def _delete_listing_photos(self, listing):
        for photo in listing.photos.all():
            if photo.image:
                photo.image.delete(save=False)
            photo.delete()
