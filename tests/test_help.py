import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from handlers.admin_commands import ADMIN_HELP, MEMBER_HELP, _select_help  # noqa: E402


class MemberHelpTests(unittest.TestCase):
    def test_member_help_has_intro_and_rules_pointer(self):
        self.assertIn("Tech Immigrants Helper Bot", MEMBER_HELP)
        self.assertIn("pinned rules", MEMBER_HELP)

    def test_member_help_lists_public_commands(self):
        self.assertIn("/start", MEMBER_HELP)
        self.assertIn("/help", MEMBER_HELP)

    def test_member_help_omits_admin_commands(self):
        self.assertNotIn("/stats", MEMBER_HELP)
        self.assertNotIn("/approve_all", MEMBER_HELP)


class AdminHelpTests(unittest.TestCase):
    def test_admin_help_lists_every_command(self):
        for command in ("/start", "/help", "/stats", "/approve_all"):
            self.assertIn(command, ADMIN_HELP)


class SelectHelpTests(unittest.TestCase):
    def test_group_admin_gets_admin_help(self):
        self.assertIs(_select_help("supergroup", "administrator"), ADMIN_HELP)
        self.assertIs(_select_help("group", "creator"), ADMIN_HELP)

    def test_group_member_gets_member_help(self):
        self.assertIs(_select_help("supergroup", "member"), MEMBER_HELP)

    def test_private_chat_never_returns_admin_help(self):
        self.assertIs(_select_help("private", "creator"), MEMBER_HELP)
        self.assertIs(_select_help("private", "administrator"), MEMBER_HELP)


if __name__ == "__main__":
    unittest.main()
