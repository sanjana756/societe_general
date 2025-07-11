import json
import feedparser
from pathlib import Path

ROOT        = Path(__file__).parent.parent
CONFIG      = ROOT / "config" / "feeds.json"
DATA_DIR    = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "raw_feeds.json"

def load_feed_urls():
    with open(CONFIG, encoding="utf-8") as f:
        return json.load(f).get("feeds", [])

def fetch_all():
    """
    Fetch each feed URL with error handling.
    On failure, logs the error and skips that feed.
    """
    urls    = load_feed_urls()
    entries = []

    for url in urls:
        try:
            parsed = feedparser.parse(url)
            # feedparser marks broken feeds with bozo flag
            if getattr(parsed, "bozo", False):
                raise parsed.bozo_exception or Exception("Unknown feedparser error")

            for e in parsed.entries:
                entries.append({
                    "feed":      url,
                    "title":     e.get("title", ""),
                    "link":      e.get("link", ""),
                    "published": e.get("published", ""),
                    "summary":   e.get("summary", e.get("description", ""))
                })

            print(f"✔️  Fetched {len(parsed.entries)} items from {url}")

        except Exception as exc:
            print(f"❌ Error fetching {url!r}: {exc}")

    # Persist whatever we got
    DATA_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(entries, out, indent=2, ensure_ascii=False)

    return entries

if __name__ == "__main__":
    all_entries = fetch_all()
    print(f"\nTotal fetched entries: {len(all_entries)} across {len(load_feed_urls())} feeds.")
