import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram Bot Token
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7804111155:AAFVqQ8msydHOb27yJuzMbtFpaUZOAUSSFs")
    
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
