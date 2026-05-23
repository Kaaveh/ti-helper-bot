import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from handlers.admin_commands import _is_admin  # noqa: E402
from services.help import render_help  # noqa: E402


def _user(language_code):
    return SimpleNamespace(language_code=language_code, first_name="Ali")


class RenderHelpTests(unittest.TestCase):
    def test_member_english(self):
        msg = render_help(_user("en"), is_admin=False)
        self.assertIn("Tech Immigrants Helper Bot", msg)
        self.assertIn("pinned rules", msg)
        self.assertIn("/start", msg)
        self.assertIn("/help", msg)
        self.assertNotIn("/stats", msg)
        self.assertNotIn("/approve_all", msg)

    def test_member_farsi(self):
        msg = render_help(_user("fa"), is_admin=False)
        self.assertIn("Tech Immigrants", msg)
        self.assertIn("قوانین پین‌شده", msg)
        self.assertIn("/start", msg)
        self.assertIn("/help", msg)
        self.assertNotIn("/stats", msg)
        self.assertNotIn("/approve_all", msg)
        self.assertNotIn("Welcome", msg)

    def test_admin_english(self):
        msg = render_help(_user("en-US"), is_admin=True)
        for command in ("/start", "/help", "/stats", "/approve_all"):
            self.assertIn(command, msg)
        self.assertIn("Admin commands", msg)

    def test_admin_farsi(self):
        msg = render_help(_user("fa"), is_admin=True)
        for command in ("/start", "/help", "/stats", "/approve_all"):
            self.assertIn(command, msg)
        self.assertIn("دستورات ادمین", msg)
        self.assertNotIn("Admin commands", msg)

    def test_unsupported_language_falls_back_to_en(self):
        msg = render_help(_user("de"), is_admin=False)
        self.assertIn("Tech Immigrants Helper Bot", msg)
        self.assertIn("pinned rules", msg)

    def test_missing_language_code_falls_back_to_en(self):
        msg = render_help(_user(None), is_admin=True)
        self.assertIn("Admin commands", msg)


class IsAdminTests(unittest.TestCase):
    def test_group_admin_is_admin(self):
        self.assertTrue(_is_admin("supergroup", "administrator"))
        self.assertTrue(_is_admin("group", "creator"))

    def test_group_member_is_not_admin(self):
        self.assertFalse(_is_admin("supergroup", "member"))

    def test_private_chat_is_never_admin(self):
        self.assertFalse(_is_admin("private", "creator"))
        self.assertFalse(_is_admin("private", "administrator"))


if __name__ == "__main__":
    unittest.main()
