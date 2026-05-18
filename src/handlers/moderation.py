import logging
from telegram import Update
from telegram.ext import ContextTypes
from services.spam_checker import assess_message
from config import MAX_WARNINGS

logger = logging.getLogger(__name__)

# In-memory warning tracker (replace with DB in production)
_warnings: dict[int, int] = {}


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if not message or not message.text:
        return

    user = update.effective_user
    chat = update.effective_chat

    assessment = await assess_message(message.text, user)

    if not assessment["is_spam"]:
        return

    user_id = user.id
    _warnings[user_id] = _warnings.get(user_id, 0) + 1
    count = _warnings[user_id]

    if count > MAX_WARNINGS:
        await chat.ban_member(user_id)
        await message.delete()
        logger.info(f"Banned user {user_id} (@{user.username}) — exceeded warning limit")
    elif count == MAX_WARNINGS:
        await message.delete()
        await chat.restrict_member(user_id, permissions=_muted_permissions())
        await message.reply_text(
            f"⚠️ @{user.username} has been muted for repeated self-promotion. "
            f"Next violation results in a ban."
        )
        logger.info(f"Muted user {user_id} (@{user.username}) — warning {count}")
    else:
        await message.delete()
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=(
                    f"Your message in Tech Immigrants was removed because it looked like "
                    f"self-promotion/advertising.\n\n"
                    f"Reason: {assessment['reason']}\n\n"
                    f"Warning {count}/{MAX_WARNINGS}. Please review the group rules."
                ),
            )
        except Exception:
            pass
        logger.info(f"Warned user {user_id} (@{user.username}) — warning {count}/{MAX_WARNINGS}")


def _muted_permissions():
    from telegram import ChatPermissions

    return ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_other_messages=False,
    )
