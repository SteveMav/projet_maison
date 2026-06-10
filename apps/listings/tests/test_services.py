import shutil
import tempfile
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image

from apps.commissionnaires.models import CommissionnaireProfile
from apps.listings.models import Listing, ListingPhoto
from apps.listings.selectors import get_listing_for_commissionnaire, get_listing_primary_photo
from apps.listings.services import (
    add_listing_photo,
    add_listing_photo_for_profile,
    create_listing,
    get_publication_readiness,
    set_primary_photo,
)


def make_image_upload(name="photo.jpg", image_format="JPEG", color="white"):
    image = Image.new("RGB", (16, 16), color=color)
    buffer = BytesIO()
    image.save(buffer, format=image_format)
    return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/jpeg")


class ListingServiceTests(TestCase):
    def setUp(self):
        self.media_root = tempfile.mkdtemp()
        self.settings_override = override_settings(MEDIA_ROOT=self.media_root)
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)
        self.addCleanup(lambda: shutil.rmtree(self.media_root, ignore_errors=True))

    def create_profile(self, email="pro@example.com"):
        user = get_user_model().objects.create_user(
            email=email,
            password="StrongPass123!",
            whatsapp_phone="+243990000000",
        )
        return CommissionnaireProfile.objects.create(
            user=user,
            display_name="Maison Pro",
            whatsapp_phone="+243990000000",
        )

    def create_listing(self, profile=None, **overrides):
        return create_listing(
            commissionnaire_profile=profile or self.create_profile(),
            monthly_price_amount=1200,
            commune="Gombe",
            bedroom_count=2,
            description="Appartement lumineux proche des services.",
            **overrides,
        )

    def test_create_listing_requires_commissionnaire_profile_not_raw_user(self):
        profile = self.create_profile()

        listing = self.create_listing(profile)

        self.assertEqual(listing.commissionnaire_profile, profile)
        self.assertEqual(listing.monthly_price_amount, 1200)
        self.assertEqual(listing.monthly_price_currency, Listing.Currency.USD)
        self.assertEqual(
            listing.availability_status,
            Listing.AvailabilityStatus.UNDER_REVIEW,
        )
        self.assertIsNotNone(listing.submitted_at)

        with self.assertRaises(TypeError):
            create_listing(
                commissionnaire_profile=profile.user,
                monthly_price_amount=1200,
                commune="Gombe",
                bedroom_count=2,
                description="Appartement lumineux proche des services.",
            )

    def test_add_listing_photo_validates_upload_and_saves_under_listing_media_path(self):
        listing = self.create_listing()

        photo = add_listing_photo(listing, make_image_upload("room.jpg"))

        self.assertEqual(photo.listing, listing)
        self.assertTrue(photo.image.name.startswith(f"listings/{listing.pk}/"))
        self.assertEqual(photo.position, 0)
        self.assertTrue(photo.is_primary)
        self.assertTrue(ListingPhoto.objects.filter(pk=photo.pk).exists())

    def test_add_listing_photo_rejects_invalid_image_before_save(self):
        listing = self.create_listing()
        invalid_upload = SimpleUploadedFile("bad.jpg", b"not an image")

        with self.assertRaises(ValidationError):
            add_listing_photo(listing, invalid_upload)

        self.assertEqual(ListingPhoto.objects.count(), 0)

    def test_photo_ordering_and_primary_fallback_are_deterministic(self):
        listing = self.create_listing()
        first = add_listing_photo(listing, make_image_upload("first.jpg"), position=2)
        second = add_listing_photo(listing, make_image_upload("second.jpg"), position=1)

        self.assertEqual(list(ListingPhoto.objects.values_list("pk", flat=True)), [second.pk, first.pk])
        self.assertEqual(get_listing_primary_photo(listing), first)

        first.is_primary = False
        first.save(update_fields=["is_primary"])

        self.assertEqual(get_listing_primary_photo(listing), second)

    def test_set_primary_photo_clears_previous_primary_for_same_listing(self):
        listing = self.create_listing()
        first = add_listing_photo(listing, make_image_upload("first.jpg"), position=0)
        second = add_listing_photo(listing, make_image_upload("second.jpg"), position=1)

        set_primary_photo(second)
        first.refresh_from_db()
        second.refresh_from_db()

        self.assertFalse(first.is_primary)
        self.assertTrue(second.is_primary)
        self.assertEqual(
            ListingPhoto.objects.filter(listing=listing, is_primary=True).count(),
            1,
        )

    def test_profile_scoped_photo_mutation_rejects_forged_listing_ids(self):
        owner_profile = self.create_profile("owner@example.com")
        other_profile = self.create_profile("other@example.com")
        listing = self.create_listing(owner_profile)

        with self.assertRaises(PermissionDenied):
            add_listing_photo_for_profile(
                commissionnaire_profile=other_profile,
                listing_id=listing.pk,
                uploaded_file=make_image_upload("intrusion.jpg"),
            )

        self.assertEqual(ListingPhoto.objects.count(), 0)

    def test_selector_returns_only_listing_owned_by_profile(self):
        owner_profile = self.create_profile("owner@example.com")
        other_profile = self.create_profile("other@example.com")
        listing = self.create_listing(owner_profile)

        self.assertEqual(get_listing_for_commissionnaire(owner_profile, listing.pk), listing)

        with self.assertRaises(Listing.DoesNotExist):
            get_listing_for_commissionnaire(other_profile, listing.pk)

    def test_publication_readiness_requires_required_fields_and_three_photos(self):
        listing = self.create_listing()

        not_ready = get_publication_readiness(listing)
        self.assertFalse(not_ready.is_ready)
        self.assertIn("minimum_photos", not_ready.missing_requirements)

        for index in range(3):
            add_listing_photo(
                listing,
                make_image_upload(f"photo-{index}.jpg", color=(index * 20, 0, 0)),
                position=index,
            )

        ready = get_publication_readiness(listing)
        self.assertTrue(ready.is_ready)
        self.assertEqual(ready.missing_requirements, ())
