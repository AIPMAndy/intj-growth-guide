#!/usr/bin/env python3
"""Build self-contained index.html from editable site sources and the 41-item JSON catalog."""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
def main():
    items = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))
    assert len(items) == 41, f"Expected 41 entries, got {len(items)}"
    tmpl = (ROOT / "site/template.html").read_text(encoding="utf-8")
    css = (ROOT / "site/style.css").read_text(encoding="utf-8")
    js = (ROOT / "site/app.js").read_text(encoding="utf-8")
    for marker in ("/*__STYLE__*/", "/*__CATALOG__*/", "/*__APPLICATION__*/"):
        if marker not in tmpl:
            raise ValueError("Missing build marker: "+marker)
    payload = json.dumps(items, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = tmpl.replace("/*__STYLE__*/", css).replace("/*__CATALOG__*/", payload).replace("/*__APPLICATION__*/", js)
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print(f"Built index.html ({len(items)} items)")
if __name__ == "__main__":
    main()
