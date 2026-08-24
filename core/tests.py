from django.urls import reverse
from django.test import TestCase

# Create your tests here.


class CanonicalUrlTemplateTests(TestCase):
    def test_canonical_url_tag_in_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<link rel="canonical" href="http://testserver/">')
