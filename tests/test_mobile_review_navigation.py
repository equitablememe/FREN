"""Static safety regression for FREN's explicitly user-controlled Resolucent return route."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MobileReturnRoute(unittest.TestCase):
    def test_return_to_resolucent_uses_same_tab_and_no_referrer(self):
        html = (ROOT / "mobile" / "index.html").read_text()
        matches = re.findall(r'<a class="resolucent-return"([^>]*)>', html)
        self.assertEqual(len(matches), 1)
        attrs = matches[0]
        self.assertIn('href="https://www.resolucent.com/#fren-handoff"', attrs)
        self.assertNotIn('target="_blank"', attrs)
        self.assertIn('rel="noreferrer"', attrs)

    def test_migration_and_no_automatic_upload_disclosures(self):
        html = (ROOT / "mobile" / "index.html").read_text()
        readme = (ROOT / "mobile" / "README.md").read_text()
        self.assertIn("Your notebook stays in this browser; it is not automatically uploaded.", html)
        self.assertIn("Notes saved on", html)
        self.assertIn("will not appear automatically", readme)


if __name__ == "__main__":
    unittest.main()
