import re
from urllib.parse import urlparse

def get_clean_filename(username):
    """Sanitize username for safe filename use"""
    return re.sub(r'[^a-zA-Z0-9_]', '_', username)

def is_valid_instagram_url(url):
    """Validate if URL is a proper Instagram URL"""
    patterns = [
        r'^https?://(www\.)?instagram\.com/p/',
        r'^https?://(www\.)?instagram\.com/reel/',
        r'^https?://(www\.)?instagram\.com/stories/'
    ]
    return any(re.search(pattern, url) for pattern in patterns)

def format_file_size(size_in_bytes):
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} TB"
