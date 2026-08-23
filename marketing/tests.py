import json
from io import StringIO
from django.test import TestCase
from django.urls import reverse


class MarketingPageTests(TestCase):
    def test_home_page_renders(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Built for creators. Engineered for modern work.')

    def test_about_page_renders(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'We build with clarity, momentum, and systems that actually hold up.')

    def test_services_page_renders(self):
        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Built for creators. Engineered for modern work.')
