"""Regression tests for the independent, private decision evidence workbench."""
import hashlib
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL = "https://aipmandy.github.io/intj-growth-guide/decision.html"


class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.canonical = []
        self.jsonld = []
        self.active_script = False
        self.buf = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical.append(attrs.get("href"))
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.active_script = True
            self.buf = []

    def handle_data(self, data):
        if self.active_script:
            self.buf.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.active_script:
            self.jsonld.append(json.loads("".join(self.buf)))
            self.active_script = False


class DecisionTests(unittest.TestCase):
    def test_meta_and_accessible_form(self):
        html = (ROOT / "decision.html").read_text(encoding="utf-8")
        p = Tags()
        p.feed(html)
        self.assertEqual(p.canonical, [URL])
        self.assertEqual(len(p.jsonld), 1)
        self.assertEqual(p.jsonld[0]["@type"], "WebApplication")
        self.assertEqual(p.jsonld[0]["author"]["name"], "AI 酋长 Andy")
        self.assertEqual(p.jsonld[0]["publisher"]["url"], "https://www.a6no1.cn/")
        self.assertIn("2026-11-23", html)
        self.assertIn("role=\"status\"", html)
        for name in ["question", "optionA", "optionB", "evidence", "falsifier",
                     "experiment", "criteriaRows", "result", "save", "export", "records"]:
            self.assertIn(name, p.ids)
        self.assertIn('src="decision.js"', html)
        for target in ["https://metaver.vip/", "https://metaver.vip/services",
                       "https://www.a6no1.cn/", "AIPMAndy",
                       "pdf/intj-growth-guide-guide.pdf"]:
            self.assertIn(target, html)

    def test_validation_persistence_and_csv_defenses(self):
        source = (ROOT / "decision.js").read_text(encoding="utf-8")
        for marker in ["Number.isInteger", 'an<0||an>5', 'bn<0||bn>5',
                       'url.protocol==="https:"', "textContent", "localStorage",
                       "confirm(", "URL.createObjectURL", "csvCell", "Math.round"]:
            self.assertIn(marker, source)
        self.assertNotIn("fetch(", source)
        self.assertNotIn("innerHTML", source)
        self.assertIn("30", source)
        self.assertIn(r'[=+\-@]', source)

    def test_home_navigation_and_source_build(self):
        template = (ROOT / "site/template.html").read_text(encoding="utf-8")
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        for html in [template, home]:
            self.assertIn('href="decision.html"', html)
            self.assertIn('href="pdf/intj-growth-guide-guide.pdf"', html)
            self.assertIn('https://www.a6no1.cn/', html)

    def test_sitemap_and_historical_pdf_integrity(self):
        self.assertIn(URL, (ROOT / "sitemap.xml").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / "pdf/edition.json").read_text(encoding="utf-8"))
        pdf = (ROOT / manifest["pdf_path"]).read_bytes()
        self.assertEqual(len(pdf), manifest["bytes"])
        self.assertEqual(hashlib.sha256(pdf).hexdigest(), manifest["sha256"])
        self.assertEqual(manifest["pages"], 45)


if __name__ == "__main__":
    unittest.main()
