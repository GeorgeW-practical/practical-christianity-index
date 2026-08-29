# Practical Christianity — Devotional Index

A structured, machine-readable index of the [Practical Christianity](https://practicalchristian.substack.com) devotional archive (George Willeboordse's verse-by-verse Bible studies, published on Substack).

**Why this exists:** Substack gives no control over `robots.txt`, sitemaps, or structured data, and most devotionals are paywalled after a paragraph or two — which makes the archive hard for AI systems (and search engines) to discover and cite accurately. This repo publishes a free, fully public index — title, Scripture passage, and an open one-line summary for every devotional, linking back to the full piece on Substack — so AI tools and search engines have something clean to crawl and cite, while the full studies stay on Substack.

**Live page:** https://georgew-practical.github.io/practical-christianity-index/
(once GitHub Pages is enabled for this repo — see below)

## What's in here

- `data/devotionals.csv` — the source catalogue: one row per devotional (title, passage, Substack URL, one-line teaser, date, free/paid).
- `scripts/build.py` — reads the CSV and generates the four published files below. Re-run it after editing the CSV.
- `index.html` — the actual index page (human-readable, plus embedded schema.org structured data for AI/search crawlers).
- `llms.txt` — a plain-text/Markdown overview of the archive, in the emerging `llms.txt` format some AI tools look for.
- `sitemap.xml`, `robots.txt` — standard crawler discovery files.

## Current status

Seeded with the **10 most recent devotionals** as a working proof of concept — not yet the full archive (1,000+ posts). To fill it out, the fastest path is exporting the full post list from Substack (Settings → Exports) rather than scraping page by page; hand that export over and the catalogue can be rebuilt in one pass.

## Updating

1. Add rows to `data/devotionals.csv` (or replace it with a fuller export-derived version).
2. Run `python3 scripts/build.py` to regenerate `index.html`, `llms.txt`, `sitemap.xml`, and `robots.txt`.
3. Commit and push. GitHub Pages redeploys automatically.

## Enabling GitHub Pages (one-time)

Repo **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main` / `(root)` → Save**.
