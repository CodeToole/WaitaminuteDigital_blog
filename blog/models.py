from django.db import models
from django.urls import reverse

from core.utils import extract_youtube_id, get_youtube_embed_url, get_youtube_thumbnail_url


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class PublishedPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published').select_related('category')


# WAGTAIL SEAM: this plain Django blog model is intentionally the stable v1 foundation.
# In a future Wagtail upgrade, the Post model data can be migrated into Wagtail Page types here.
class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True)
    excerpt = models.TextField(help_text='Short summary shown in card previews.')
    body = models.TextField()
    cover_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    youtube_url = models.URLField(blank=True, help_text='Paste a YouTube video URL (e.g. https://youtu.be/... or https://youtube.com/watch?v=...).')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PublishedPostManager()

    class Meta:
        ordering = ['-published_at', '-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

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
