import json
from io import StringIO
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from blog.models import Category, Post


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


class HomeInsightsSectionTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Strategy", slug="strategy")

    def _make_post(self, title, slug, offset_days=0):
        return Post.objects.create(
            title=title,
            slug=slug,
            excerpt=f"Excerpt for {title}.",
            body=f"Body for {title}.",
            category=self.category,
            status='published',
            published_at=timezone.now() - timezone.timedelta(days=offset_days),
        )

    def test_home_renders_no_posts_gracefully(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Insights')
        # No hardcoded articles, no crash
        self.assertNotContains(response, 'Designing a website that acts like a sales system')

    def test_home_shows_single_post_as_featured(self):
        post = self._make_post("Only Post", "only-post")
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)
        self.assertContains(response, 'insight-card-featured')

    def test_home_shows_up_to_four_posts(self):
        posts = [self._make_post(f"Post {i}", f"post-{i}", offset_days=i) for i in range(4)]
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        for post in posts:
            self.assertContains(response, post.title)

    def test_home_does_not_show_fifth_post(self):
        for i in range(5):
            self._make_post(f"Post {i}", f"post-{i}", offset_days=i)
        response = self.client.get(reverse('home'))
        # Fifth (oldest) post should not appear on homepage
        self.assertNotContains(response, 'Post 4')

    def test_home_featured_post_is_newest(self):
        old = self._make_post("Old Post", "old-post", offset_days=10)
        new = self._make_post("New Post", "new-post", offset_days=0)
        response = self.client.get(reverse('home'))
        content = response.content.decode()
        # Featured (first occurrence) should be the newest post
        self.assertLess(content.index('New Post'), content.index('Old Post'))

    def test_home_view_all_articles_link_present(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'View All Articles')
        self.assertContains(response, reverse('blog'))

    def test_home_draft_posts_not_shown(self):
        Post.objects.create(
            title="Draft Post",
            slug="draft-post",
            excerpt="This is a draft.",
            body="Draft body.",
            status='draft',
        )
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, 'Draft Post')

