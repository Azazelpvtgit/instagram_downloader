import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram Bot Token
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    
    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "instagram_bot")
    
    # Instagram API Configuration (if used)
    INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME", "")
    INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "")
    
    # Other configurations
    SESSION_STRING = os.getenv("SESSION_STRING", "")
    WORKERS = int(os.getenv("WORKERS", "24"))
    GROUP_ID = os.getenv("GROUP_ID", "")
