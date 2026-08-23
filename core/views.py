from django.conf import settings
from django.urls import reverse
from django.shortcuts import render

from blog.models import Post
from portfolio.models import Project


def home(request):
    featured_projects = Project.objects.filter(is_featured=True).prefetch_related('tags')[:3]
    if not featured_projects:
        featured_projects = Project.objects.all().prefetch_related('tags')[:3]
    return render(request, 'core/home.html', {'featured_projects': featured_projects})


def robots_txt(request):
    return render(request, 'robots.txt', {'site_url': settings.PUBLIC_SITE_URL}, content_type='text/plain')


def sitemap_xml(request):
    items = [
        {'loc': request.build_absolute_uri('/'), 'lastmod': None},
        {'loc': request.build_absolute_uri('/services/'), 'lastmod': None},
        {'loc': request.build_absolute_uri('/about/'), 'lastmod': None},
        {'loc': request.build_absolute_uri('/portfolio/'), 'lastmod': None},
        {'loc': request.build_absolute_uri('/blog/'), 'lastmod': None},
    ]

    for project in Project.objects.all():
        items.append({'loc': request.build_absolute_uri(project.get_absolute_url()), 'lastmod': project.created.date()})

    for post in Post.published.all():
        items.append({'loc': request.build_absolute_uri(post.get_absolute_url()), 'lastmod': post.published_at.date() if post.published_at else post.created.date()})

    return render(request, 'sitemap.xml', {'items': items}, content_type='application/xml')


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


def server_error(request):
    return render(request, '500.html', status=500)
