import shutil
import tempfile
from io import BytesIO
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from PIL import Image

from apps.commissionnaires.models import CommissionnaireProfile
from apps.listings.models import Listing, ListingPhoto


def make_image_upload(name="photo.jpg", image_format="JPEG", color="white"):
    image = Image.new("RGB", (16, 16), color=color)
    buffer = BytesIO()
    image.save(buffer, format=image_format)
    return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/jpeg")


class ListingPreviewViewTests(TestCase):
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

    def test_preview_renders_listing_card_successfully_and_does_not_create_listing(self):
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
            "description": "Superbe appartement à Gombe.",
            "photos": photos,
        }

        response = self.client.post(
            reverse("commissionnaires:listing_submit"),
            data=post_data,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vérifiez les informations avant l'envoi.")
        self.assertContains(response, "Gombe")
        self.assertContains(response, "1200")
        self.assertContains(response, "2 chambres")
        self.assertContains(response, "Superbe appartement à Gombe.")
        
        # Ensure no details page link is rendered in preview mode
        # Since we use div for preview, it should not have listings:detail link
        self.assertNotContains(response, "/annonces/0/")
        self.assertNotContains(response, "Verifiee")

        # Ensure no Listing was created in DB
        self.assertEqual(Listing.objects.count(), 0)

        # Check draft exists in session
        session = self.client.session
        self.assertIn("listing_draft", session)
        draft = session["listing_draft"]
        self.assertEqual(draft["monthly_price_amount"], 1200)
        self.assertEqual(len(draft["photos"]), 3)

    def test_preview_validation_errors_block_submission(self):
        post_data = {
            "action": "preview",
            "monthly_price_amount": "",
            "commune": "",
            "bedroom_count": 2,
            "description": "",
        }

        response = self.client.post(
            reverse("commissionnaires:listing_submit"),
            data=post_data,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ce champ est obligatoire.")
        self.assertEqual(Listing.objects.count(), 0)

    def test_edit_loads_draft_values_correctly(self):
        # Establish a valid draft in session
        session = self.client.session
        session["listing_draft"] = {
            "token": "testtoken",
            "profile_id": self.profile.id,
            "monthly_price_amount": 1500,
            "commune": "Ngaliema",
            "bedroom_count": 3,
            "description": "Jolie maison.",
            "photos": [
                "listing-preview-drafts/1/testtoken/0_p1.jpg",
                "listing-preview-drafts/1/testtoken/1_p2.jpg",
                "listing-preview-drafts/1/testtoken/2_p3.jpg",
            ],
            "timestamp": timezone.now().isoformat(),
        }
        session.save()

        # Request edit state
        response = self.client.post(
            reverse("commissionnaires:listing_submit"),
            data={"action": "edit"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1500")
        self.assertContains(response, "Ngaliema")
        self.assertContains(response, "3")
        self.assertContains(response, "Jolie maison.")
        self.assertContains(response, "Photos actuellement enregistrées en brouillon")

    def test_final_submit_creates_listing_and_cleans_draft(self):
        # Create temp files simulating draft uploads
        draft_token = "submittoken"
        temp_dir = Path(self.media_root) / "listing-preview-drafts" / str(self.profile.id) / draft_token
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        photo_paths = []
        for i in range(3):
            file_name = f"{i}_photo.jpg"
            img = Image.new("RGB", (16, 16), color="white")
            img.save(temp_dir / file_name, format="JPEG")
            photo_paths.append(f"listing-preview-drafts/{self.profile.id}/{draft_token}/{file_name}")

        # Set session draft
        session = self.client.session
        session["listing_draft"] = {
            "token": draft_token,
            "profile_id": self.profile.id,
            "monthly_price_amount": 950,
            "commune": "Kintambo",
            "bedroom_count": 1,
            "description": "Studio moderne tout équipé.",
            "photos": photo_paths,
            "timestamp": timezone.now().isoformat(),
        }
        session.save()

        # Submit final listing
        response = self.client.post(
            reverse("commissionnaires:listing_submit"),
            data={"action": "submit"},
        )

        # Verify database creation
        listing = Listing.objects.first()
        self.assertIsNotNone(listing)
        self.assertEqual(listing.monthly_price_amount, 950)
        self.assertEqual(listing.commune, "Kintambo")
        self.assertEqual(listing.bedroom_count, 1)
        self.assertEqual(listing.description, "Studio moderne tout équipé.")
        self.assertEqual(listing.availability_status, Listing.AvailabilityStatus.UNDER_REVIEW)
        self.assertEqual(listing.photos.count(), 3)
        self.assertTrue(listing.photos.first().is_primary)

        # Verify redirection to confirmation
        self.assertRedirects(
            response,
            reverse("commissionnaires:listing_submitted", args=[listing.pk]),
        )

        # Verify draft cleaned up from session and disk
        self.assertNotIn("listing_draft", self.client.session)
        self.assertFalse(temp_dir.exists())

    def test_final_submit_prevent_duplicate_creation(self):
        draft_token = "duptoken"
        temp_dir = Path(self.media_root) / "listing-preview-drafts" / str(self.profile.id) / draft_token
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        photo_paths = []
        for i in range(3):
            file_name = f"{i}_photo.jpg"
            img = Image.new("RGB", (16, 16), color="white")
            img.save(temp_dir / file_name, format="JPEG")
            photo_paths.append(f"listing-preview-drafts/{self.profile.id}/{draft_token}/{file_name}")

        session = self.client.session
        session["listing_draft"] = {
            "token": draft_token,
            "profile_id": self.profile.id,
            "monthly_price_amount": 1000,
            "commune": "Gombe",
            "bedroom_count": 2,
            "description": "Description.",
            "photos": photo_paths,
            "timestamp": timezone.now().isoformat(),
        }
        session.save()

        # Submit first time
        response1 = self.client.post(
            reverse("commissionnaires:listing_submit"),
            data={"action": "submit"},
        )
        self.assertEqual(Listing.objects.count(), 1)

        # Submit second time (simulating double click or back/refresh)
        response2 = self.client.post(
            reverse("commissionnaires:listing_submit"),
            data={"action": "submit"},
        )
        
        # Verify no second listing was created
        self.assertEqual(Listing.objects.count(), 1)
        self.assertContains(response2, "Votre session de brouillon a expiré ou est invalide")
