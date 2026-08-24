from django.template import Context, Template
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from blog.models import Category, Post
from blog.utils import (
    get_facebook_share_url,
    get_linkedin_share_url,
    get_share_urls,
    get_twitter_share_url,
    get_x_share_url,
)


class SocialShareUtilsTests(TestCase):
    def test_get_facebook_share_url(self):
        url = "https://waitaminutedigital.com/blog/test-post/"
        share_url = get_facebook_share_url(url)
        self.assertIn("https://www.facebook.com/sharer/sharer.php?", share_url)
        self.assertIn("u=https%3A%2F%2Fwaitaminutedigital.com%2Fblog%2Ftest-post%2F", share_url)

    def test_get_twitter_share_url(self):
        url = "https://waitaminutedigital.com/blog/test-post/"
        title = "Test Blog Post"
        share_url = get_twitter_share_url(url, text=title)
        self.assertIn("https://x.com/intent/tweet?", share_url)
        self.assertIn("url=https%3A%2F%2Fwaitaminutedigital.com%2Fblog%2Ftest-post%2F", share_url)
        self.assertIn("text=Test+Blog+Post", share_url)

    def test_get_x_share_url_alias(self):
        url = "https://waitaminutedigital.com/blog/test-post/"
        title = "Test Blog Post"
        share_url = get_x_share_url(url, text=title)
        self.assertEqual(share_url, get_twitter_share_url(url, text=title))

    def test_get_linkedin_share_url(self):
        url = "https://waitaminutedigital.com/blog/test-post/"
        share_url = get_linkedin_share_url(url)
        self.assertIn("https://www.linkedin.com/sharing/share-offsite/?", share_url)
        self.assertIn("url=https%3A%2F%2Fwaitaminutedigital.com%2Fblog%2Ftest-post%2F", share_url)

    def test_get_share_urls_dictionary(self):
        url = "https://waitaminutedigital.com/blog/test-post/"
        title = "My Post"
        urls = get_share_urls(url, title=title)
        self.assertIn('facebook', urls)
        self.assertIn('twitter', urls)
        self.assertIn('x', urls)
        self.assertIn('linkedin', urls)


class PostSocialShareModelTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(name="Engineering", slug="engineering")
        self.post = Post.objects.create(
            title="Building Modern Web Apps",
            slug="building-modern-web-apps",
            excerpt="A deep dive into architecture and systems.",
            body="Post body text goes here.",
            category=self.category,
            status="published",
            published_at=timezone.now(),
        )

    def test_get_share_image_url_fallback(self):
        request = self.factory.get(self.post.get_absolute_url())
        image_url = self.post.get_share_image_url(request)
        self.assertTrue(image_url.startswith("http://") or image_url.startswith("https://"))
        self.assertIn("wmd-logo-full-onblack.png", image_url)

    def test_get_share_image_url_youtube(self):
        self.post.youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.post.save()
        request = self.factory.get(self.post.get_absolute_url())
        image_url = self.post.get_share_image_url(request)
        self.assertEqual(image_url, "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg")

    def test_get_share_urls_method(self):
        request = self.factory.get(self.post.get_absolute_url())
        urls = self.post.get_share_urls(request)
        self.assertIn("facebook", urls)
        self.assertIn("twitter", urls)
        self.assertIn("linkedin", urls)
        self.assertIn(self.post.slug, urls["facebook"])


class SocialShareTemplateTagsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.post = Post.objects.create(
            title="Design Systems Guide",
            slug="design-systems-guide",
            excerpt="How to build modular CSS design tokens.",
            body="Guide contents.",
            status="published",
            published_at=timezone.now(),
        )

    def test_template_tag_filters(self):
        template = Template(
            "{% load blog_tags %}"
            "FB: {{ post|facebook_share_url:request }} | "
            "X: {{ post|x_share_url:request }} | "
            "LI: {{ post|linkedin_share_url:request }} | "
            "IMG: {{ post|share_image_url:request }}"
        )
        request = self.factory.get(self.post.get_absolute_url())
        rendered = template.render(Context({'post': self.post, 'request': request}))
        self.assertIn("facebook.com/sharer/sharer.php", rendered)
        self.assertIn("x.com/intent/tweet", rendered)
        self.assertIn("linkedin.com/sharing/share-offsite", rendered)

    def test_share_buttons_inclusion_tag(self):
        template = Template(
            "{% load blog_tags %}"
            "{% share_buttons post=post %}"
        )
        request = self.factory.get(self.post.get_absolute_url())
        rendered = template.render(Context({'post': self.post, 'request': request}))
        self.assertIn("share-btn-facebook", rendered)
        self.assertIn("share-btn-x", rendered)
        self.assertIn("share-btn-linkedin", rendered)
        self.assertIn("share-btn-copy", rendered)


class PostDetailSocialShareViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Insights", slug="insights")
        self.post = Post.objects.create(
            title="Why Open Graph Matters for Publishers",
            slug="why-open-graph-matters-for-publishers",
            excerpt="Mastering rich link previews across social media and messaging platforms.",
            body="Content explaining Open Graph, Twitter Cards, and social buttons.",
            category=self.category,
            status="published",
            published_at=timezone.now(),
        )

    def test_post_detail_renders_open_graph_meta_tags(self):
        url = reverse('post_detail', kwargs={'slug': self.post.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        # Open Graph tags
        self.assertContains(response, '<meta property="og:type" content="article">')
        self.assertContains(response, f'<meta property="og:title" content="{self.post.title} | Waitaminute Digital">')
        self.assertContains(response, f'<meta property="og:description" content="{self.post.excerpt}">')
        self.assertContains(response, f'<meta property="og:url" content="http://testserver{url}">')
        self.assertContains(response, '<meta property="og:image" content=')

        # Twitter Card tags
        self.assertContains(response, '<meta name="twitter:card" content="summary_large_image">')
        self.assertContains(response, f'<meta name="twitter:title" content="{self.post.title} | Waitaminute Digital">')
        self.assertContains(response, f'<meta name="twitter:description" content="{self.post.excerpt}">')
        self.assertContains(response, '<meta name="twitter:image" content=')

    def test_post_detail_renders_social_share_buttons(self):
        url = reverse('post_detail', kwargs={'slug': self.post.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        # Social sharing buttons
        self.assertContains(response, 'class="share-btn share-btn-facebook"')
        self.assertContains(response, 'class="share-btn share-btn-x"')
        self.assertContains(response, 'class="share-btn share-btn-linkedin"')
        self.assertContains(response, 'class="share-btn share-btn-copy"')

        # Check button contents & labels
        self.assertContains(response, 'aria-label="Share on Facebook"')
        self.assertContains(response, 'aria-label="Share on X (Twitter)"')
        self.assertContains(response, 'aria-label="Share on LinkedIn"')
        self.assertContains(response, 'aria-label="Copy link to clipboard"')
        self.assertContains(response, 'Copy Link')

        # Check share URLs contain encoded link to the post
        self.assertContains(response, 'facebook.com/sharer/sharer.php')
        self.assertContains(response, 'x.com/intent/tweet')
        self.assertContains(response, 'linkedin.com/sharing/share-offsite')
        self.assertContains(response, self.post.slug)



from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

import io
from PIL import Image

def _create_test_image(format='PNG', size=(10, 10), color=(255, 0, 0)):
    buf = io.BytesIO()
    img = Image.new('RGB', size, color=color)
    img.save(buf, format=format)
    buf.seek(0)
    return buf.getvalue()

class PostImageValidationTests(TestCase):
    def test_valid_png_image(self):
        content = _create_test_image('PNG')
        uploaded = SimpleUploadedFile("valid.png", content, content_type="image/png")
        post = Post(title="Valid PNG", slug="valid-png", excerpt="S", body="B", cover_image=uploaded)
        post.full_clean()  # should not raise

    def test_valid_jpeg_image(self):
        content = _create_test_image('JPEG')
        uploaded = SimpleUploadedFile("valid.jpg", content, content_type="image/jpeg")
        post = Post(title="Valid JPG", slug="valid-jpg", excerpt="S", body="B", cover_image=uploaded)
        post.full_clean()  # should not raise

    def test_uppercase_allowed_extension(self):
        content = _create_test_image('PNG')
        uploaded = SimpleUploadedFile("valid.PNG", content, content_type="image/png")
        post = Post(title="Valid Upper PNG", slug="valid-upper-png", excerpt="S", body="B", cover_image=uploaded)
        post.full_clean()  # should not raise

    def test_fake_bytes_named_jpg_raises_validation_error(self):
        fake_file = SimpleUploadedFile("fake.jpg", b"not an image", content_type="image/jpeg")
        post = Post(title="Fake JPG", slug="fake-jpg", excerpt="S", body="B", cover_image=fake_file)
        with self.assertRaises(ValidationError) as ctx:
            post.full_clean()
        self.assertIn("Invalid image file content", str(ctx.exception))

    def test_invalid_image_extension_raises_validation_error(self):
        invalid_file = SimpleUploadedFile("script.py", b"print('hello')", content_type="text/x-python")
        post = Post(title="Test Post", slug="test-post", excerpt="Summary", body="Content", cover_image=invalid_file)
        with self.assertRaises(ValidationError) as ctx:
            post.full_clean()
        self.assertIn("Unsupported image file extension", str(ctx.exception))

    def test_oversized_image_raises_validation_error(self):
        large_file = SimpleUploadedFile("huge_photo.jpg", b"0" * (10 * 1024 * 1024 + 1), content_type="image/jpeg")
        post = Post(title="Test Post Large Image", slug="test-post-large-image", excerpt="Summary", body="Content", cover_image=large_file)
        with self.assertRaises(ValidationError) as ctx:
            post.full_clean()
        self.assertIn("File size exceeds maximum allowed limit", str(ctx.exception))

    def test_missing_optional_image(self):
        post = Post(title="No Image", slug="no-image", excerpt="S", body="B")
        post.full_clean()  # should not raise
