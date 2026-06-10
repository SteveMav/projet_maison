from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from PIL import Image

from apps.listings.validators import (
    ALLOWED_LISTING_IMAGE_EXTENSIONS,
    ALLOWED_LISTING_IMAGE_FORMATS,
    MAX_LISTING_PHOTO_BYTES,
    validate_listing_photo_upload,
)


def make_image_upload(name="photo.jpg", image_format="JPEG"):
    image = Image.new("RGB", (16, 16), color="white")
    buffer = BytesIO()
    image.save(buffer, format=image_format)
    return SimpleUploadedFile(
        name,
        buffer.getvalue(),
        content_type="application/octet-stream",
    )


class ListingPhotoValidatorTests(SimpleTestCase):
    def test_validation_constants_allow_only_mobile_property_photo_formats(self):
        self.assertEqual(
            ALLOWED_LISTING_IMAGE_EXTENSIONS,
            {".jpg", ".jpeg", ".png", ".webp"},
        )
        self.assertEqual(
            ALLOWED_LISTING_IMAGE_FORMATS,
            {"JPEG", "PNG", "WEBP"},
        )
        self.assertGreater(MAX_LISTING_PHOTO_BYTES, 0)

    def test_valid_jpeg_png_and_webp_uploads_are_accepted(self):
        cases = [
            ("living-room.jpg", "JPEG"),
            ("kitchen.png", "PNG"),
            ("balcony.webp", "WEBP"),
        ]

        for filename, image_format in cases:
            with self.subTest(filename=filename):
                upload = make_image_upload(filename, image_format)

                self.assertIs(validate_listing_photo_upload(upload), upload)
                self.assertEqual(upload.tell(), 0)

    def test_rejects_unsupported_extensions_even_when_content_is_image(self):
        upload = make_image_upload("photo.gif", "PNG")

        with self.assertRaises(ValidationError) as error:
            validate_listing_photo_upload(upload)

        self.assertEqual(error.exception.code, "invalid_extension")

    def test_rejects_empty_files(self):
        upload = SimpleUploadedFile("empty.jpg", b"", content_type="image/jpeg")

        with self.assertRaises(ValidationError) as error:
            validate_listing_photo_upload(upload)

        self.assertEqual(error.exception.code, "empty")

    def test_rejects_corrupt_images(self):
        upload = SimpleUploadedFile(
            "corrupt.jpg",
            b"not real image bytes",
            content_type="image/jpeg",
        )

        with self.assertRaises(ValidationError) as error:
            validate_listing_photo_upload(upload)

        self.assertEqual(error.exception.code, "invalid_image")

    def test_rejects_svg_files(self):
        upload = SimpleUploadedFile(
            "floorplan.svg",
            b"<svg><script>alert(1)</script></svg>",
            content_type="image/svg+xml",
        )

        with self.assertRaises(ValidationError) as error:
            validate_listing_photo_upload(upload)

        self.assertEqual(error.exception.code, "invalid_extension")

    def test_rejects_files_above_max_size_before_image_decode(self):
        upload = SimpleUploadedFile(
            "huge.jpg",
            b"0" * (MAX_LISTING_PHOTO_BYTES + 1),
            content_type="image/jpeg",
        )

        with self.assertRaises(ValidationError) as error:
            validate_listing_photo_upload(upload)

        self.assertEqual(error.exception.code, "too_large")

    def test_rejects_client_mime_type_when_content_is_not_a_real_image(self):
        upload = SimpleUploadedFile(
            "fake.jpg",
            b"plain text but pretending to be jpeg",
            content_type="image/jpeg",
        )

        with self.assertRaises(ValidationError) as error:
            validate_listing_photo_upload(upload)

        self.assertEqual(error.exception.code, "invalid_image")
