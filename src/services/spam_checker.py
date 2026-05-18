import re
from telegram import User
from config import ANTHROPIC_API_KEY

# Heuristic signals for spam accounts
_SPAM_BIO_PATTERNS = [
    r"(crypto|forex|trading|invest|earn|profit|income)",
    r"(DM me|message me|contact me)",
    r"(100%|guaranteed|free money)",
    r"(t\.me/|bit\.ly/|linktr\.ee/)",
]

_SPAM_MSG_PATTERNS = [
    r"(DM me|send me a message|contact me)",
    r"(join my|check out my|visit my)",
    r"(crypto|forex|trading signals|investment)",
    r"(earn \$|make \$|passive income)",
    r"(limited spots|act now|don't miss)",
    r"(t\.me/|bit\.ly/|linktr\.ee/|wa\.me/)",
]


async def assess_user(user: User) -> dict:
    """Assess whether a join request should be approved.

    Returns dict with: approved (bool), score (float 0-1), reason (str),
    and optionally welcome_message.
    """
    score = 0.0
    reasons = []

    if not user.username:
        score += 0.2
        reasons.append("no username")

    if not user.first_name or len(user.first_name.strip()) < 2:
        score += 0.2
        reasons.append("missing/short name")

    # Check if the user has a profile photo (not available via join request,
    # but we can try via bot API)
    # For now, rely on other signals

    if user.is_bot:
        score += 0.9
        reasons.append("is a bot")

    # If we have AI available, do a deeper check
    if ANTHROPIC_API_KEY and score < 0.5:
        ai_result = await _ai_assess_user(user)
        if ai_result:
            score = max(score, ai_result["score"])
            if ai_result.get("reason"):
                reasons.append(ai_result["reason"])

    approved = score < 0.5

    return {
        "approved": approved,
        "score": score,
        "reason": "; ".join(reasons) if reasons else "passed checks",
    }


async def assess_message(text: str, user: User) -> dict:
    """Assess whether a message is spam/self-promotion.

    Returns dict with: is_spam (bool), score (float 0-1), reason (str).
    """
    score = 0.0
    reasons = []

    text_lower = text.lower()

    for pattern in _SPAM_MSG_PATTERNS:
        if re.search(pattern, text_lower):
            score += 0.3
            reasons.append(f"matched: {pattern}")

    url_count = len(re.findall(r"https?://", text))
    if url_count >= 3:
        score += 0.3
        reasons.append(f"{url_count} URLs")

    if len(text) > 500 and url_count >= 2:
        score += 0.2
        reasons.append("long message with multiple links")

    score = min(score, 1.0)

    # AI assessment for borderline cases
    if ANTHROPIC_API_KEY and 0.3 <= score <= 0.7:
        ai_result = await _ai_assess_message(text)
        if ai_result:
            score = (score + ai_result["score"]) / 2
            if ai_result.get("reason"):
                reasons.append(ai_result["reason"])

    return {
        "is_spam": score >= 0.5,
        "score": score,
        "reason": "; ".join(reasons) if reasons else "clean",
    }


async def _ai_assess_user(user: User) -> dict | None:
    """Use Claude to assess a user profile for spam signals."""
    try:
        import anthropic

        client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
        response = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=150,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Assess this Telegram user wanting to join a tech professionals community. "
                        f"Is this likely a real person or spam/scam?\n\n"
                        f"Name: {user.first_name} {user.last_name or ''}\n"
                        f"Username: @{user.username or 'none'}\n"
                        f"Is bot: {user.is_bot}\n\n"
                        f"Reply with JSON only: {{\"score\": 0.0-1.0, \"reason\": \"brief reason\"}}\n"
                        f"Score 0 = definitely real, 1 = definitely spam."
                    ),
                }
            ],
        )
        import json

        return json.loads(response.content[0].text)
    except Exception:
        return None


async def _ai_assess_message(text: str) -> dict | None:
    """Use Claude to assess if a message is self-promotion."""
    try:
        import anthropic

        client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
        response = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=150,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Is this message in a tech community group self-promotion or spam? "
                        f"Legitimate sharing of resources/experiences is OK. "
                        f"Advertising services, recruiting clients, or MLM is not.\n\n"
                        f"Message: {text[:500]}\n\n"
                        f"Reply with JSON only: {{\"score\": 0.0-1.0, \"reason\": \"brief reason\"}}\n"
                        f"Score 0 = legitimate, 1 = clear spam/promo."
                    ),
                }
            ],
        )
        import json

        return json.loads(response.content[0].text)
    except Exception:
        return None
