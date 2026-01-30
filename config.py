import os

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "@skylinefortravel")

# Database
DB_PATH = 'koko_teacher.db'

# Schedule
SCHEDULE = {
    "Spanish": "09:00",
    "French": "19:00",
    "Chinese": "00:00"
}

# Video Settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
BG_COLOR = (20, 20, 20) # Dark background
FONT_SIZE = 60
MAX_LINES_PER_SLIDE = 4

# YouTube API
CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# Instagram Settings (Note: Using Meta Graph API requires access token)
# For simple text posting, we will provide a template or use a placeholder if no token is provided
INSTAGRAM_ACCOUNT_ID = "YOUR_INSTAGRAM_ACCOUNT_ID"
INSTAGRAM_ACCESS_TOKEN = "YOUR_INSTAGRAM_ACCESS_TOKEN"
