from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from telegram import User

_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
_SUPPORTED_LANGS = {"en", "fa"}
_DEFAULT_LANG = "en"


def _detect_language(user: "User") -> str:
    code = (getattr(user, "language_code", None) or "").lower().replace("_", "-")
    primary = code.split("-")[0]
    if primary in _SUPPORTED_LANGS:
        return primary
    return _DEFAULT_LANG


@lru_cache(maxsize=None)
def _load_template(lang: str, audience: str) -> str:
    path = _TEMPLATES_DIR / f"help_{audience}_{lang}.txt"
    if not path.exists():
        path = _TEMPLATES_DIR / f"help_{audience}_{_DEFAULT_LANG}.txt"
    return path.read_text(encoding="utf-8")


def render_help(user: "User", is_admin: bool) -> str:
    lang = _detect_language(user)
    audience = "admin" if is_admin else "member"
    return _load_template(lang, audience)
