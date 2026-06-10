import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.commissionnaires.models import CommissionnaireProfile
from apps.listings.models import Listing, ListingPhoto
from apps.listings.services import create_listing


class ListingCardTemplateTests(TestCase):
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

    def create_listing(self, **overrides):
        profile = overrides.pop("commissionnaire_profile", None) or self.create_profile()
        data = {
            "commissionnaire_profile": profile,
            "monthly_price_amount": 1200,
            "commune": "Gombe",
            "bedroom_count": 2,
            "description": "Appartement lumineux proche des services.",
            "availability_status": Listing.AvailabilityStatus.AVAILABLE,
            "submitted_at": timezone.now(),
        }
        data.update(overrides)
        return create_listing(**data)

    def add_photo(self, listing, *, position=0, is_primary=False, name="photo.jpg", alt_text=""):
        return ListingPhoto.objects.create(
            listing=listing,
            image=f"listings/{listing.pk}/{name}",
            position=position,
            is_primary=is_primary,
            alt_text=alt_text,
        )

    def test_listing_card_renders_required_fields_and_primary_photo(self):
        listing = self.create_listing()
        self.add_photo(
            listing,
            position=0,
            is_primary=False,
            name="secondary.jpg",
            alt_text="Photo secondaire",
        )
        primary = self.add_photo(
            listing,
            position=1,
            is_primary=True,
            name="primary.jpg",
            alt_text="Salon lumineux a Gombe",
        )

        response = self.client.get(reverse("listings:browse"))

        self.assertContains(response, "1200 USD / mois")
        self.assertContains(response, "Gombe")
        self.assertContains(response, "2 chambres")
        self.assertContains(response, "Mis a jour le")
        self.assertContains(response, primary.image.url)
        self.assertContains(response, 'alt="Salon lumineux a Gombe"')
        self.assertNotContains(response, "secondary.jpg")

    def test_unverified_listing_does_not_render_verification_badge(self):
        listing = self.create_listing()
        self.add_photo(listing, is_primary=True)

        response = self.client.get(reverse("listings:browse"))

        self.assertNotContains(response, "Verifiee")
        self.assertNotContains(response, "Verification")

    def test_card_body_links_to_detail_route_without_nested_actions(self):
        listing = self.create_listing()
        self.add_photo(listing, is_primary=True)
        detail_url = reverse("listings:detail", kwargs={"pk": listing.pk})

        response = self.client.get(reverse("listings:browse"))
        html = response.content.decode()

        self.assertContains(response, f'href="{detail_url}"')
        self.assertContains(
            response,
            "aria-label=\"Voir l'annonce a Gombe, 2 chambres\"",
        )
        card_link = re.search(
            r'<a\s+class="listing-card-link"[^>]*>.*?</a>',
            html,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(card_link)
        self.assertNotIn("<button", card_link.group(0))
        self.assertEqual(card_link.group(0).count("<a"), 1)

    def test_browse_empty_state_uses_default_unfiltered_copy(self):
        response = self.client.get(reverse("listings:browse"))

        self.assertContains(response, "Aucune annonce disponible pour le moment.")
        self.assertNotContains(response, "Aucune annonce ne correspond exactement.")

    def test_filter_form_renders_visible_labels_and_preserves_values(self):
        response = self.client.get(
            reverse("listings:browse"),
            {
                "commune": "Ngaliema",
                "budget_min": "500",
                "budget_max": "1500",
                "bedrooms_min": "2",
            },
        )

        self.assertContains(response, '<label for="id_commune">Commune</label>')
        self.assertContains(
            response,
            '<label for="id_budget_min">Budget minimum</label>',
        )
        self.assertContains(
            response,
            '<label for="id_budget_max">Budget maximum</label>',
        )
        self.assertContains(
            response,
            '<label for="id_bedrooms_min">Chambres minimum</label>',
        )
        self.assertContains(response, 'name="commune"')
        self.assertContains(response, 'value="Ngaliema"')
        self.assertContains(response, 'value="500"')
        self.assertContains(response, 'value="1500"')
        self.assertContains(response, 'value="2"')

    def test_active_filter_chips_and_clear_action_render(self):
        response = self.client.get(
            reverse("listings:browse"),
            {
                "commune": "Ngaliema",
                "budget_min": "500",
                "bedrooms_min": "2",
            },
        )

        self.assertContains(response, "Commune: Ngaliema")
        self.assertContains(response, "Min: 500 USD")
        self.assertContains(response, "2+ chambres")
        self.assertContains(
            response,
            'href="/annonces/?budget_min=500&amp;bedrooms_min=2"',
        )
        self.assertContains(response, 'href="/annonces/"')
        self.assertContains(response, "Effacer les filtres")

    def test_filtered_empty_state_uses_exact_copy_and_one_reset_action(self):
        self.create_listing(
            commune="Gombe",
            availability_status=Listing.AvailabilityStatus.AVAILABLE,
        )

        response = self.client.get(
            reverse("listings:browse"),
            {"commune": "Ngaliema"},
        )

        self.assertContains(response, "Aucune annonce ne correspond exactement.")
        self.assertNotContains(response, "Aucune annonce disponible pour le moment.")
        self.assertEqual(response.content.decode().count("Effacer les filtres"), 1)

    def test_result_count_live_region_exists_in_initial_html(self):
        self.create_listing(availability_status=Listing.AvailabilityStatus.AVAILABLE)

        response = self.client.get(reverse("listings:browse"))

        self.assertContains(response, 'id="listing-result-count"')
        self.assertContains(response, 'role="status"')
        self.assertContains(response, 'aria-live="polite"')
        self.assertContains(response, "1 annonce trouvée")

    def test_browse_loads_progressive_filter_script(self):
        response = self.client.get(reverse("listings:browse"))

        self.assertContains(response, 'src="/static/js/filters.js"')
        self.assertContains(response, "data-filter-form")
        self.assertContains(response, "data-filter-results")

    def test_browse_template_uses_grid_and_accessible_pagination(self):
        profile = self.create_profile()
        for index in range(13):
            listing = self.create_listing(
                commissionnaire_profile=profile,
                submitted_at=timezone.now() + timezone.timedelta(minutes=index),
            )
            self.add_photo(listing, is_primary=True, name=f"photo-{index}.jpg")

        response = self.client.get(reverse("listings:browse"))

        self.assertContains(response, 'class="browse-page"')
        self.assertContains(response, 'class="listing-grid"')
        self.assertContains(response, 'aria-label="Pagination des annonces"')
        self.assertContains(response, 'class="pagination-link"')

    def test_css_defines_responsive_grid_and_touch_targets(self):
        css = (settings.BASE_DIR / "static_src" / "css" / "input.css").read_text()

        self.assertIn(".listing-grid", css)
        self.assertIn("grid-template-columns: 1fr;", css)
        self.assertIn("@media (min-width: 700px)", css)
        self.assertIn("grid-template-columns: repeat(2, minmax(0, 1fr));", css)
        self.assertIn("@media (min-width: 921px)", css)
        self.assertIn("grid-template-columns: repeat(3, minmax(0, 1fr));", css)
        self.assertIn("aspect-ratio: 4 / 3;", css)
        self.assertIn("min-height: 44px;", css)

    def test_card_images_use_bounded_loading_controls(self):
        profile = self.create_profile()
        for index in range(3):
            listing = self.create_listing(
                commissionnaire_profile=profile,
                submitted_at=timezone.now() + timezone.timedelta(minutes=index),
            )
            self.add_photo(listing, is_primary=True, name=f"photo-{index}.jpg")

        response = self.client.get(reverse("listings:browse"))
        html = response.content.decode()

        self.assertEqual(html.count('loading="eager"'), 1)
        self.assertEqual(html.count('loading="lazy"'), 2)
        self.assertEqual(html.count('width="640"'), 3)
        self.assertEqual(html.count('height="420"'), 3)
        self.assertNotIn("spinner", html.lower())
        self.assertNotIn("infinite", html.lower())
