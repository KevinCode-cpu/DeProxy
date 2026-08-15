import pathlib
import unittest

from src.database import config


class RequirementsTest(unittest.TestCase):
    def test_resemblyzer_is_not_required_for_default_install(self) -> None:
        requirements = pathlib.Path("requirements.txt").read_text(encoding="utf-8")
        packages = [
            line.strip()
            for line in requirements.splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        self.assertNotIn("resemblyzer", packages)

    def test_placeholder_supabase_values_are_rejected(self) -> None:
        self.assertTrue(config._is_placeholder_value("PASTE_YOUR_SUPABASE_PROJECT_URL"))
        self.assertTrue(config._is_placeholder_value("PASTE_YOUR_SUPABASE_SECRET_KEY"))
        self.assertFalse(config._is_placeholder_value("https://project.supabase.co"))
        self.assertFalse(config._is_placeholder_value("sb_secret_abc123"))


if __name__ == "__main__":
    unittest.main()
