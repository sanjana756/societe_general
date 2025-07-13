import gradio as gr
import json
from pathlib import Path
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np


# Graph creation functions
def create_line_chart(frequency=1):
    # Example data
    x = np.linspace(0, 10, 100)
    y = np.sin(frequency * x)
    
    # Create the Plotly figure
    fig = px.line(x=x, y=y, title=f"Interactive Line Chart (Frequency {frequency})", labels={'x': 'X-Axis', 'y': 'Y-Axis'})
    
    return fig


def create_bar_chart():
    # Example data
    categories = ['A', 'B', 'C', 'D', 'E']
    values = [10, 15, 20, 25, 30]
    
    # Create the Plotly bar chart
    fig = px.bar(x=categories, y=values, title="Interactive Bar Chart", labels={'x': 'Categories', 'y': 'Values'})
    
    return fig


def create_pie_chart():
    # Example data
    labels = ['Critical', 'High', 'Medium', 'Low']
    values = [40, 30, 20, 10]
    
    # Create a Plotly Pie chart
    fig = px.pie(values=values, names=labels, title="Incident Severity Distribution")
    
    return fig


def create_scatter_plot():
    # Example data
    x = np.random.rand(50)
    y = np.random.rand(50)
    
    # Create the Plotly scatter plot
    fig = px.scatter(x=x, y=y, title="Interactive Scatter Plot", labels={'x': 'X-Axis', 'y': 'Y-Axis'})
    
    return fig


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
    Build and return the Gradio UI with a graph section and interactive filters.
    """
    with gr.Blocks(title="Threat Intelligence Dashboard") as demo:
        gr.Markdown(
            """
            # 🚨 Threat Intelligence Aggregator Dashboard
            Welcome to the **Threat Intelligence Aggregator**. Use this dashboard to explore, analyze, and visualize threat data.
            """
        )

        # Dynamic data load
        REPORTS = load_reports()
        FEEDS   = sorted({r["feed"] for r in REPORTS})

        # Controls - make the inputs more stylish and informative
        with gr.Row():
            feed_sel = gr.Dropdown(choices=["All Feeds"] + FEEDS, value="All Feeds", label="Select Feed", interactive=True)
            ioc_input = gr.Textbox(label="Search IOC", placeholder="e.g., 192.168.1.1 or hash", lines=1)
            kw_input = gr.Textbox(label="Search Title/Description", placeholder="Enter keyword to search reports", lines=1)

        refresh_btn = gr.Button("Refresh Data", variant="primary")

        # Graph options with a stylish selection
        graph_option = gr.Radio(choices=["Line Chart", "Bar Chart", "Pie Chart", "Scatter Plot"], label="Select Graph Type", value="Line Chart", interactive=True)

        frequency_slider = gr.Slider(minimum=1, maximum=10, step=0.1, value=1, label="Frequency for Line Chart", interactive=True)

        # Dataframe for display with alternate row coloring
        table = gr.Dataframe(
            headers=["Feed", "Title", "Link", "Published", "IOCs", "Summary"],
            interactive=False,
            wrap=True,
            show_label=False
        )

        # Create the graph output container
        graph_output = gr.Plot()

        # Summary section with a markdown for statistics
        summary_box = gr.Markdown("## Summary: The total number of reports processed and IOCs detected.")

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

        def show_graph(graph_choice, frequency):
            """
            Return the appropriate graph based on user selection.
            """
            if graph_choice == "Line Chart":
                return create_line_chart(frequency)
            elif graph_choice == "Bar Chart":
                return create_bar_chart()
            elif graph_choice == "Pie Chart":
                return create_pie_chart()
            elif graph_choice == "Scatter Plot":
                return create_scatter_plot()

        # Wire up events
        for comp in [feed_sel, ioc_input, kw_input]:
            comp.change(update_table, [feed_sel, ioc_input, kw_input], table)
        refresh_btn.click(update_table, [feed_sel, ioc_input, kw_input], table)

        # Change graph when selecting different graph type
        graph_option.change(show_graph, [graph_option, frequency_slider], graph_output)

        # Initial load on startup
        demo.load(update_table, [feed_sel, ioc_input, kw_input], table)

    return demo


if __name__ == "__main__":
    ui = build_ui()
    ui.launch()
