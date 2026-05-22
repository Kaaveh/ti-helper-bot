import logging
from telegram import Update
from telegram.ext import ContextTypes
from services.spam_checker import assess_user
from services.welcome import render_welcome

logger = logging.getLogger(__name__)


async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    request = update.chat_join_request
    user = request.from_user

    assessment = await assess_user(user)

    if assessment["approved"]:
        await request.approve()
        logger.info(f"Auto-approved user {user.id} (@{user.username}) — score: {assessment['score']:.2f}")

        try:
            await context.bot.send_message(
                chat_id=user.id,
                text=render_welcome(user),
            )
        except Exception as exc:
            logger.warning(
                f"Failed to DM welcome to user {user.id} (@{user.username}): {exc}"
            )
    else:
        await request.decline()
        logger.info(
            f"Declined user {user.id} (@{user.username}) — "
            f"score: {assessment['score']:.2f}, reason: {assessment['reason']}"
        )
