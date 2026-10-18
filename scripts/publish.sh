#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
repo="AIPMAndy/intj-growth-guide"
if ! command -v git >/dev/null; then echo "Please install git"; exit 1; fi
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then echo "Please git clone https://github.com/$repo first"; exit 1; fi
url="$(git remote get-url origin)"
case "$url" in
  "https://github.com/$repo"|"https://github.com/$repo.git"|"git@github.com:$repo.git") ;;
  *) echo "Refusing to push: origin is $url, expected $repo"; exit 1 ;;
esac
python3 scripts/build.py
python3 -m unittest discover -s tests -v
if [[ -n "$(git status --porcelain)" ]]; then
  echo "Changes detected. Inspect with git status, commit intentionally, then push."
  exit 1
fi
echo "All checks passed. Pushing existing main branch."
git push origin main
echo "GitHub Pages source must be configured in Settings > Pages > Deploy from a branch > main > /(root)."
