"""Catalog data checks: schema, distribution, text quality and generated page contract."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KINDS = {"series": 10, "film": 12, "book": 15, "doc": 4}
THEMES = {"决策判断", "系统思维", "职业与商业", "沟通与关系", "情绪与自洽", "执行与成长"}
LEVELS = {"入门", "进阶"}
REQUIRED = ("id", "kind", "title", "original", "year", "creator", "theme", "level", "reason", "takeaway", "action", "pitfall")
TEXT_BOUNDS = {"reason": (15, 80), "takeaway": (12, 80), "action": (15, 80), "pitfall": (10, 80)}


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))

    def test_count(self) -> None:
        self.assertEqual(len(self.data), 41)
        self.assertEqual({kind: sum(i["kind"] == kind for i in self.data) for kind in KINDS}, KINDS)

    def test_unique_ids_and_titles(self) -> None:
        ids = [item["id"] for item in self.data]
        self.assertEqual(len(ids), len(set(ids)))
        titles = [item["title"] for item in self.data]
        self.assertEqual(len(titles), len(set(titles)))
        originals = [item["original"] for item in self.data]
        self.assertEqual(len(originals), len(set(originals)))

    def test_required_fields(self) -> None:
        for item in self.data:
            for field in REQUIRED:
                self.assertTrue(str(item.get(field, "")).strip(), f'{item.get("id")}: {field}')

    def test_id_matches_kind(self) -> None:
        for item in self.data:
            self.assertRegex(item["id"], r"^(series|film|book|doc)-[a-z0-9]+(?:-[a-z0-9]+)*$")
            self.assertTrue(item["id"].startswith(item["kind"] + "-"), item["id"])

    def test_enumerations(self) -> None:
        for item in self.data:
            self.assertIn(item["kind"], KINDS, item["id"])
            self.assertIn(item["theme"], THEMES, item["id"])
            self.assertIn(item["level"], LEVELS, item["id"])

    def test_years_are_plausible(self) -> None:
        for item in self.data:
            self.assertIsInstance(item["year"], int, item["id"])
            self.assertGreaterEqual(item["year"], 1900, item["id"])
            self.assertLessEqual(item["year"], 2026, item["id"])

    def test_text_lengths(self) -> None:
        for item in self.data:
            for field, (low, high) in TEXT_BOUNDS.items():
                length = len(item[field])
                self.assertTrue(low <= length <= high, f'{item["id"]}: {field} 长度 {length}')

    def test_warning_is_optional_but_short(self) -> None:
        for item in self.data:
            warning = item.get("warning", "")
            self.assertLessEqual(len(warning), 40, item["id"])

    def test_theme_coverage(self) -> None:
        counts = {theme: sum(i["theme"] == theme for i in self.data) for theme in THEMES}
        for theme, count in counts.items():
            self.assertGreaterEqual(count, 4, f"{theme}: {count}")


class GeneratedPageTests(unittest.TestCase):
    def test_pages_exist(self) -> None:
        for name in ("index.html", "plan.html", "article.html"):
            self.assertTrue((ROOT / name).exists(), name)
            self.assertIn("<html", (ROOT / name).read_text(encoding="utf-8"))

    def test_index_embeds_catalog_and_links(self) -> None:
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("metaver.vip", html)
        self.assertIn("AIPMAndy", html)
        self.assertIn('id="catalogData"', html)
        self.assertNotIn("/*__CATALOG__*/", html)

    def test_index_is_reproducible(self) -> None:
        import subprocess
        import sys

        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/build.py"), "--check"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
