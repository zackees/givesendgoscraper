"""
Tests the scraper module.
"""

import unittest

from givesendgoscraper.scraper import scrape_givesendgo

class GenerateFilesTester(unittest.TestCase):
    """Tester for the server."""

    def test_scraper(self) -> None:
        """Tests that the files can be created ok."""
        data = scrape_givesendgo("maryamhenein")
        self.assertIn("goal", data)
        self.assertIn("raised", data)

if __name__ == "__main__":
    unittest.main()