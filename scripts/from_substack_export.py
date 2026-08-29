#!/usr/bin/env python3
"""
Convert a Substack posts.csv export into data/devotionals.csv for this repo.

Usage:
    python3 scripts/from_substack_export.py /path/to/posts.csv > data/devotionals.csv

Keeps only published "newsletter" type posts (excludes podcasts, restacks,
and static pages). Extracts a Scripture passage from titles of the form
"Title | Passage" when the right-hand side contains a digit.
"""
import csv
import re
import sys

SUBSTACK_URL = "https://practicalchristian.substack.com"


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "posts.csv"
    with open(src, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    kept = [r for r in rows if r["is_published"] == "true" and r["type"] == "newsletter"]

    out_rows = []
    for r in kept:
        post_id, slug = r["post_id"].split(".", 1)
        url = f"{SUBSTACK_URL}/p/{slug}"
        title = r["title"].strip()
        passage = ""
        if " | " in title:
            left, right = title.split(" | ", 1)
            if re.search(r"\d", right):
                title, passage = left.strip(), right.strip()
        date = r["post_date"][:10] if r["post_date"] else ""
        tier = "paid" if r["audience"] == "only_paid" else "free"
        teaser = r["subtitle"].strip()
        out_rows.append(
            {
                "title": title,
                "passage": passage,
                "url": url,
                "teaser": teaser,
                "date": date,
                "tier": tier,
            }
        )

    # Most recent first
    out_rows.sort(key=lambda r: r["date"], reverse=True)

    writer = csv.DictWriter(
        sys.stdout, fieldnames=["title", "passage", "url", "teaser", "date", "tier"]
    )
    writer.writeheader()
    writer.writerows(out_rows)
    print(f"# {len(out_rows)} rows written", file=sys.stderr)


if __name__ == "__main__":
    main()

