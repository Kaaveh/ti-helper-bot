from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from telegram import User

_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
_SUPPORTED_LANGS = {"en", "fa"}
_DEFAULT_LANG = "en"
_FALLBACK_NAMES = {"en": "there", "fa": "دوست عزیز"}


def _detect_language(user: "User") -> str:
    code = (user.language_code or "").lower()
    primary = code.split("-")[0]
    if primary in _SUPPORTED_LANGS:
        return primary
    return _DEFAULT_LANG


def render_welcome(user: "User") -> str:
    lang = _detect_language(user)
    path = _TEMPLATES_DIR / f"welcome_{lang}.txt"
    if not path.exists():
        path = _TEMPLATES_DIR / f"welcome_{_DEFAULT_LANG}.txt"
    template = path.read_text(encoding="utf-8")
    name = (user.first_name or "").strip() or _FALLBACK_NAMES.get(lang, _FALLBACK_NAMES[_DEFAULT_LANG])
    return template.format(first_name=name)
