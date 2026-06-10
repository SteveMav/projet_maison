import shutil
import tempfile
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from apps.commissionnaires.models import CommissionnaireProfile
from apps.listings.models import Listing


def make_image_upload(name="photo.jpg", image_format="JPEG", color="white"):
    image = Image.new("RGB", (16, 16), color=color)
    buffer = BytesIO()
    image.save(buffer, format=image_format)
    return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/jpeg")


class ListingSubmissionViewTests(TestCase):
    def setUp(self):
        self.media_root = tempfile.mkdtemp()
        self.settings_override = override_settings(MEDIA_ROOT=self.media_root)
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)
        self.addCleanup(lambda: shutil.rmtree(self.media_root, ignore_errors=True))

        # Setup user and eligible profile
        self.user = get_user_model().objects.create_user(
            email="commissionnaire@example.com",
            password="StrongPass123!",
            whatsapp_phone="+243990000000",
        )
        self.profile = CommissionnaireProfile.objects.create(
            user=self.user,
            display_name="Maison Pro",
            whatsapp_phone="+243990000000",
        )
        self.client.force_login(self.user)

    def test_get_submission_form_rendering(self):
        response = self.client.get(reverse("commissionnaires:listing_submit"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Publier un bien")
        self.assertContains(response, "Prix mensuel en USD")
        self.assertContains(response, "Commune")
        self.assertContains(response, "Nombre de chambres")
        self.assertContains(response, "Description")
        self.assertContains(response, "Photos du logement")

    def test_post_submission_success(self):
        photos = [
            make_image_upload("photo1.jpg"),
            make_image_upload("photo2.jpg"),
            make_image_upload("photo3.jpg"),
        ]
        post_data = {
            "action": "preview",
            "monthly_price_amount": 1200,
            "commune": "Gombe",
            "bedroom_count": 2,
            "description": "Superbe appartement rénové avec goût.",
            "photos": photos,
        }

        # Step 1: Preview
        response = self.client.post(
            reverse("commissionnaires:listing_submit"),
            data=post_data,
        )
        self.assertEqual(response.status_code, 200)

        # Step 2: Final submit
        response = self.client.post(
            reverse("commissionnaires:listing_submit"),
            data={"action": "submit"},
        )

        listing = Listing.objects.first()
        self.assertIsNotNone(listing)
        self.assertRedirects(
            response,
            reverse("commissionnaires:listing_submitted", args=[listing.pk]),
        )

    def test_post_submission_validation_errors_missing_fields(self):
        post_data = {
            "action": "preview",
            "monthly_price_amount": "",
            "commune": "   ",
            "bedroom_count": 2,
            "description": "",
            # no photos
        }

        response = self.client.post(
            reverse("commissionnaires:listing_submit"),
            data=post_data,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ce champ est obligatoire.")
        self.assertEqual(Listing.objects.count(), 0)

    def test_post_submission_validation_errors_fewer_than_three_photos(self):
        photos = [
            make_image_upload("photo1.jpg"),
            make_image_upload("photo2.jpg"),
        ]
        post_data = {
            "action": "preview",
            "monthly_price_amount": 1200,
            "commune": "Gombe",
            "bedroom_count": 2,
            "description": "Superbe appartement.",
            "photos": photos,
        }

        response = self.client.post(
            reverse("commissionnaires:listing_submit"),
            data=post_data,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vous devez fournir au moins 3 photos.")
        self.assertEqual(Listing.objects.count(), 0)

    def test_post_submission_preserves_values_on_error(self):
        photos = [
            make_image_upload("photo1.jpg"),
        ]
        post_data = {
            "action": "preview",
            "monthly_price_amount": 1500,
            "commune": "Ngaliema",
            "bedroom_count": 3,
            "description": "Preserve me!",
            "photos": photos,
        }

        response = self.client.post(
            reverse("commissionnaires:listing_submit"),
            data=post_data,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1500")
        self.assertContains(response, "Ngaliema")
        self.assertContains(response, "3")
        self.assertContains(response, "Preserve me!")

    def test_submitted_confirmation_page_rendering(self):
        listing = Listing.objects.create(
            commissionnaire_profile=self.profile,
            monthly_price_amount=800,
            commune="Kintambo",
            bedroom_count=1,
            description="Studio moderne.",
        )

        response = self.client.get(reverse("commissionnaires:listing_submitted", args=[listing.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Envoyée pour modération")
        self.assertContains(response, "Kintambo")
        self.assertContains(response, "800")
        # Ensure no verification badges or trust seals are rendered
        self.assertNotContains(response, "Vérifié")
        self.assertNotContains(response, "badge")
