import os
import requests
import instaloader
from urllib.parse import urlparse
from pyrogram.types import InputMediaPhoto, InputMediaVideo
from config import Config
from .cache import mongo_manager
from .utils import get_clean_filename, is_valid_instagram_url

class InstagramDownloader:
    def __init__(self):
        self.loader = instaloader.Instaloader()
        if Config.INSTAGRAM_USERNAME and Config.INSTAGRAM_PASSWORD:
            try:
                self.loader.login(Config.INSTAGRAM_USERNAME, Config.INSTAGRAM_PASSWORD)
            except Exception as e:
                print(f"Instagram login failed: {e}")

    async def download_media(self, url):
        """Main method to handle Instagram URL and return appropriate media"""
        if not is_valid_instagram_url(url):
            return {"error": "Invalid Instagram URL"}

        try:
            # Check for post type and handle accordingly
            if "/reel/" in url or "/p/" in url:
                return await self._handle_post(url)
            elif "/stories/" in url:
                return await self._handle_story(url)
            else:
                return {"error": "Unsupported Instagram URL type"}
        except Exception as e:
            return {"error": f"Download failed: {str(e)}"}

    async def _handle_post(self, url):
        """Handle Instagram posts (including reels and regular posts)"""
        try:
            post = instaloader.Post.from_shortcode(self.loader.context, self._get_shortcode(url))
            media_list = []

            # Handle single media posts
            if not post.is_video and not post.typename == "GraphSidecar":
                photo_url = post.url
                filename = f"media/{get_clean_filename(post.owner_username)}_{post.shortcode}.jpg"
                media_list.append({
                    "type": "photo",
                    "media": photo_url,
                    "caption": self._get_caption(post),
                    "filename": filename
                })
            elif post.is_video:
                video_url = post.video_url
                filename = f"media/{get_clean_filename(post.owner_username)}_{post.shortcode}.mp4"
                media_list.append({
                    "type": "video",
                    "media": video_url,
                    "caption": self._get_caption(post),
                    "filename": filename,
                    "thumbnail": post.url if post.url else None
                })
            else:
                # Handle carousel posts
                for index, node in enumerate(post.get_sidecar_nodes()):
                    if node.is_video:
                        media_url = node.video_url
                        ext = "mp4"
                    else:
                        media_url = node.display_url
                        ext = "jpg"

                    filename = f"media/{get_clean_filename(post.owner_username)}_{post.shortcode}_{index}.{ext}"
                    media_list.append({
                        "type": "video" if node.is_video else "photo",
                        "media": media_url,
                        "caption": self._get_caption(post) if index == 0 else None,
                        "filename": filename,
                        "thumbnail": node.display_url if node.is_video else None
                    })

            return {
                "type": "media_group" if len(media_list) > 1 else "single",
                "media": media_list,
                "source_url": url
            }
        except Exception as e:
            return {"error": f"Post download failed: {str(e)}"}

    async def _handle_story(self, url):
        """Handle Instagram stories"""
        try:
            story = instaloader.StoryItem.from_shortcode(self.loader.context, self._get_shortcode(url))
            
            if story.is_video:
                media_url = story.video_url
                filename = f"media/story_{story.owner_username}_{story.shortcode}.mp4"
                return {
                    "type": "single",
                    "media": [{
                        "type": "video",
                        "media": media_url,
                        "caption": None,
                        "filename": filename,
                        "thumbnail": story.url if story.url else None
                    }],
                    "source_url": url
                }
            else:
                media_url = story.url
                filename = f"media/story_{story.owner_username}_{story.shortcode}.jpg"
                return {
                    "type": "single",
                    "media": [{
                        "type": "photo",
                        "media": media_url,
                        "caption": None,
                        "filename": filename
                    }],
                    "source_url": url
                }
        except Exception as e:
            return {"error": f"Story download failed: {str(e)}"}

    def _get_shortcode(self, url):
        """Extract shortcode from Instagram URL"""
        parsed = urlparse(url)
        if not parsed.path:
            return None
        return parsed.path.strip("/").split("/")[-1]

    def _get_caption(self, post):
        """Generate caption for the post"""
        caption = ""
        if post.caption:
            caption = post.caption
        caption += f"\n\n📥 Downloaded via @{Config.BOT_USERNAME}"
        return caption

# Initialize downloader instance
downloader = InstagramDownloader()

async def download_instagram_media(url):
    """Public interface for downloading Instagram media"""
    # Check cache first
    cached = await mongo_manager.get_cache(url)
    if cached:
        return cached

    # Download fresh content
    result = await downloader.download_media(url)
    
    # Cache the result if successful
    if "error" not in result:
        await mongo_manager.set_cache(url, result, expire=3600)  # Cache for 1 hour
    
    return result
