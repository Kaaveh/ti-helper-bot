import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

# Moderation settings
SPAM_WARN_THRESHOLD = 0.6
SPAM_MUTE_THRESHOLD = 0.8
SPAM_BAN_THRESHOLD = 0.95
MAX_WARNINGS = 2
