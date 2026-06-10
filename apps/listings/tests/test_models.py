from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, models, transaction
from django.db.models import CASCADE, PROTECT, Q
from django.db.models import ProtectedError
from django.test import SimpleTestCase
from django.test import TestCase
from django.utils import timezone

from apps.commissionnaires.models import CommissionnaireProfile
from apps.listings.models import Listing, ListingPhoto, listing_photo_upload_to
from apps.listings.services import set_primary_photo
from apps.listings.validators import validate_listing_photo_upload


class ListingModelTests(SimpleTestCase):
    def build_listing(self, **overrides):
        data = {
            "commissionnaire_profile": CommissionnaireProfile(
                id=1,
                user_id=1,
                display_name="Maison Pro",
                whatsapp_phone="+243990000000",
            ),
            "monthly_price_amount": 1200,
            "commune": "Gombe",
            "bedroom_count": 2,
            "description": "Appartement lumineux proche des services.",
            "submitted_at": timezone.now(),
        }
        data.update(overrides)
        return Listing(**data)

    def test_listing_belongs_to_exactly_one_commissionnaire_profile(self):
        field = Listing._meta.get_field("commissionnaire_profile")

        self.assertEqual(field.remote_field.model, CommissionnaireProfile)
        self.assertEqual(field.remote_field.on_delete, PROTECT)
        self.assertEqual(field.remote_field.related_name, "listings")
        self.assertFalse(field.null)

    def test_required_listing_fields_validate(self):
        required_fields = [
            "commissionnaire_profile",
            "monthly_price_amount",
            "commune",
            "description",
            "submitted_at",
        ]

        for field_name in required_fields:
            with self.subTest(field=field_name):
                listing = self.build_listing(**{field_name: None})

                with self.assertRaises(ValidationError) as error:
                    if field_name == "commissionnaire_profile":
                        listing.full_clean()
                    else:
                        listing.full_clean(exclude=["commissionnaire_profile"])

                self.assertIn(field_name, error.exception.message_dict)

        listing = self.build_listing(bedroom_count=None)
        with self.assertRaises(ValidationError) as error:
            listing.full_clean(exclude=["commissionnaire_profile"])
        self.assertIn("bedroom_count", error.exception.message_dict)

    def test_status_defaults_to_under_review_and_accepts_only_declared_values(self):
        listing = self.build_listing()

        self.assertEqual(
            listing.availability_status,
            Listing.AvailabilityStatus.UNDER_REVIEW,
        )
        self.assertEqual(
            {choice.value for choice in Listing.AvailabilityStatus},
            {"available", "unavailable", "under_review"},
        )

        listing.availability_status = "leased"
        with self.assertRaises(ValidationError) as error:
            listing.full_clean(exclude=["commissionnaire_profile"])

        self.assertIn("availability_status", error.exception.message_dict)

    def test_monthly_price_is_stored_as_integer_usd_not_float(self):
        amount_field = Listing._meta.get_field("monthly_price_amount")
        currency_field = Listing._meta.get_field("monthly_price_currency")

        self.assertIsInstance(amount_field, models.PositiveIntegerField)
        self.assertNotIsInstance(amount_field, models.FloatField)
        self.assertEqual(currency_field.default, Listing.Currency.USD)
        self.assertEqual(
            {choice.value for choice in Listing.Currency},
            {"USD"},
        )

    def test_timestamps_are_stored_on_create_and_update(self):
        listing = self.build_listing()
        listing.full_clean(exclude=["commissionnaire_profile"])

        self.assertIsNotNone(listing.submitted_at)
        self.assertTrue(Listing._meta.get_field("created_at").auto_now_add)
        self.assertTrue(Listing._meta.get_field("updated_at").auto_now)
        self.assertLessEqual(listing.submitted_at, timezone.now())

    def test_listing_indexes_support_later_browse_filters(self):
        index_fields = {tuple(index.fields) for index in Listing._meta.indexes}

        self.assertIn(("availability_status", "-updated_at"), index_fields)
        self.assertIn(("commune",), index_fields)
        self.assertIn(("bedroom_count",), index_fields)
        self.assertIn(("monthly_price_amount",), index_fields)


class ListingAdminTests(SimpleTestCase):
    def test_listing_model_is_registered_with_safe_admin_fields(self):
        model_admin = admin.site._registry[Listing]

        self.assertIn("commune", model_admin.list_display)
        self.assertIn("monthly_price_amount", model_admin.list_display)
        self.assertIn("availability_status", model_admin.list_filter)
        self.assertIn("commune", model_admin.list_filter)
        self.assertIn("commune", model_admin.search_fields)
        self.assertIn("description", model_admin.search_fields)


