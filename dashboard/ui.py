import gradio as gr
import json
from pathlib import Path

def load_reports():
    """
    Load parsed_reports.json and return list of dicts.
    """
    data_path = Path(__file__).parent.parent / "data" / "parsed_reports.json"
    if not data_path.exists():
        return []
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_ui():
    """
    Build and return the Gradio UI.
    """
    with gr.Blocks(title="Threat Intel Aggregator") as demo:
        gr.Markdown("# Threat Intelligence Dashboard")

        # Dynamic data load
        REPORTS = load_reports()
        FEEDS   = sorted({r["feed"] for r in REPORTS})

        # Controls
        feed_sel   = gr.Dropdown(choices=["All Feeds"] + FEEDS, value="All Feeds", label="Filter by Feed")
        ioc_input  = gr.Textbox(label="Search IOC", placeholder="e.g., 192.168.1.1 or hash")
        kw_input   = gr.Textbox(label="Keyword Search", placeholder="Search title or summary")
        refresh_btn = gr.Button("Refresh Data")

        # Dataframe for display
        table = gr.Dataframe(
            headers=["Feed", "Title", "Link", "Published", "IOCs", "Summary"],
            interactive=False,
            wrap=True
        )

        def filter_and_search(feed_filter, ioc_query, keyword_query):
            """
            Filter loaded reports by feed, IOC, and keyword.
            """
            data = load_reports()
            if feed_filter and feed_filter != "All Feeds":
                data = [r for r in data if r["feed"] == feed_filter]
            if ioc_query:
                iq = ioc_query.strip().lower()
                data = [r for r in data if any(iq in i.lower() for i in r.get("iocs", []))]
            if keyword_query:
                kw = keyword_query.strip().lower()
                data = [r for r in data if kw in r.get("title", "").lower() or kw in r.get("summary", "").lower()]
            return data

        def update_table(feed, ioc, kw):
            """
            Build table rows as lists of strings for Gradio Dataframe.
            """
            rows = filter_and_search(feed, ioc, kw)
            output = []
            for r in rows:
                output.append([
                    r.get("feed", ""),
                    r.get("title", ""),
                    r.get("link", ""),
                    r.get("published", ""),
                    ", ".join(r.get("iocs", [])),
                    r.get("summary", "").replace("\n", " ")
                ])
            return output

        # Wire up events
        for comp in [feed_sel, ioc_input, kw_input]:
            comp.change(update_table, [feed_sel, ioc_input, kw_input], table)
        refresh_btn.click(update_table, [feed_sel, ioc_input, kw_input], table)

        # Initial load on startup
        demo.load(update_table, [feed_sel, ioc_input, kw_input], table)

    return demo

if __name__ == "__main__":
    ui = build_ui()
    ui.launch()
