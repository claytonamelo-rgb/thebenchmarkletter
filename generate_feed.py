#!/usr/bin/env python3
"""
Gera um feed RSS 2.0 a partir dos press releases da ICIS, usando a API
REST do WordPress que sustenta https://www.icis.com/explore/press-releases/
(o Inoreader/FetchRSS não conseguem detectar essa fonte automaticamente,
mas o endpoint JSON abaixo é público e estável).

Este script é chamado pelo workflow do GitHub Actions
(.github/workflows/update-feed.yml) a cada hora e escreve o resultado em
docs/icis_press_releases.xml, que é servido pelo GitHub Pages.
"""

import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from email.utils import format_datetime
from xml.sax.saxutils import escape

API_URL = (
    "https://www.icis.com/explore/wp-json/wp/v2/press-releases"
    "?per_page=20&orderby=date&order=desc"
)

FEED_TITLE = "ICIS - Press Releases"
FEED_LINK = "https://www.icis.com/explore/press-releases/"
FEED_DESC = "Press releases e anúncios da ICIS (gerado via API REST do WordPress)."

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "docs", "icis_press_releases.xml")


def fetch_posts(url: str) -> list:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (rss-generator)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def build_rss(posts: list) -> str:
    items_xml = []
    for post in posts:
        title = escape(post["title"]["rendered"])
        link = escape(post["link"])
        guid = escape(post["guid"]["rendered"])
        description = escape(post["excerpt"]["rendered"])
        pub_date = datetime.fromisoformat(post["date"]).replace(tzinfo=timezone.utc)
        pub_date_rfc822 = format_datetime(pub_date)

        items_xml.append(f"""
    <item>
      <title>{title}</title>
      <link>{link}</link>
      <guid isPermaLink="false">{guid}</guid>
      <pubDate>{pub_date_rfc822}</pubDate>
      <description>{description}</description>
    </item>""")

    now_rfc822 = format_datetime(datetime.now(timezone.utc))

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{escape(FEED_TITLE)}</title>
    <link>{escape(FEED_LINK)}</link>
    <description>{escape(FEED_DESC)}</description>
    <lastBuildDate>{now_rfc822}</lastBuildDate>
    {''.join(items_xml)}
  </channel>
</rss>
"""


def main():
    try:
        posts = fetch_posts(API_URL)
    except Exception as exc:
        print(f"Erro ao buscar press releases: {exc}", file=sys.stderr)
        sys.exit(1)

    rss = build_rss(posts)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(rss)

    print(f"Feed escrito em {OUTPUT_PATH} com {len(posts)} itens.")


if __name__ == "__main__":
    main()
