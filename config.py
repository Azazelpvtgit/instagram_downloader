import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram Bot Token class Config:
    # Telegram API (GET THESE FROM https://my.telegram.org/apps)
    API_ID = os.getenv("API_ID", 21505404)  # Replace with your API ID
    API_HASH = os.getenv("API_HASH", "5feffdf4111ed339381056d9476d3fcd")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7804111155:AAFVqQ8msydHOb27yJuzMbtFpaUZOAUSSFs")  # Your bot token from @BotFather
    
    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://moviesdronn:S1KVbSSoWFsu2rfE@cluster0.6airt3d.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "instagram_bot")
    
    # Instagram API Configuration (if used)
    INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME", "")
    INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "")
    
    # Other configurations
    SESSION_STRING = os.getenv("SESSION_STRING", "")
    WORKERS = int(os.getenv("WORKERS", "24"))
    GROUP_ID = os.getenv("GROUP_ID", "-1002342115206")
