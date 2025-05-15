from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from .cache import mongo_manager
from .downloader import download_instagram_media

app = Client(
    "instagram_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    await mongo_manager.add_user(user_id)
    await message.reply_text("Hello! Send me an Instagram link to download content.")

@app.on_message(filters.text & filters.private)
async def handle_message(client: Client, message: Message):
    url = message.text
    if "instagram.com" in url:
        # Check cache first
        cached_content = await mongo_manager.get_cache(url)
        if cached_content:
            await message.reply_cached_content(cached_content)
            return
            
        # Download and cache
        content = await download_instagram_media(url)
        await mongo_manager.set_cache(url, content, expire=3600)  # Cache for 1 hour
        await message.reply_content(content)
    else:
        await message.reply_text("Please send a valid Instagram URL.")
