from django.db.models import Q
from django.shortcuts import render

from .models import Post


def post_list(request):
    query = request.GET.get('q', '').strip()
    posts = Post.published.all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query)
            | Q(excerpt__icontains=query)
            | Q(body__icontains=query)
        )

    if request.headers.get('Hx-Request') == 'true':
        template_name = 'blog/partials/post_list.html'
    else:
        template_name = 'blog/post_list.html'

    return render(request, template_name, {'posts': posts, 'query': query})


def post_detail(request, slug):
    post = Post.published.get(slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})
