# main.py

import json
from pathlib import Path
from itertools import groupby

from feeds.fetcher import fetch_all
from parsers.ioc_parser import extract_iocs
from summarizer.summarise import summarize
from alerting.email_alert import send_email_alert

def run_pipeline():
    # 1. Fetch raw feed entries
    raw_entries = fetch_all()

    # 2. Filter #1: keep only the latest N items per feed (e.g., N=10)
    raw_entries.sort(key=lambda e: (e["feed"], e.get("published", "")), reverse=True)
    trimmed = []
    for feed, group in groupby(raw_entries, key=lambda e: e["feed"]):
        trimmed.extend(list(group)[:10])  # keep only first 10 per feed
    raw_entries = trimmed

    # 3. Filter #2: load previously processed reports to skip repeats
    prev_reports = {}
    parsed_path = Path(__file__).parent / "data" / "parsed_reports.json"
    if parsed_path.exists():
        prev_list = json.loads(parsed_path.read_text(encoding="utf-8"))
        prev_reports = {r["link"]: r for r in prev_list}

    processed_reports = []
    seen_hashes = set()

    for entry in raw_entries:
        link = entry.get("link")
        # Skip if already processed
        if link in prev_reports:
            processed_reports.append(prev_reports[link])
            continue

        text = entry.get("summary", "").strip()

        # Filter #3: skip duplicate content by hash
        content_hash = hash(text)
        if content_hash in seen_hashes:
            summary = "🔁 duplicate content—skipped"
        else:
            summary = summarize(text)
            seen_hashes.add(content_hash)

        # Extract IOCs
        iocs = extract_iocs(text)

        # Build report object
        report = {**entry, "iocs": iocs, "summary": summary}
        processed_reports.append(report)

        
         # Send email if a new IOC is detected
        print(f"Extracted IOCs: {iocs}")
        if iocs:
            email_body = f"New IOC detected in the feed '{entry['feed']}':\n\n" + "\n".join(iocs) + f"\n\nSummary:\n{summary}"
            send_email_alert(
                subject="New IOC Detected in Threat Intelligence Feed",
                body=email_body,
                to_email="anjali00878@gmail.com"  # Replace with recipient's email
            )
        else:
            print("No IOCs found, skipping email alert.")

    # 4. Persist enriched reports
    out_dir = Path(__file__).parent / "data"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "parsed_reports.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(processed_reports, f, indent=2, ensure_ascii=False)

    print(f"✅ Pipeline complete — {len(processed_reports)} reports processed.")

if __name__ == "__main__":
    run_pipeline()
