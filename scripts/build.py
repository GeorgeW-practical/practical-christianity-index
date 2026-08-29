#!/usr/bin/env python3
"""
Build the Practical Christianity AI/search index page from data/devotionals.csv.

Usage:
    python3 scripts/build.py

Reads:  data/devotionals.csv
Writes: index.html, sitemap.xml, llms.txt, robots.txt  (repo root)

To add new devotionals: add rows to data/devotionals.csv, then re-run this
script and commit the regenerated files.
"""
import csv
import html
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "data", "devotionals.csv")

SITE_NAME = "Practical Christianity"
SITE_URL = "https://georgew-practical.github.io/practical-christianity-index/"
SUBSTACK_URL = "https://practicalchristian.substack.com"
AUTHOR = "George Willeboordse"
DESCRIPTION = (
    "A structured, machine-readable index of the Practical Christianity "
    "devotional archive: verse-by-verse Bible studies published on Substack, "
    "organized by Scripture passage so AI systems and search engines can "
    "find and cite the right study."
)


def load_rows():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def esc(s):
    return html.escape(s or "", quote=True)


def build_index_html(rows):
    today = date.today().isoformat()

    # JSON-LD: one ItemList of Article entries, for search engines and AI
    # crawlers that parse structured data.
    items_ld = []
    for i, r in enumerate(rows, start=1):
        entry = {
            "@type": "ListItem",
            "position": i,
            "item": {
                "@type": "Article",
                "headline": r["title"],
                "url": r["url"],
                "description": r["teaser"],
                "datePublished": r["date"],
                "author": {"@type": "Person", "name": AUTHOR},
                "isPartOf": {"@type": "Periodical", "name": SITE_NAME, "url": SUBSTACK_URL},
                "isAccessibleForFree": "False" if r["tier"] == "paid" else "True",
            },
        }
        if r.get("passage"):
            entry["item"]["about"] = r["passage"]
        items_ld.append(entry)

    json_ld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"{SITE_NAME} — Devotional Index",
        "description": DESCRIPTION,
        "itemListElement": items_ld,
    }
    import json as _json

    json_ld_str = _json.dumps(json_ld, ensure_ascii=False, indent=2)

    # Group by Old/New Testament book would need a book list; for now group
    # by nothing (chronological) — grouping can be added once the full
    # archive is loaded.
    rows_html = []
    for r in rows:
        tier_label = "Paid" if r["tier"] == "paid" else "Free"
        passage_html = f'<span class="passage">{esc(r["passage"])}</span>' if r.get("passage") else ""
        rows_html.append(
            f"""
      <li class="entry">
        <a class="title" href="{esc(r['url'])}">{esc(r['title'])}</a>
        {passage_html}
        <span class="tier tier-{r['tier']}">{tier_label}</span>
        <p class="teaser">{esc(r['teaser'])}</p>
        <span class="date">{esc(r['date'])}</span>
      </li>"""
        )

    css = """
  :root { color-scheme: light dark; }
  body { font-family: system-ui, -apple-system, Georgia, serif; max-width: 780px; margin: 0 auto; padding: 2rem 1.25rem 4rem; line-height: 1.5; }
  header { margin-bottom: 2rem; }
  h1 { font-size: 1.6rem; margin-bottom: 0.25rem; }
  .sub { color: #666; font-size: 0.95rem; }
  ul.entries { list-style: none; padding: 0; margin: 0; }
  li.entry { padding: 1rem 0; border-bottom: 1px solid #ddd; }
  a.title { font-weight: 600; font-size: 1.05rem; text-decoration: none; }
  a.title:hover { text-decoration: underline; }
  .passage { display: inline-block; margin-left: 0.5rem; font-size: 0.85rem; color: #555; }
  .tier { display: inline-block; margin-left: 0.5rem; font-size: 0.75rem; padding: 0.05rem 0.4rem; border-radius: 3px; border: 1px solid #999; }
  .tier-free { color: #0a7a2f; border-color: #0a7a2f; }
  .tier-paid { color: #8a5b00; border-color: #8a5b00; }
  .teaser { margin: 0.35rem 0 0.15rem; color: #333; }
  .date { font-size: 0.8rem; color: #888; }
  footer { margin-top: 3rem; font-size: 0.85rem; color: #888; }
"""

    body_html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{SITE_NAME} — Devotional Index</title>
<meta name="description" content="{esc(DESCRIPTION)}">
<link rel="canonical" href="{SITE_URL}">
<meta property="og:title" content="{SITE_NAME} — Devotional Index">
<meta property="og:description" content="{esc(DESCRIPTION)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE_URL}">
<style>{css}</style>
<script type="application/ld+json">
{json_ld_str}
</script>
</head>
<body>
<header>
  <h1>{SITE_NAME} — Devotional Index</h1>
  <p class="sub">{esc(DESCRIPTION)}</p>
  <p class="sub">Full publication: <a href="{SUBSTACK_URL}">{SUBSTACK_URL}</a> &middot; Machine-readable overview: <a href="llms.txt">llms.txt</a></p>
</header>
<main>
  <ul class="entries">{''.join(rows_html)}
  </ul>
</main>
<footer>
  <p>Generated {today} from {len(rows)} indexed devotionals. This index currently covers a seed batch of the archive; more entries are added over time. Content on Substack is published by {AUTHOR}.</p>
</footer>
</body>
</html>
"""
    return body_html


def build_llms_txt(rows):
    lines = [
        f"# {SITE_NAME}",
        "",
        f"> {DESCRIPTION}",
        "",
        f"Full publication (Substack): {SUBSTACK_URL}",
        "",
        "## Devotionals",
        "",
    ]
    for r in rows:
        passage = f" ({r['passage']})" if r.get("passage") else ""
        tier = " [paid]" if r["tier"] == "paid" else ""
        lines.append(f"- [{r['title']}]({r['url']}){passage}{tier}: {r['teaser']}")
    lines.append("")
    return "\n".join(lines)


def build_sitemap_xml():
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{SITE_URL}</loc>
    <changefreq>daily</changefreq>
  </url>
</urlset>
"""


def build_robots_txt():
    return f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}sitemap.xml
"""


def main():
    rows = load_rows()
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(build_index_html(rows))
    with open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8") as f:
        f.write(build_llms_txt(rows))
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(build_sitemap_xml())
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(build_robots_txt())
    print(f"Built index.html, llms.txt, sitemap.xml, robots.txt from {len(rows)} rows.")


if __name__ == "__main__":
    main()

