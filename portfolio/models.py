from django.db import models
from django.urls import reverse

from core.utils import extract_youtube_id, get_youtube_embed_url, get_youtube_thumbnail_url, validate_image_file


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    summary = models.TextField(help_text='Short description for cards and previews.')
    body = models.TextField(help_text='Long-form project details.')
    cover_image = models.ImageField(upload_to='projects/', blank=True, null=True, validators=[validate_image_file])
    youtube_url = models.URLField(blank=True, help_text='Paste a YouTube video URL (e.g. https://youtu.be/... or https://youtube.com/watch?v=...).')
    client = models.CharField(max_length=120, blank=True)
    tags = models.ManyToManyField(Tag, related_name='projects', blank=True)
    url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})

    @property
    def youtube_id(self):
        return extract_youtube_id(self.youtube_url)

    @property
    def youtube_embed_url(self):
        return get_youtube_embed_url(self.youtube_id)

    @property
    def youtube_thumbnail_url(self):
        return get_youtube_thumbnail_url(self.youtube_id)

    @property
    def display_image_url(self):
        if self.cover_image:
            return self.cover_image.url
        if self.youtube_thumbnail_url:
            return self.youtube_thumbnail_url
        return None

    def get_share_image_url(self, request=None):
        """
        Return an absolute URL for Open Graph and Twitter card image previews.
        Falls back to the site logo/banner if no cover image or video thumbnail is set.
        """
        image_url = self.display_image_url
        if not image_url:
            fallback = '/static/img/logo/wmd-logo-full-onblack.png'
            return request.build_absolute_uri(fallback) if request else fallback

        if image_url.startswith(('http://', 'https://')):
            return image_url

        if request:
            return request.build_absolute_uri(image_url)
        return image_url

    def get_share_urls(self, request=None):
        """Return sharing URLs for Facebook, X (Twitter), LinkedIn, etc."""
        from blog.utils import get_share_urls
        url = request.build_absolute_uri(self.get_absolute_url()) if request else self.get_absolute_url()
        return get_share_urls(url=url, title=self.title, summary=self.summary)
