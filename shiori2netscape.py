#!/usr/bin/env python3
"""Export a Shiori SQLite database to a Netscape bookmark HTML file for Karakeep import."""
import argparse
import html
import sqlite3
from datetime import datetime, timezone

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("db_path", nargs="?", default="shiori.db")
parser.add_argument("out_path", nargs="?", default="shiori-export.html")
parser.add_argument("--no-tags", action="store_true", help="omit tags from the export")
args = parser.parse_args()

con = sqlite3.connect(f"file:{args.db_path}?mode=ro", uri=True)
rows = con.execute(
    """
    SELECT b.id, b.url, b.title, b.excerpt, b.created_at,
           GROUP_CONCAT(t.name, ',')
    FROM bookmark b
    LEFT JOIN bookmark_tag bt ON bt.bookmark_id = b.id
    LEFT JOIN tag t ON t.id = bt.tag_id
    GROUP BY b.id
    ORDER BY b.id
    """
).fetchall()


def to_epoch(ts):
    try:
        dt = datetime.strptime(ts[:19], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        return str(int(dt.timestamp()))
    except (TypeError, ValueError):
        return ""


esc = lambda s: html.escape(s or "", quote=True)

with open(args.out_path, "w", encoding="utf-8") as f:
    f.write(
        "<!DOCTYPE NETSCAPE-Bookmark-file-1>\n"
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n'
        "<TITLE>Bookmarks</TITLE>\n<H1>Bookmarks</H1>\n<DL><p>\n"
    )
    for _id, url, title, excerpt, created_at, tags in rows:
        attrs = f'HREF="{esc(url)}"'
        if (epoch := to_epoch(created_at)):
            attrs += f' ADD_DATE="{epoch}"'
        if tags and not args.no_tags:
            attrs += f' TAGS="{esc(tags)}"'
        f.write(f"    <DT><A {attrs}>{esc(title or url)}</A>\n")
        if excerpt:
            f.write(f"    <DD>{esc(excerpt)}\n")
    f.write("</DL><p>\n")

print(f"Wrote {len(rows)} bookmarks to {args.out_path}")
