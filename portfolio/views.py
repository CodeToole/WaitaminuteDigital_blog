from django.shortcuts import get_object_or_404, render

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
    # Use get_object_or_404 to fail securely with a 404 instead of raising
    # unhandled Project.DoesNotExist 500 errors on invalid project slugs.
    project = get_object_or_404(Project.objects.prefetch_related('tags'), slug=slug)
    return render(request, 'portfolio/project_detail.html', {'project': project})
