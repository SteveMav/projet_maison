from django.test import SimpleTestCase
from django.urls import reverse


class CoreRouteTests(SimpleTestCase):
    def test_home_route_is_public(self):
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")
        self.assertContains(response, "Maison")
