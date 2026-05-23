from telegram import Update
from telegram.ext import ContextTypes

_GROUP_CHAT_TYPES = ("group", "supergroup")

MEMBER_HELP = (
    "👋 Hi! I'm the Tech Immigrants Helper Bot.\n\n"
    "I handle join approvals, moderate spam, and keep the community healthy.\n\n"
    "Available commands:\n"
    "/start — Show the bot intro\n"
    "/help — Show this help message\n\n"
    "Please review the pinned rules to keep our space helpful for everyone."
)

ADMIN_HELP = (
    "👋 Hi! I'm the Tech Immigrants Helper Bot.\n\n"
    "I handle join approvals, moderate spam, and keep the community healthy.\n\n"
    "Member commands:\n"
    "/start — Show the bot intro\n"
    "/help — Show this help message\n\n"
    "Admin commands:\n"
    "/stats — Community stats overview\n"
    "/approve_all — Approve all pending join requests"
)


def _select_help(chat_type: str, member_status: str) -> str:
    if chat_type in _GROUP_CHAT_TYPES and member_status in ("administrator", "creator"):
        return ADMIN_HELP
    return MEMBER_HELP


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Hi! I'm the Tech Immigrants Helper Bot.\n\n"
        "I handle join approvals, moderate spam, and keep the community healthy.\n\n"
        "Admin commands:\n"
        "/stats — Community stats overview\n"
        "/approve_all — Approve all pending join requests"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    member_status = ""
    if chat.type in _GROUP_CHAT_TYPES:
        member = await chat.get_member(update.effective_user.id)
        member_status = member.status

    await update.message.reply_text(_select_help(chat.type, member_status))


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO: Pull from database in Phase 2
    await update.message.reply_text(
        "📊 Stats (coming in Phase 2)\n\n"
        "• Members approved today: —\n"
        "• Spam blocked today: —\n"
        "• Trending topics: —"
    )


async def approve_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    member = await chat.get_member(update.effective_user.id)

    if member.status not in ("administrator", "creator"):
        await update.message.reply_text("⛔ Admin only.")
        return

    await update.message.reply_text("✅ Approving all pending requests...")
    # Note: Bot API doesn't have a "list pending requests" endpoint.
    # This would need to be tracked in DB from incoming ChatJoinRequest events.