class ListingDatabaseModelTests(TestCase):
    def create_profile(self, email=None):
        if email is None:
            email = f"pro{get_user_model().objects.count() + 1}@example.com"
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

    def build_listing(self, profile=None, **overrides):
        data = {
            "commissionnaire_profile": profile or self.create_profile(),
            "monthly_price_amount": 1200,
            "commune": "Gombe",
            "bedroom_count": 2,
            "description": "Appartement lumineux proche des services.",
            "submitted_at": timezone.now(),
        }
        data.update(overrides)
        return Listing(**data)

    def test_listing_persistence_requires_profile_and_protects_owner(self):
        profile = self.create_profile()
        listing = self.build_listing(profile=profile)
        listing.full_clean()
        listing.save()

        with self.assertRaises(ProtectedError):
            profile.delete()

        listing.delete()
        self.assertTrue(CommissionnaireProfile.objects.filter(pk=profile.pk).exists())

        without_profile = Listing(
            monthly_price_amount=1200,
            commune="Gombe",
            bedroom_count=2,
            description="Appartement lumineux proche des services.",
            submitted_at=timezone.now(),
        )
        with self.assertRaises(IntegrityError):
            without_profile.save()

    def test_saved_listing_timestamps_and_required_fields_validate(self):
        listing = self.build_listing()
        listing.full_clean()
        listing.save()

        self.assertIsNotNone(listing.submitted_at)
        self.assertIsNotNone(listing.created_at)
        self.assertIsNotNone(listing.updated_at)

        for field_name in [
            "commissionnaire_profile",
            "monthly_price_amount",
            "commune",
            "bedroom_count",
            "description",
            "submitted_at",
        ]:
            with self.subTest(field=field_name):
                invalid = self.build_listing(**{field_name: None})
                with self.assertRaises(ValidationError) as error:
                    invalid.full_clean()
                self.assertIn(field_name, error.exception.message_dict)

    def test_invalid_availability_status_is_rejected_by_model_validation(self):
        listing = self.build_listing(availability_status="leased")

        with self.assertRaises(ValidationError) as error:
            listing.full_clean()

        self.assertIn("availability_status", error.exception.message_dict)

    def test_database_constraints_limit_photo_positions_and_primary(self):
        listing = self.build_listing()
        listing.full_clean()
        listing.save()
        ListingPhoto.objects.create(
            listing=listing,
            image="listings/1/first.jpg",
            position=0,
            is_primary=True,
        )

        with self.assertRaises(IntegrityError), transaction.atomic():
            ListingPhoto.objects.create(
                listing=listing,
                image="listings/1/duplicate-position.jpg",
                position=0,
            )

        with self.assertRaises(IntegrityError), transaction.atomic():
            ListingPhoto.objects.create(
                listing=listing,
                image="listings/1/duplicate-primary.jpg",
                position=1,
                is_primary=True,
            )


class ListingPhotoModelTests(SimpleTestCase):
    def test_photo_belongs_to_listing_and_uses_local_listing_media_path(self):
        listing_field = ListingPhoto._meta.get_field("listing")
        image_field = ListingPhoto._meta.get_field("image")

        self.assertEqual(listing_field.remote_field.model, Listing)
        self.assertEqual(listing_field.remote_field.on_delete, CASCADE)
        self.assertEqual(listing_field.remote_field.related_name, "photos")
        self.assertIsInstance(image_field, models.ImageField)
        self.assertEqual(image_field.upload_to, listing_photo_upload_to)
        self.assertIn(validate_listing_photo_upload, image_field.validators)
        self.assertTrue(
            listing_photo_upload_to(ListingPhoto(listing_id=42), "living room.JPG").startswith(
                "listings/42/"
            )
        )

    def test_photo_metadata_and_ordering_are_deterministic(self):
        position_field = ListingPhoto._meta.get_field("position")
        primary_field = ListingPhoto._meta.get_field("is_primary")
        alt_text_field = ListingPhoto._meta.get_field("alt_text")

        self.assertIsInstance(position_field, models.PositiveSmallIntegerField)
        self.assertEqual(position_field.default, 0)
        self.assertFalse(primary_field.default)
        self.assertEqual(alt_text_field.max_length, 180)
        self.assertTrue(alt_text_field.blank)
        self.assertEqual(ListingPhoto._meta.ordering, ["position", "id"])

    def test_photo_constraints_limit_position_and_primary_per_listing(self):
        constraints = {constraint.name: constraint for constraint in ListingPhoto._meta.constraints}

        self.assertIn("unique_listing_photo_position", constraints)
        self.assertEqual(
            constraints["unique_listing_photo_position"].fields,
            ("listing", "position"),
        )
        self.assertIn("unique_primary_photo_per_listing", constraints)
        self.assertEqual(
            constraints["unique_primary_photo_per_listing"].fields,
            ("listing",),
        )
        self.assertEqual(
            constraints["unique_primary_photo_per_listing"].condition,
            Q(is_primary=True),
        )

    def test_listing_exposes_primary_photo_helper(self):
        self.assertTrue(hasattr(Listing, "get_primary_photo"))

    def test_service_level_primary_enforcement_helper_is_available(self):
        self.assertTrue(callable(set_primary_photo))


class ListingPhotoAdminTests(SimpleTestCase):
    def test_listing_admin_includes_photo_inline(self):
        model_admin = admin.site._registry[Listing]

        inline_models = {inline.model for inline in model_admin.inlines}

        self.assertIn(ListingPhoto, inline_models)
