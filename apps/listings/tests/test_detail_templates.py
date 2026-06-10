from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.commissionnaires.models import CommissionnaireProfile
from apps.listings.models import Listing, ListingPhoto
from apps.listings.services import create_listing


class DetailTemplateTests(TestCase):
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

    def test_detail_renders_all_fields(self):
        listing = self.create_listing(
            commune="Gombe",
            monthly_price_amount=1500,
            bedroom_count=3,
            description="Superbe appartement familial."
        )
        photo = ListingPhoto.objects.create(listing=listing, image="img.jpg", alt_text="Ma jolie photo")

        url = reverse("listings:detail", kwargs={"pk": listing.pk})
        response = self.client.get(url)

        self.assertContains(response, "1500 USD / mois")
        self.assertContains(response, "Logement à Gombe")
        self.assertContains(response, "3 chambres")
        self.assertContains(response, "Superbe appartement familial.")
        self.assertContains(response, "Maison Pro")
        self.assertContains(response, "Le contact WhatsApp passe par une identification légère.")
        self.assertContains(response, "Signaler cette annonce")
        self.assertContains(response, "Disponible")
        self.assertContains(response, "Mis à jour le")
        self.assertContains(response, "1/1")
        self.assertContains(response, "Ma jolie photo")

    def test_whatsapp_cta_visibility(self):
        # Available listing shows CTA
        available = self.create_listing(availability_status=Listing.AvailabilityStatus.AVAILABLE)
        url_available = reverse("listings:detail", kwargs={"pk": available.pk})
        response = self.client.get(url_available)
        self.assertContains(response, "Contacter sur WhatsApp")
        self.assertContains(response, "data-contact-whatsapp")

        # Unavailable listing hides CTA and shows return-to-results
        unavailable = self.create_listing(availability_status=Listing.AvailabilityStatus.UNAVAILABLE)
        url_unavailable = reverse("listings:detail", kwargs={"pk": unavailable.pk})
        response = self.client.get(url_unavailable)
        self.assertNotContains(response, "Contacter sur WhatsApp")
        self.assertContains(response, "Cette annonce n'est plus disponible.")
        self.assertContains(response, "Voir d'autres annonces")

    def test_unverified_listing_renders_no_badge(self):
        listing = self.create_listing()
        url = reverse("listings:detail", kwargs={"pk": listing.pk})
        response = self.client.get(url)
        self.assertNotContains(response, "Cette annonce a passé un contrôle supplémentaire")
        self.assertNotContains(response, "Verifiée")

    def test_verified_listing_renders_badge_if_simulated(self):
        listing = self.create_listing()
        # Mock is_verified to True
        listing.is_verified = True
        listing.save()

        # Let's verify our custom properties are accessible
        # In python we can dynamically set it on the fetched listing.
        # But wait! We need to make sure the view forwards it or model has a way.
        # Let's check: in django, since is_verified isn't a database field, if we set it on listing,
        # it is not saved unless we override or it's a property.
        # Wait, does the django model have an is_verified property? Let's check:
        # In models.py we saw:
        # ```python
        # # No is_verified in models.py
        # ```
        # Wait, if we set it as an annotation or property, can we do it?
        # Let's check listing_card.html:
        # `{% if listing.is_verified %}`
        # Wait, how does a listing become verified in the code?
        # Is there any other place where `is_verified` is defined? No, our grep search only returned `listing_card.html`.
        # So it is probably not defined yet, but the template checks for it.
        # If we set `listing.is_verified = True` in Python and pass it to a context/render, it will render correctly!
        # But since DetailView fetches the object from queryset, how can we test it?
        # We can dynamically attach `is_verified` inside a test by mocking the queryset or view context, or we can just mock/monkeypatch it on the model class for this test!
        # E.g.:
        # `Listing.is_verified = True` (on class level) during the test, then clean up.
        # Yes, that's incredibly simple and clean!
        
        Listing.is_verified = True
        try:
            url = reverse("listings:detail", kwargs={"pk": listing.pk})
            response = self.client.get(url)
            self.assertContains(response, "Cette annonce a passé un contrôle supplémentaire. Le badge ne garantit pas le résultat d'une transaction hors ligne.")
        finally:
            del Listing.is_verified
