from django.db import models
from django.urls import reverse

from core.utils import extract_youtube_id, get_youtube_embed_url, get_youtube_thumbnail_url


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
    cover_image = models.ImageField(upload_to='projects/', blank=True, null=True)
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
