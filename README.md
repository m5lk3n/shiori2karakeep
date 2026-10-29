# shiori2karakeep

Migrate bookmarks from [Shiori](https://github.com/go-shiori/shiori) to [Karakeep](https://karakeep.app).

`shiori2netscape.py` reads a Shiori SQLite database and writes a Netscape bookmark HTML file, the standard browser bookmarks format that Karakeep can import.

## Why not `shiori export`?

Shiori has a built-in `shiori export <file>` command that produces the same format, but it sets `ADD_DATE` to the bookmark's *modified* time rather than its *creation* time. This script uses the creation time, so bookmarks keep their original dates in Karakeep.

## What gets exported

For each bookmark:

- URL and title (the URL is used if there is no title)
- creation date, as `ADD_DATE`
- tags, as `TAGS` (can be disabled with `--no-tags`)
- excerpt, as a `<DD>` description line

The database is opened read-only and is never modified.

## Requirements

- Python 3.8 or newer (standard library only)
- A Shiori SQLite database (`shiori.db`)

## Usage

```bash
python3 shiori2netscape.py [--no-tags] [DB_PATH] [OUT_PATH]
```

`DB_PATH` defaults to `shiori.db` and `OUT_PATH` to `shiori-export.html`.

```bash
python3 shiori2netscape.py shiori.db shiori-export.html
python3 shiori2netscape.py --no-tags shiori.db shiori-export.html
```

### With make

```bash
make                  # list available targets
make export           # export with tags
make export-no-tags   # export without tags
make clean            # remove the export file
```

Override the defaults with variables, e.g. `make export DB=path/to/shiori.db OUT=bookmarks.html PYTHON=python3.12`.

## Importing into Karakeep

1. Log in to your Karakeep instance and go to **User Settings → Import / Export**.
2. Choose **Import Bookmarks from HTML file** and upload the generated file.
3. Karakeep creates the bookmarks and tags, then crawls each URL in the background to fetch content, screenshots and AI tags. Large imports can take a while.

Consider importing a small sample first to check that tags and dates come through the way you want.

## Limitations

- **Saved content is not migrated.** Shiori's stored article text, offline archives and thumbnails stay behind. Karakeep fetches every page again, so pages that have since gone offline will be imported as bare links.
- **Public/private status and author are dropped.** Karakeep has no equivalent for either.
- **Time zones.** Shiori stores timestamps without a time zone; they are treated as UTC, so times may be off by your UTC offset.
