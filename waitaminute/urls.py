"""
URL configuration for waitaminute project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from blog.models import Category, Post
from core import views as core_views
from leads.models import Lead
from portfolio.models import Project


class WMDAdminSite(admin.AdminSite):
    site_title = 'Waitaminute Digital Control Center'
    site_header = 'Waitaminute Digital Control Center'
    index_title = 'Dashboard'
    index_template = 'admin/index.html'

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}

        extra_context.update({
            'portfolio_count': Project.objects.count(),
            'blog_post_count': Post.objects.count(),
            'lead_count': Lead.objects.count(),
            'category_count': Category.objects.count(),
        })
        return super().index(request, extra_context=extra_context)


admin_site = WMDAdminSite(name='admin')

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('core.urls')),
    path('about/', include('marketing.urls')),
    path('services/', include('services.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('blog/', include('blog.urls')),
    path('leads/', include('leads.urls')),
    path('robots.txt', core_views.robots_txt, name='robots_txt'),
    path('sitemap.xml', core_views.sitemap_xml, name='sitemap_xml'),
]

if not settings.MEDIA_URL.startswith('http'):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})]

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
