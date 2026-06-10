from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db.models import Prefetch

from apps.commissionnaires.models import CommissionnaireProfile
from apps.listings.models import Listing, ListingPhoto
from apps.listings.selectors import get_listing_detail_queryset
from apps.listings.services import create_listing


class DetailSelectorTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="pro@example.com",
            password="StrongPass123!",
            whatsapp_phone="+243990000000",
        )
        self.profile = CommissionnaireProfile.objects.create(
            user=self.user,
            display_name="Maison Pro",
            whatsapp_phone="+243990000000",
        )

    def create_listing(self, **overrides):
        data = {
            "commissionnaire_profile": self.profile,
            "monthly_price_amount": 1200,
            "commune": "Gombe",
            "bedroom_count": 2,
            "description": "Appartement lumineux proche des services.",
            "availability_status": Listing.AvailabilityStatus.AVAILABLE,
        }
        data.update(overrides)
        return create_listing(**data)

    def test_available_listing_is_eligible(self):
        listing = self.create_listing(availability_status=Listing.AvailabilityStatus.AVAILABLE)
        qs = get_listing_detail_queryset()
        self.assertIn(listing, qs)

    def test_unavailable_listing_is_eligible(self):
        listing = self.create_listing(availability_status=Listing.AvailabilityStatus.UNAVAILABLE)
        qs = get_listing_detail_queryset()
        self.assertIn(listing, qs)

    def test_under_review_listing_is_not_eligible(self):
        listing = self.create_listing(availability_status=Listing.AvailabilityStatus.UNDER_REVIEW)
        qs = get_listing_detail_queryset()
        self.assertNotIn(listing, qs)

    def test_photos_are_ordered_deterministically(self):
        listing = self.create_listing()
        photo1 = ListingPhoto.objects.create(listing=listing, image="p1.jpg", position=2, is_primary=False)
        photo2 = ListingPhoto.objects.create(listing=listing, image="p2.jpg", position=1, is_primary=True)
        photo3 = ListingPhoto.objects.create(listing=listing, image="p3.jpg", position=0, is_primary=False)

        qs = get_listing_detail_queryset()
        fetched_listing = qs.get(pk=listing.pk)
        photos = list(fetched_listing.photos.all())

        self.assertEqual(len(photos), 3)
        self.assertEqual(photos[0], photo2)
        self.assertEqual(photos[1], photo3)
        self.assertEqual(photos[2], photo1)

    def test_query_count_is_bounded(self):
        listing1 = self.create_listing()
        ListingPhoto.objects.create(listing=listing1, image="p1.jpg", position=0)
        ListingPhoto.objects.create(listing=listing1, image="p2.jpg", position=1)

        listing2 = self.create_listing()
        ListingPhoto.objects.create(listing=listing2, image="p3.jpg", position=0)

        with self.assertNumQueries(2):
            qs = get_listing_detail_queryset()
            listings = list(qs)
            for l in listings:
                list(l.photos.all())
                l.commissionnaire_profile.display_name
