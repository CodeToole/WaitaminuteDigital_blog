import urllib.parse
from django.urls import reverse


def get_facebook_share_url(url: str) -> str:
    """Generate Facebook share URL."""
    return f"https://www.facebook.com/sharer/sharer.php?{urllib.parse.urlencode({'u': url})}"


def get_twitter_share_url(url: str, text: str = "") -> str:
    """Generate X (Twitter) intent tweet URL."""
    params = {'url': url}
    if text:
        params['text'] = text
    return f"https://x.com/intent/tweet?{urllib.parse.urlencode(params)}"


def get_x_share_url(url: str, text: str = "") -> str:
    """Alias for get_twitter_share_url."""
    return get_twitter_share_url(url, text=text)


def get_linkedin_share_url(url: str, title: str = "", summary: str = "") -> str:
    """Generate LinkedIn share URL using modern offsite sharing endpoint."""
    params = {'url': url}
    return f"https://www.linkedin.com/sharing/share-offsite/?{urllib.parse.urlencode(params)}"


def get_share_urls(url: str, title: str = "", summary: str = "") -> dict:
    """Generate a dictionary containing sharing URLs for all supported platforms."""
    return {
        'facebook': get_facebook_share_url(url),
        'twitter': get_twitter_share_url(url, text=title),
        'x': get_x_share_url(url, text=title),
        'linkedin': get_linkedin_share_url(url, title=title, summary=summary),
    }
