from django.shortcuts import render

from .models import Project, Tag


def project_list(request):
    selected_tag = request.GET.get('tag')
    tags = Tag.objects.order_by('name')
    projects = Project.objects.all().prefetch_related('tags')

    if selected_tag:
        projects = projects.filter(tags__slug=selected_tag).distinct()

    if request.headers.get('Hx-Request') == 'true':
        template_name = 'portfolio/partials/project_grid.html'
    else:
        template_name = 'portfolio/project_list.html'

    context = {
        'projects': projects,
        'tags': tags,
        'selected_tag': selected_tag,
    }
    return render(request, template_name, context)


def project_detail(request, slug):
    project = Project.objects.prefetch_related('tags').get(slug=slug)
    return render(request, 'portfolio/project_detail.html', {'project': project})
