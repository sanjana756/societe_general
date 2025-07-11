# 🛡️ Threat Intel Aggregator

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

> **A modular pipeline for aggregating, parsing, and summarizing cybersecurity threat intelligence feeds.**

---

## 🚀 Overview

**Threat Intel Aggregator** is a Python-based framework that fetches threat intelligence from multiple RSS feeds, extracts key indicators (IOCs), summarizes reports using LLMs, and provides a dashboard for interactive exploration. It is designed for security analysts, researchers, and anyone interested in staying ahead of cyber threats.

---

## ✨ Features

- 🔗 **Multi-Feed Aggregation**: Collects data from top threat intelligence sources
- 🧠 **Automated Summarization**: Uses LLMs to generate concise summaries
- 🕵️ **IOC Extraction**: Identifies IPs, URLs, and hashes from reports
- 📊 **Dashboard**: Interactive UI for filtering, searching, and exploring reports
- 🛠️ **Modular Design**: Easy to extend with new feeds, parsers, or summarizers

---

## 📁 Directory Structure

```text
societe_general/
├── config/         # Feed source configuration
│   └── feeds.json
├── dashboard/      # Dashboard UI (Gradio, etc.)
├── data/           # Fetched and processed data
│   └── raw_feeds.json
├── feeds/          # Feed fetching logic
│   └── fetcher.py
├── parsers/        # IOC extraction logic
│   └── ioc_parser.py
├── summarizer/     # Summarization logic
├── requirements.txt
└── ...
```

---

## ⚡ Quickstart

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd societe_general
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # (Repeat in each submodule if needed)
   ```
3. **Fetch threat feeds**
   ```bash
   python feeds/fetcher.py
   ```
4. **Run the pipeline**
   ```bash
   python main.py
   ```
5. **Launch the dashboard**
   ```bash
   # (Assuming dashboard/ui.py is a Gradio app)
   python dashboard/ui.py
   ```

---

## 📝 Usage
- **Configure feeds**: Edit `config/feeds.json` to add or remove sources.
- **Customize parsing**: Extend `parsers/ioc_parser.py` for new IOC types.
- **Summarization**: Uses LLMs (see `summarizer/`).
- **Dashboard**: Filter, search, and explore reports interactively.

---

## 🙏 Credits
- Built with [feedparser](https://pythonhosted.org/feedparser/), [Gradio](https://gradio.app/), and [Groq LLM](https://groq.com/).
- Inspired by the cybersecurity community and open-source threat intelligence.

---

## 📬 Contributing
Pull requests and suggestions are welcome! Please open an issue to discuss your ideas.

---

## 📄 License
This project is licensed under the MIT License. 