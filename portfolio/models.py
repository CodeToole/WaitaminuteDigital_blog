from django.db import models
from django.urls import reverse


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
