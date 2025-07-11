import json
from pathlib import Path
import feedparser

# Paths
ROOT       = Path(__file__).parent.parent
CONFIG     = ROOT / "config" / "feeds.json"
DATA_DIR   = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "raw_feeds.json"

def load_feed_urls():
    """Load the list of feed URLs from config/feeds.json."""
    with open(CONFIG, encoding="utf-8") as f:
        return json.load(f).get("feeds", [])

def fetch_all():
    """
    Fetch every feed URL, collect entries, and persist to data/raw_feeds.json.
    Returns the list of all entry dicts.
    """
    urls    = load_feed_urls()
    entries = []

    for url in urls:
        parsed = feedparser.parse(url)
        for e in parsed.entries:
            entries.append({
                "feed":      url,
                "title":     e.get("title", ""),
                "link":      e.get("link", ""),
                "published": e.get("published", ""),
                "summary":   e.get("summary", e.get("description", ""))
            })

    # Ensure data directory exists
    DATA_DIR.mkdir(exist_ok=True)
    # Write out raw feeds
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(entries, out, indent=2, ensure_ascii=False)

    return entries

if __name__ == "__main__":
    all_entries = fetch_all()
    print(f"✅ Fetched {len(all_entries)} entries across {len(load_feed_urls())} feeds.")
