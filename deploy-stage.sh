#!/bin/sh
# Monta /tmp/stage para o Netlify: arquivos na raiz e em dist/ (o projeto publica "dist").
set -e
cd "$(dirname "$0")"
python3 build.py >/dev/null
rm -rf /tmp/stage && mkdir -p /tmp/stage/dist
cp index.html /tmp/stage/
for f in $(grep -oE '(img|video)/[a-z0-9-]+\.(webp|mp4|webm)' index.html | grep -v kits | sort -u); do
  mkdir -p /tmp/stage/$(dirname $f); cp $f /tmp/stage/$f
done
cp -r /tmp/stage/index.html /tmp/stage/img /tmp/stage/video /tmp/stage/dist/
cat > /tmp/stage/netlify.toml <<'T'
[build]
  publish = "dist"
  command = "echo static"

[[headers]]
  for = "/img/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
[[headers]]
  for = "/video/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
[[headers]]
  for = "/*.html"
  [headers.values]
    Cache-Control = "public, max-age=0, must-revalidate"
T
rm -f /tmp/site.zip && cd /tmp/stage && zip -qr /tmp/site.zip .
ls -la /tmp/site.zip
