from django.urls import reverse
from django.test import TestCase

# Create your tests here.


from blog.models import Post, Category
from portfolio.models import Project
from django.utils import timezone

class CanonicalUrlTemplateTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Tech", slug="tech")
        self.post = Post.objects.create(
            title="Post Canonical Test",
            slug="post-canonical-test",
            excerpt="Excerpt",
            body="Body",
            category=self.category,
            status="published",
            published_at=timezone.now(),
        )
        self.project = Project.objects.create(
            title="Project Canonical Test",
            slug="project-canonical-test",
            summary="Summary",
            body="Body",
        )

    def test_canonical_url_tag_in_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertEqual(content.count('rel="canonical"'), 1)
        self.assertContains(response, '<link rel="canonical" href="http://testserver/">')

    def test_canonical_url_tag_in_blog_index(self):
        response = self.client.get(reverse('blog'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertEqual(content.count('rel="canonical"'), 1)
        self.assertContains(response, '<link rel="canonical" href="http://testserver/blog/">')

    def test_canonical_url_tag_in_blog_detail(self):
        response = self.client.get(reverse('post_detail', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertEqual(content.count('rel="canonical"'), 1)
        self.assertContains(response, f'<link rel="canonical" href="http://testserver/blog/{self.post.slug}/">')

    def test_canonical_url_tag_in_portfolio_detail(self):
        response = self.client.get(reverse('project_detail', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertEqual(content.count('rel="canonical"'), 1)
        self.assertContains(response, f'<link rel="canonical" href="http://testserver/portfolio/{self.project.slug}/">')

    def test_canonical_url_strips_query_parameters(self):
        response = self.client.get(reverse('blog') + '?q=search&utm_source=twitter&gclid=123')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertEqual(content.count('rel="canonical"'), 1)
        self.assertContains(response, '<link rel="canonical" href="http://testserver/blog/">')
        # query parameters not present in canonical URL tag
        self.assertContains(response, '<link rel="canonical" href="http://testserver/blog/">')
        self.assertNotContains(response, 'gclid')

    def test_htmx_partial_response_does_not_emit_canonical_tag(self):
        response = self.client.get(reverse('blog'), HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'rel="canonical"')


import os
from unittest import mock
from django.conf import settings

class WhiteNoiseSettingsTests(TestCase):
    def test_production_default_is_manifest_strict(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            wn_env = os.environ.get('WHITENOISE_MANIFEST_STRICT')
            use_sqlite = str(os.environ.get('USE_SQLITE', 'False')).strip().lower() in {'1', 'true', 'yes', 'on'}
            strict = (str(wn_env).strip().lower() in {'1', 'true', 'yes', 'on'}) if wn_env is not None else not use_sqlite
            self.assertTrue(strict)

    def test_explicit_test_configuration_can_be_non_strict(self):
        with mock.patch.dict(os.environ, {'USE_SQLITE': 'True'}, clear=True):
            wn_env = os.environ.get('WHITENOISE_MANIFEST_STRICT')
            use_sqlite = str(os.environ.get('USE_SQLITE', 'False')).strip().lower() in {'1', 'true', 'yes', 'on'}
            strict = (str(wn_env).strip().lower() in {'1', 'true', 'yes', 'on'}) if wn_env is not None else not use_sqlite
            self.assertFalse(strict)

    def test_unrecognized_env_values_default_to_false_for_env_setting(self):
        # Unrecognized value for WHITENOISE_MANIFEST_STRICT (e.g. "invalid") yields False for that env setting, but if absent defaults to True
        with mock.patch.dict(os.environ, {'WHITENOISE_MANIFEST_STRICT': 'invalid'}, clear=True):
            wn_env = os.environ.get('WHITENOISE_MANIFEST_STRICT')
            strict = str(wn_env).strip().lower() in {'1', 'true', 'yes', 'on'}
            self.assertFalse(strict)

        with mock.patch.dict(os.environ, {'WHITENOISE_MANIFEST_STRICT': '1'}, clear=True):
            wn_env = os.environ.get('WHITENOISE_MANIFEST_STRICT')
            strict = str(wn_env).strip().lower() in {'1', 'true', 'yes', 'on'}
            self.assertTrue(strict)
