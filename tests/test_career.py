import json
import unittest
from pathlib import Path

R = Path(__file__).resolve().parents[1]
C = R / "career"
TRACKS = {"市场定位", "业绩证明", "沟通影响", "晋升带队", "组织博弈", "谈薪跳槽"}
KINDS = {"film": 18, "series": 12, "book": 18}

class CareerGuideTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((C / "data/catalog.json").read_text(encoding="utf-8"))

    def test_count_and_unique_ids(self):
        self.assertEqual(len(self.data), 48)
        self.assertEqual(len({x["id"] for x in self.data}), 48)

    def test_category_counts(self):
        for kind, expected in KINDS.items():
            self.assertEqual(sum(x["kind"] == kind for x in self.data), expected)
        for track in TRACKS:
            self.assertEqual(sum(x["track"] == track for x in self.data), 8)

    def test_required_fields(self):
        for item in self.data:
            for field in ("id", "kind", "title", "original", "track", "why", "principle", "action", "trap"):
                self.assertTrue(str(item.get(field, "")).strip(), (item.get("id"), field))
            self.assertIn(item["track"], TRACKS)
            self.assertIn(item["kind"], KINDS)

    def test_site_assets(self):
        html = (C / "index.html").read_text(encoding="utf-8")
        self.assertIn('<html lang="zh-CN">', html)
        self.assertIn('src="app.js"', html)
        self.assertIn('href="style.css"', html)
        self.assertIn('id="cards"', html)
        for asset in ("style.css", "app.js", "assets/social-preview.svg", "README.md",
                      "guides/7-day.md", "guides/30-day.md", "templates/promotion-case.md",
                      "templates/salary-negotiation.md", "templates/weekly-review.md",
                      "docs/SOURCES.md", "CONTRIBUTING.md"):
            self.assertTrue((C / asset).is_file(), asset)

    def test_recommendations_have_executable_actions(self):
        for item in self.data:
            self.assertGreaterEqual(len(item["action"]), 18, item["id"])
            self.assertGreaterEqual(len(item["trap"]), 10, item["id"])

if __name__ == "__main__":
    unittest.main()
