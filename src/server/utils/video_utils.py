from ensure import ensure_annotations # This is a decorator that checks whether function arguments match their type hints.
from urllib.parse import urlparse, parse_qs

@ensure_annotations
def extract_video_id(url) -> str :
    parsed_url = urlparse(url)

    # Standard URL
    if parsed_url.hostname in ("www.youtube.com", "youtube.com"):
        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query).get("v", [None])[0]

        # Shorts URL
        elif parsed_url.path.startswith("/shorts/"):
            return parsed_url.path.split("/")[2]

        # Embed URL
        elif parsed_url.path.startswith("/embed/"):
            return parsed_url.path.split("/")[2]

    # Short URL
    elif parsed_url.hostname == "youtu.be":
        return parsed_url.path.lstrip("/")
