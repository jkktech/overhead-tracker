#!/usr/bin/env bash
# Usage: ./release.sh   -> stamps a new version into index.html + version.json, commits and pushes.
set -euo pipefail
cd "$(dirname "$0")"
V="$(date +%Y.%m.%d.%H%M)"
sed -i "s/^var APP_VERSION='[^']*'/var APP_VERSION='$V'/" index.html
printf '{"version":"%s"}\n' "$V" > version.json
git add index.html version.json
git commit -m "Release $V"
git push
echo "Released $V - the Echo will pick it up within ~30-40 minutes."
