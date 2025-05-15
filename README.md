# Instagram Downloader Bot (MongoDB Version)

A Telegram bot that downloads Instagram content (photos, videos, reels) and sends them to users.

## Features

- Downloads Instagram media content
- MongoDB backend for data storage
- User management system
- Content caching system

## Setup

1. Clone this repository
2. Install requirements: `pip install -r requirements.txt`
3. Create a `.env` file based on `.env.example`
4. Run the bot: `python main.py`

## MongoDB Setup

1. Install MongoDB on your server
2. Create a database with the name specified in `.env`
3. The bot will automatically create the necessary collections
