import logging
from telegram import Update
from telegram.ext import (
    Application,
    ChatJoinRequestHandler,
    MessageHandler,
    CommandHandler,
    filters,
)
from config import TELEGRAM_BOT_TOKEN
from handlers.join_requests import handle_join_request
from handlers.moderation import handle_message
from handlers.admin_commands import start, stats, approve_all, help_command

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("approve_all", approve_all))

    app.add_handler(ChatJoinRequestHandler(handle_join_request))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    logger.info("TIHelperBot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
