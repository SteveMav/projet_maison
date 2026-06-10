from django.test import SimpleTestCase

from apps.listings.forms import ListingFilterForm


class ListingFilterFormTests(SimpleTestCase):
    def test_all_fields_are_optional(self):
        form = ListingFilterForm(data={})

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data,
            {
                "commune": "",
                "budget_min": None,
                "budget_max": None,
                "bedrooms_min": None,
            },
        )

    def test_numeric_filters_clean_to_integers(self):
        form = ListingFilterForm(
            data={
                "budget_min": "500",
                "budget_max": "1500",
                "bedrooms_min": "2",
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["budget_min"], 500)
        self.assertEqual(form.cleaned_data["budget_max"], 1500)
        self.assertEqual(form.cleaned_data["bedrooms_min"], 2)

    def test_commune_is_trimmed(self):
        form = ListingFilterForm(data={"commune": "  Ngaliema  "})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["commune"], "Ngaliema")

    def test_numeric_filters_reject_non_numeric_values(self):
        form = ListingFilterForm(
            data={
                "budget_min": "cheap",
                "budget_max": "many",
                "bedrooms_min": "two",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("budget_min", form.errors)
        self.assertIn("budget_max", form.errors)
        self.assertIn("bedrooms_min", form.errors)

    def test_numeric_filters_reject_negative_values(self):
        form = ListingFilterForm(
            data={
                "budget_min": "-1",
                "budget_max": "-2",
                "bedrooms_min": "-3",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("budget_min", form.errors)
        self.assertIn("budget_max", form.errors)
        self.assertIn("bedrooms_min", form.errors)

    def test_budget_max_must_be_greater_than_or_equal_to_budget_min(self):
        form = ListingFilterForm(data={"budget_min": "1500", "budget_max": "500"})

        self.assertFalse(form.is_valid())
        self.assertIn("budget_max", form.errors)
