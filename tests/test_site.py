"""Site-level checks: metadata, assets, internal links, anchors and discoverability files."""
from __future__ import annotations

import json
import re
import struct
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://aipmandy.github.io/intj-growth-guide"
PAGES = ("index.html", "article.html", "plan.html")
EXTERNAL = ("http://", "https://", "mailto:", "tel:", "javascript:", "data:")


class PageParser(HTMLParser):
    """Minimal parser that collects the pieces the checks care about."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in_title = False
        self.meta: dict[str, str] = {}
        self.links: list[dict[str, str]] = []
        self.anchors: set[str] = set()
        self.refs: list[str] = []
        self.scripts: list[tuple[str, str]] = []
        self._script_type: str | None = None
        self._script_buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        if "id" in data:
            self.anchors.add(data["id"])
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            key = data.get("property") or data.get("name") or data.get("http-equiv")
            if key:
                self.meta[key] = data.get("content", "")
        elif tag == "link":
            self.links.append(data)
        elif tag in ("a", "img", "source"):
            for attr in ("href", "src"):
                if data.get(attr):
                    self.refs.append(data[attr])
        elif tag == "script":
            self._script_type = data.get("type")
            self._script_buf = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        elif tag == "script" and self._script_type is not None:
            self.scripts.append((self._script_type, "".join(self._script_buf)))
            self._script_type = None

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data
        if self._script_type is not None:
            self._script_buf.append(data)


def parse(name: str) -> PageParser:
    parser = PageParser()
    parser.feed((ROOT / name).read_text(encoding="utf-8"))
    parser.close()
    return parser


def catalog() -> list[dict]:
    return json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))


def png_size(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError(f"{path.name} is not a PNG")
    return struct.unpack(">II", header[16:24])


def local_path(ref: str) -> Path | None:
    """Map a reference in the repo to a file on disk, or None when not local."""
    if not ref or ref.startswith(EXTERNAL) or ref.startswith("#"):
        return None
    path = unquote(urlparse(ref).path)
    if not path:
        return None
    if path.startswith("/intj-growth-guide/"):
        path = path[len("/intj-growth-guide/") :]
    elif path.startswith("/"):
        return None
    return ROOT / path


class MetadataTests(unittest.TestCase):
    def test_titles_are_unique_and_specific(self) -> None:
        titles = [parse(name).title.strip() for name in PAGES]
        for title in titles:
            self.assertGreaterEqual(len(title), 12, title)
            self.assertLessEqual(len(title), 70, title)
        self.assertEqual(len(titles), len(set(titles)))

    def test_description_length(self) -> None:
        for name in PAGES:
            description = parse(name).meta.get("description", "")
            self.assertTrue(60 <= len(description) <= 160, f"{name}: {len(description)} 字")

    def test_canonical_and_social_preview(self) -> None:
        for name in PAGES:
            page = parse(name)
            expected = SITE + ("/" if name == "index.html" else "/" + name)
            canonical = [link.get("href", "") for link in page.links if link.get("rel") == "canonical"]
            self.assertEqual(canonical, [expected], name)
            self.assertEqual(page.meta.get("og:url"), expected, name)
            image = page.meta.get("og:image", "")
            self.assertTrue(image.startswith(SITE) and image.endswith(".png"), name)
            self.assertEqual(page.meta.get("og:image:width"), "1200", name)
            self.assertEqual(page.meta.get("og:image:height"), "630", name)
            self.assertEqual(page.meta.get("twitter:card"), "summary_large_image", name)
            self.assertTrue(page.meta.get("og:title"), name)
            self.assertTrue(page.meta.get("og:description"), name)

    def test_favicons_linked(self) -> None:
        for name in PAGES:
            hrefs = [link.get("href", "") for link in parse(name).links]
            self.assertTrue(any(h.endswith("favicon.svg") for h in hrefs), name)
            self.assertTrue(any(h.endswith("apple-touch-icon.png") for h in hrefs), name)

    def test_structured_data_parses(self) -> None:
        for name in PAGES:
            blocks = [body for kind, body in parse(name).scripts if kind == "application/ld+json"]
            self.assertEqual(len(blocks), 1, name)
            data = json.loads(blocks[0])
            self.assertEqual(data["@context"], "https://schema.org")
            self.assertIn("@type", data)
            self.assertEqual(data["inLanguage"], "zh-CN")

    def test_index_structured_data_covers_catalog(self) -> None:
        blocks = [b for t, b in parse("index.html").scripts if t == "application/ld+json"]
        data = json.loads(blocks[0])
        items = data["mainEntity"]["itemListElement"]
        self.assertEqual(len(items), 41)
        self.assertEqual(data["mainEntity"]["numberOfItems"], 41)
        self.assertEqual([i["name"] for i in items], [w["title"] for w in catalog()])


class AssetTests(unittest.TestCase):
    def test_social_preview_is_1200x630(self) -> None:
        self.assertEqual(png_size(ROOT / "assets/social-preview.png"), (1200, 630))

    def test_apple_touch_icon_is_180(self) -> None:
        self.assertEqual(png_size(ROOT / "assets/apple-touch-icon.png"), (180, 180))

    def test_favicon_32(self) -> None:
        self.assertEqual(png_size(ROOT / "assets/favicon-32.png"), (32, 32))

    def test_svg_sources_exist(self) -> None:
        for name in ("social-preview.svg", "favicon.svg"):
            self.assertTrue((ROOT / "assets" / name).is_file(), name)

    def test_no_orphan_duplicate_templates(self) -> None:
        self.assertFalse((ROOT / "site/plan-template.html").exists())


class LinkTests(unittest.TestCase):
    def test_local_links_resolve(self) -> None:
        missing = []
        for name in PAGES:
            for ref in parse(name).refs:
                target = local_path(ref)
                if target is not None and not target.exists():
                    missing.append(f"{name} -> {ref}")
        self.assertEqual(missing, [])

    def test_in_page_anchors_resolve(self) -> None:
        anchors = {name: parse(name).anchors for name in PAGES}
        broken = []
        for name in PAGES:
            for ref in parse(name).refs:
                if "#" not in ref or ref.startswith(EXTERNAL):
                    continue
                path, _, fragment = ref.partition("#")
                if not fragment:
                    continue
                target = local_path(path) if path else ROOT / name
                if target is None or not target.exists():
                    continue
                page_name = target.name
                if page_name in anchors and fragment not in anchors[page_name]:
                    broken.append(f"{name} -> {ref}")
        self.assertEqual(broken, [])

    def test_article_sections_match_catalog(self) -> None:
        page = parse("article.html")
        expected = [item["id"] for item in catalog()]
        found = re.findall(r'<section class="item" id="([^"]+)"', (ROOT / "article.html").read_text(encoding="utf-8"))
        self.assertEqual(found, expected)
        for item_id in expected:
            self.assertIn(item_id, page.anchors)

    def test_article_lists_every_title(self) -> None:
        html = (ROOT / "article.html").read_text(encoding="utf-8")
        for item in catalog():
            self.assertIn(item["title"], html, item["id"])


class DiscoverabilityTests(unittest.TestCase):
    def test_sitemap_covers_pages(self) -> None:
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        locs = re.findall(r"<loc>([^<]+)</loc>", sitemap)
        self.assertEqual(len(locs), len(set(locs)))
        for name in PAGES:
            expected = SITE + ("/" if name == "index.html" else "/" + name)
            self.assertIn(expected, locs)
        for loc in locs:
            self.assertTrue(loc.startswith(SITE + "/"), loc)

    def test_sitemap_lastmod_is_iso_date(self) -> None:
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        for value in re.findall(r"<lastmod>([^<]+)</lastmod>", sitemap):
            self.assertRegex(value, r"^\d{4}-\d{2}-\d{2}$")

    def test_robots_points_to_sitemap(self) -> None:
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("Sitemap: " + SITE + "/sitemap.xml", robots)
        self.assertIn("Allow: /", robots)

    def test_404_page(self) -> None:
        page = parse("404.html")
        self.assertIn("noindex", page.meta.get("robots", ""))
        self.assertIn("/intj-growth-guide/", (ROOT / "404.html").read_text(encoding="utf-8"))

    def test_no_unbuilt_markers(self) -> None:
        for name in PAGES:
            html = (ROOT / name).read_text(encoding="utf-8")
            self.assertNotIn("/*__", html, name)


class RepositoryDocTests(unittest.TestCase):
    def test_readme_points_to_live_site(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(SITE + "/", readme)
        self.assertNotIn("](index.html)", readme)
        self.assertNotIn("](article.html)", readme)
        self.assertNotIn("](plan.html)", readme)

    def test_start_here_points_to_live_site(self) -> None:
        start = (ROOT / "START-HERE.md").read_text(encoding="utf-8")
        self.assertNotIn("](index.html)", start)
        self.assertNotIn("](plan.html)", start)

    def test_markdown_never_links_to_raw_html(self) -> None:
        """GitHub renders .md links to .html as raw source; point at the live site instead."""
        offenders = []
        for path in ROOT.rglob("*.md"):
            if ".git" in path.parts:
                continue
            for ref in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                target = ref.split("#")[0]
                if target.endswith(".html") and not target.startswith(EXTERNAL):
                    offenders.append(f"{path.relative_to(ROOT)} -> {ref}")
        self.assertEqual(offenders, [])

    def test_community_files_exist(self) -> None:
        for name in (
            ".github/PULL_REQUEST_TEMPLATE.md",
            ".github/ISSUE_TEMPLATE/config.yml",
            ".github/ISSUE_TEMPLATE/suggest-work.yml",
            ".github/ISSUE_TEMPLATE/fix-content.yml",
            "CONTRIBUTING.md",
            "LICENSE",
            ".editorconfig",
        ):
            self.assertTrue((ROOT / name).is_file(), name)

    def test_workflows_validate_before_deploy(self) -> None:
        deploy = (ROOT / ".github/workflows/deploy-pages.yml").read_text(encoding="utf-8")
        self.assertIn("needs:", deploy)
        self.assertIn("scripts/build.py --check", deploy)
        self.assertIn("unittest", deploy)


if __name__ == "__main__":
    unittest.main()
