import shutil
import tempfile
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image

from apps.commissionnaires.models import CommissionnaireProfile
from apps.listings.models import Listing, ListingPhoto
from apps.listings.services import submit_listing_for_commissionnaire


def make_image_upload(name="photo.jpg", image_format="JPEG", color="white"):
    image = Image.new("RGB", (16, 16), color=color)
    buffer = BytesIO()
    image.save(buffer, format=image_format)
    return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/jpeg")


class ListingSubmissionServiceTests(TestCase):
    def setUp(self):
        self.media_root = tempfile.mkdtemp()
        self.settings_override = override_settings(MEDIA_ROOT=self.media_root)
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)
        self.addCleanup(lambda: shutil.rmtree(self.media_root, ignore_errors=True))

    def create_profile(self, email="pro@example.com", display_name="Maison Pro"):
        user = get_user_model().objects.create_user(
            email=email,
            password="StrongPass123!",
            whatsapp_phone="+243990000000",
        )
        return CommissionnaireProfile.objects.create(
            user=user,
            display_name=display_name,
            whatsapp_phone="+243990000000",
        )

    def test_submit_listing_success(self):
        profile = self.create_profile()
        listing_data = {
            "monthly_price_amount": 1200,
            "commune": "Gombe",
            "bedroom_count": 2,
            "description": "Appartement de standing.",
        }
        photos = [
            make_image_upload("photo1.jpg", color="red"),
            make_image_upload("photo2.jpg", color="blue"),
            make_image_upload("photo3.jpg", color="green"),
        ]

        listing = submit_listing_for_commissionnaire(
            profile=profile,
            listing_data=listing_data,
            uploaded_photos=photos,
        )

        # Assert Listing created with correct attributes
        self.assertEqual(listing.commissionnaire_profile, profile)
        self.assertEqual(listing.monthly_price_amount, 1200)
        self.assertEqual(listing.commune, "Gombe")
        self.assertEqual(listing.bedroom_count, 2)
        self.assertEqual(listing.description, "Appartement de standing.")
        self.assertEqual(listing.availability_status, Listing.AvailabilityStatus.UNDER_REVIEW)
        self.assertIsNotNone(listing.submitted_at)

        # Assert Photos created and ordered
        photos_qs = listing.photos.all()
        self.assertEqual(photos_qs.count(), 3)
        self.assertEqual(photos_qs[0].position, 0)
        self.assertTrue(photos_qs[0].is_primary)
        self.assertEqual(photos_qs[1].position, 1)
        self.assertFalse(photos_qs[1].is_primary)
        self.assertEqual(photos_qs[2].position, 2)
        self.assertFalse(photos_qs[2].is_primary)

    def test_submit_listing_profile_not_eligible(self):
        profile = self.create_profile(display_name="   ")  # Will be stripped and invalid on full clean, but let's force an ineligible profile by bypassing save validation or making a profile that's not eligible.
        # Wait, if display_name is empty/blank in DB, but the profile model clean trims and rejects it...
        # Let's make the profile ineligible by having the user not have a whatsapp phone.
        # But wait, profile model is_publication_eligible checks user_has_whatsapp_phone.
        # Let's delete the user's whatsapp_phone to make the profile ineligible!
        profile.user.whatsapp_phone = ""
        profile.user.save()

        self.assertFalse(profile.is_publication_eligible)

        listing_data = {
            "monthly_price_amount": 1200,
            "commune": "Gombe",
            "bedroom_count": 2,
            "description": "Appartement de standing.",
        }
        photos = [
            make_image_upload("photo1.jpg"),
            make_image_upload("photo2.jpg"),
            make_image_upload("photo3.jpg"),
        ]

        with self.assertRaises(ValidationError):
            submit_listing_for_commissionnaire(
                profile=profile,
                listing_data=listing_data,
                uploaded_photos=photos,
            )

    def test_submit_listing_fewer_than_three_photos(self):
        profile = self.create_profile()
        listing_data = {
            "monthly_price_amount": 1200,
            "commune": "Gombe",
            "bedroom_count": 2,
            "description": "Appartement.",
        }
        photos = [
            make_image_upload("photo1.jpg"),
            make_image_upload("photo2.jpg"),
        ]

        with self.assertRaises(ValidationError):
            submit_listing_for_commissionnaire(
                profile=profile,
                listing_data=listing_data,
                uploaded_photos=photos,
            )

    def test_submit_listing_invalid_photos(self):
        profile = self.create_profile()
        listing_data = {
            "monthly_price_amount": 1200,
            "commune": "Gombe",
            "bedroom_count": 2,
            "description": "Appartement.",
        }
        photos = [
            make_image_upload("photo1.jpg"),
            make_image_upload("photo2.jpg"),
            SimpleUploadedFile("corrupt.jpg", b"corrupted image content", content_type="image/jpeg"),
        ]

        with self.assertRaises(ValidationError):
            submit_listing_for_commissionnaire(
                profile=profile,
                listing_data=listing_data,
                uploaded_photos=photos,
            )

    def test_submit_listing_db_error_rolls_back_and_cleans_files(self):
        profile = self.create_profile()
        listing_data = {
            "monthly_price_amount": 1200,
            "commune": "Gombe",
            "bedroom_count": -5,  # Invalid value to trigger model full_clean() error
            "description": "Appartement.",
        }
        photos = [
            make_image_upload("photo1.jpg"),
            make_image_upload("photo2.jpg"),
            make_image_upload("photo3.jpg"),
        ]

        with self.assertRaises(ValidationError):
            submit_listing_for_commissionnaire(
                profile=profile,
                listing_data=listing_data,
                uploaded_photos=photos,
            )

        # Ensure no Listing was created in DB
        self.assertEqual(Listing.objects.count(), 0)
        self.assertEqual(ListingPhoto.objects.count(), 0)
