import pathlib
import unittest


class RequirementsTest(unittest.TestCase):
    def test_resemblyzer_is_not_required_for_default_install(self) -> None:
        requirements = pathlib.Path("requirements.txt").read_text(encoding="utf-8")
        packages = [
            line.strip()
            for line in requirements.splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        self.assertNotIn("resemblyzer", packages)


if __name__ == "__main__":
    unittest.main()
