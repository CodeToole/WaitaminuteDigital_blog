import re


def extract_youtube_id(url: str) -> str | None:
    """
    Extract YouTube video ID from various URL formats:
    - https://youtu.be/EeGCxH_0zx4?si=...
    - https://www.youtube.com/watch?v=EeGCxH_0zx4
    - https://www.youtube.com/embed/EeGCxH_0zx4
    - https://www.youtube.com/shorts/EeGCxH_0zx4
    - EeGCxH_0zx4 (raw 11-char ID)
    """
    if not url:
        return None

    url = url.strip()

    # If it's already an 11-char video ID
    if re.fullmatch(r'[a-zA-Z0-9_-]{11}', url):
        return url

    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?(?:.*&)?v=([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/shorts\/([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([a-zA-Z0-9_-]{11})',
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def get_youtube_thumbnail_url(video_id: str | None) -> str | None:
    if not video_id:
        return None
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"


def get_youtube_embed_url(video_id: str | None) -> str | None:
    if not video_id:
        return None
    return f"https://www.youtube.com/embed/{video_id}"
