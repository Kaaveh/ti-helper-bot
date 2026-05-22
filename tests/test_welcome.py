import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from services.welcome import render_welcome  # noqa: E402


def _user(language_code, first_name="Ali"):
    return SimpleNamespace(language_code=language_code, first_name=first_name)


class RenderWelcomeTests(unittest.TestCase):
    def test_farsi_uses_fa_template(self):
        msg = render_welcome(_user("fa"))
        self.assertIn("Ali", msg)
        self.assertIn("Tech Immigrants", msg)
        self.assertNotIn("Welcome", msg)

    def test_regional_english_tag_maps_to_en(self):
        msg = render_welcome(_user("en-US", first_name="Sara"))
        self.assertIn("Welcome to Tech Immigrants, Sara", msg)

    def test_underscore_separator_in_language_code(self):
        msg = render_welcome(_user("en_US", first_name="Sara"))
        self.assertIn("Welcome to Tech Immigrants, Sara", msg)

    def test_missing_language_code_falls_back_to_en(self):
        msg = render_welcome(_user(None, first_name="X"))
        self.assertIn("Welcome to Tech Immigrants, X", msg)

    def test_unsupported_language_falls_back_to_en(self):
        msg = render_welcome(_user("de", first_name="Hans"))
        self.assertIn("Welcome to Tech Immigrants, Hans", msg)

    def test_empty_first_name_uses_en_fallback(self):
        msg = render_welcome(_user(None, first_name=""))
        self.assertIn("Welcome to Tech Immigrants, there", msg)
        self.assertNotIn(", !", msg)

    def test_whitespace_first_name_uses_en_fallback(self):
        msg = render_welcome(_user("en", first_name="   "))
        self.assertIn("Welcome to Tech Immigrants, there", msg)

    def test_empty_first_name_uses_fa_fallback(self):
        msg = render_welcome(_user("fa", first_name=""))
        self.assertIn("دوست عزیز", msg)
        self.assertNotIn("، !", msg)


if __name__ == "__main__":
    unittest.main()
