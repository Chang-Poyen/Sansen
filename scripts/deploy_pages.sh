#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
python3 scripts/build_pages.py
if [ ! -x scripts/pages-deps/node_modules/.bin/wrangler ]; then
  npm ci --prefix scripts/pages-deps
fi
exec scripts/pages-deps/node_modules/.bin/wrangler pages deploy dist/pages --project-name sansen-study --branch main
