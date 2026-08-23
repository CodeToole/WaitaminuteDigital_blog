from django.db.models import Q
from django.shortcuts import get_object_or_404, render

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
    post = get_object_or_404(Post.published, slug=slug)
    post_url = request.build_absolute_uri(post.get_absolute_url())
    share_urls = post.get_share_urls(request)
    share_image_url = post.get_share_image_url(request)
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'post_url': post_url,
        'share_urls': share_urls,
        'share_image_url': share_image_url,
    })

