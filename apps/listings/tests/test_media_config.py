from django.conf import settings
from django.conf.urls.static import static
from django.test import SimpleTestCase, override_settings

from apps.listings.models import ListingPhoto, listing_photo_upload_to


class ListingMediaConfigTests(SimpleTestCase):
    def test_local_media_settings_are_configured(self):
        self.assertEqual(settings.MEDIA_URL, "/media/")
        self.assertTrue(str(settings.MEDIA_ROOT).endswith("media"))

    @override_settings(DEBUG=True)
    def test_debug_urlpatterns_serve_media_with_django_static_helper(self):
        debug_media_patterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

        self.assertTrue(debug_media_patterns)
        self.assertIn("media", str(debug_media_patterns[0].pattern))

    def test_listing_upload_path_stays_under_media_not_static(self):
        upload_path = listing_photo_upload_to(ListingPhoto(listing_id=7), "room.jpg")

        self.assertTrue(upload_path.startswith("listings/7/"))
        self.assertFalse(upload_path.startswith("static/"))
