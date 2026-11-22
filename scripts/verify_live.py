#!/usr/bin/env python3
"""Verify public GitHub Pages bytes against the checked-out deployment source.

A successful Actions deployment is not treated as public acceptance: each
listed resource must answer HTTP 200 and have exactly the same SHA-256 as main.
"""
from __future__ import annotations

import hashlib
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://aipmandy.github.io/intj-growth-guide/"
FILES = ("index.html", "decision.html", "decision.js", "plan.html",
         "robots.txt", "sitemap.xml", "pdf/intj-growth-guide-guide.pdf")


def verify(path: str) -> None:
    expected = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
    url = BASE + path
    last = ""
    for attempt in range(12):
        try:
            req = urllib.request.Request(
                url, headers={
                    "User-Agent": "INTJ-Atlas-live-verification/1.0",
                    "Accept-Encoding": "identity",
                    "Cache-Control": "no-cache",
                }
            )
            with urllib.request.urlopen(req, timeout=25) as res:
                body = res.read()
                status = res.status
            actual = hashlib.sha256(body).hexdigest()
            if status == 200 and actual == expected:
                print(f"PASS HTTP {status} SHA-256 {actual} {url}", flush=True)
                return
            last = f"HTTP {status}, sha expected={expected}, actual={actual}"
        except (TimeoutError, urllib.error.URLError) as exc:
            last = str(exc)
        if attempt < 11:
            time.sleep(10)
    raise RuntimeError(f"Live resource did not match checked-out source: {url}: {last}")


if __name__ == "__main__":
    for file in FILES:
        verify(file)
    print(f"PASS: {len(FILES)}/{len(FILES)} live public files matched byte-for-byte")
