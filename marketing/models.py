from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index

from blog.models import Post
from portfolio.models import Project
from .blocks import PageStreamBlock


class MarketingPage(Page):
    intro = models.CharField(max_length=200, blank=True, help_text='Short intro shown above the page body.')
    body = StreamField(PageStreamBlock(), blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    class Meta:
        abstract = True


class HomePage(MarketingPage):
    template = 'marketing/home_page.html'
    max_count = 1

    parent_page_types = ['wagtailcore.Page']
    subpage_types = ['marketing.ServicesPage', 'marketing.AboutPage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        featured_projects = Project.objects.filter(is_featured=True)[:3]
        if not featured_projects:
            featured_projects = Project.objects.all()[:3]
        context['featured_projects'] = featured_projects
        context['latest_posts'] = Post.published.order_by('-published_at', '-created')[:3]
        return context


class ServicesPage(MarketingPage):
    template = 'marketing/services_page.html'
    max_count = 1
    parent_page_types = ['wagtailcore.Page']
    subpage_types = []


class AboutPage(MarketingPage):
    template = 'marketing/about_page.html'
    max_count = 1
    parent_page_types = ['wagtailcore.Page']
    subpage_types = []
