from django import template
from blog.utils import (
    get_facebook_share_url,
    get_twitter_share_url,
    get_x_share_url,
    get_linkedin_share_url,
    get_share_urls,
)

register = template.Library()


def _resolve_post_url(post_or_url, request=None):
    if hasattr(post_or_url, 'get_absolute_url'):
        relative_url = post_or_url.get_absolute_url()
        if request:
            return request.build_absolute_uri(relative_url)
        return relative_url
    return str(post_or_url)


def _resolve_title(post_or_url):
    if hasattr(post_or_url, 'title'):
        return post_or_url.title
    return ""


@register.filter
def facebook_share_url(post_or_url, request=None):
    url = _resolve_post_url(post_or_url, request)
    return get_facebook_share_url(url)


@register.filter
def twitter_share_url(post_or_url, request=None):
    url = _resolve_post_url(post_or_url, request)
    title = _resolve_title(post_or_url)
    return get_twitter_share_url(url, text=title)


@register.filter
def x_share_url(post_or_url, request=None):
    url = _resolve_post_url(post_or_url, request)
    title = _resolve_title(post_or_url)
    return get_x_share_url(url, text=title)


@register.filter
def linkedin_share_url(post_or_url, request=None):
    url = _resolve_post_url(post_or_url, request)
    title = _resolve_title(post_or_url)
    summary = getattr(post_or_url, 'excerpt', '')
    return get_linkedin_share_url(url, title=title, summary=summary)


@register.filter
def share_image_url(post, request=None):
    if hasattr(post, 'get_share_image_url'):
        return post.get_share_image_url(request)
    return ""


@register.inclusion_tag('blog/partials/share_buttons.html', takes_context=True)
def share_buttons(context, post=None, layout='horizontal'):
    request = context.get('request')
    if post is None:
        post = context.get('post')

    post_url = ""
    share_urls = {}
    if post:
        if request:
            post_url = request.build_absolute_uri(post.get_absolute_url())
        else:
            post_url = post.get_absolute_url()
        share_urls = post.get_share_urls(request)

    return {
        'post': post,
        'post_url': post_url,
        'share_urls': share_urls,
        'layout': layout,
        'request': request,
    }
