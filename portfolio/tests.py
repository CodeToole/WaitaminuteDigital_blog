import html

from django.core.files.uploadedfile import SimpleUploadedFile
from django.template import Context, Template
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from portfolio.models import Project, Tag


class ProjectSocialShareModelTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.tag = Tag.objects.create(name="Web", slug="web")
        self.project = Project.objects.create(
            title="The Acting Collective",
            slug="acting-collective",
            client="The Acting Collective — Powered by Ziare",
            summary="A direct pipeline from acting training to real film credits.",
            body="Project long-form body text.",
            url="https://theactingcollective.vip",
            is_featured=True,
        )
        self.project.tags.add(self.tag)

    def test_get_share_image_url_fallback(self):
        request = self.factory.get(self.project.get_absolute_url())
        image_url = self.project.get_share_image_url(request)
        self.assertTrue(image_url.startswith("http://") or image_url.startswith("https://"))
        self.assertIn("wmd-logo-full-onblack.png", image_url)

    def test_get_share_image_url_with_cover(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        cover = SimpleUploadedFile('cover.gif', small_gif, content_type='image/gif')
        self.project.cover_image = cover
        self.project.save()

        request = self.factory.get(self.project.get_absolute_url())
        image_url = self.project.get_share_image_url(request)
        self.assertIn(self.project.cover_image.url, image_url)

    def test_get_share_image_url_youtube(self):
        self.project.youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.project.save()
        request = self.factory.get(self.project.get_absolute_url())
        image_url = self.project.get_share_image_url(request)
        self.assertEqual(image_url, "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg")

    def test_get_share_urls_method(self):
        request = self.factory.get(self.project.get_absolute_url())
        urls = self.project.get_share_urls(request)
        self.assertIn("facebook", urls)
        self.assertIn("twitter", urls)
        self.assertIn("x", urls)
        self.assertIn("linkedin", urls)
        self.assertIn(self.project.slug, urls["facebook"])
        self.assertIn(self.project.slug, urls["x"])


class ProjectDetailSocialShareViewTests(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Brand", slug="brand")
        self.project_without_cover = Project.objects.create(
            title="Unicorn Bounty Hunters",
            slug="unicorn-bounty-hunters",
            client="Unicorn Bounty Hunters LLC",
            summary="A studio-booking and artist-roster site for an independent Mobile music collective.",
            body="Full project narrative.",
            url="https://unicornbountyhunters.com",
            is_featured=True,
        )
        self.project_without_cover.tags.add(self.tag)

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.cover = SimpleUploadedFile('sample_cover.gif', small_gif, content_type='image/gif')
        self.project_with_cover = Project.objects.create(
            title="Huncho Fest",
            slug="huncho-fest",
            client="Huncho Fest — presented by NMBG Jay",
            summary="The event and artist-registration site for Mobile's biggest independent music festival.",
            body="Music festival web experience.",
            cover_image=self.cover,
            url="https://hunchofest.com",
            is_featured=False,
        )
        self.project_with_cover.tags.add(self.tag)

    def test_project_detail_renders_open_graph_and_twitter_meta_tags(self):
        for project, has_cover in [(self.project_without_cover, False), (self.project_with_cover, True)]:
            url = reverse('project_detail', kwargs={'slug': project.slug})
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)

            # Open Graph tags
            self.assertContains(response, '<meta property="og:type" content="article">')
            self.assertContains(response, f'<meta property="og:title" content="{project.title} | Waitaminute Digital">')
            self.assertContains(response, f'<meta property="og:description" content="{html.escape(project.summary)}">')
            self.assertContains(response, f'<meta property="og:url" content="http://testserver{url}">')
            self.assertContains(response, '<meta property="og:image" content=')

            # Twitter Card tags
            self.assertContains(response, '<meta name="twitter:card" content="summary_large_image">')
            self.assertContains(response, f'<meta name="twitter:title" content="{project.title} | Waitaminute Digital">')
            self.assertContains(response, f'<meta name="twitter:description" content="{html.escape(project.summary)}">')
            self.assertContains(response, '<meta name="twitter:image" content=')

            # Cover vs Fallback image validation
            if has_cover:
                self.assertContains(response, project.cover_image.url)
            else:
                self.assertContains(response, 'wmd-logo-full-onblack.png')

    def test_project_detail_renders_social_share_buttons_both_placements(self):
        url = reverse('project_detail', kwargs={'slug': self.project_without_cover.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        # Both placements (header and footer)
        content = response.content.decode('utf-8')
        self.assertEqual(content.count('data-post-url='), 2)
        self.assertContains(response, 'class="article-meta-row"')
        self.assertContains(response, 'class="article-share-footer"')
        self.assertContains(response, 'Share this project')

        # Social sharing buttons present
        self.assertContains(response, 'class="share-btn share-btn-facebook"')
        self.assertContains(response, 'class="share-btn share-btn-x"')
        self.assertContains(response, 'class="share-btn share-btn-linkedin"')
        self.assertContains(response, 'class="share-btn share-btn-copy"')

        # Accessibility and button labels
        self.assertContains(response, 'aria-label="Share on Facebook"')
        self.assertContains(response, 'aria-label="Share on X (Twitter)"')
        self.assertContains(response, 'aria-label="Share on LinkedIn"')
        self.assertContains(response, 'aria-label="Copy link to clipboard"')
        self.assertContains(response, 'Copy Link')

        # Encoded share targets
        self.assertContains(response, 'facebook.com/sharer/sharer.php')
        self.assertContains(response, 'x.com/intent/tweet')
        self.assertContains(response, 'linkedin.com/sharing/share-offsite')
        self.assertContains(response, self.project_without_cover.slug)



from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

class ProjectImageValidationTests(TestCase):
    def test_invalid_image_extension_raises_validation_error(self):
        invalid_file = SimpleUploadedFile("executable.exe", b"binary", content_type="application/octet-stream")
        project = Project(
            title="Test Project",
            slug="test-project",
            summary="Summary",
            body="Content",
            cover_image=invalid_file,
        )
        with self.assertRaises(ValidationError) as ctx:
            project.full_clean()
        self.assertIn("Unsupported image file extension", str(ctx.exception))

    def test_oversized_image_raises_validation_error(self):
        large_file = SimpleUploadedFile("huge_banner.png", b"0" * (10 * 1024 * 1024 + 1), content_type="image/png")
        project = Project(
            title="Test Project Large Image",
            slug="test-project-large-image",
            summary="Summary",
            body="Content",
            cover_image=large_file,
        )
        with self.assertRaises(ValidationError) as ctx:
            project.full_clean()
        self.assertIn("File size exceeds maximum allowed limit", str(ctx.exception))
