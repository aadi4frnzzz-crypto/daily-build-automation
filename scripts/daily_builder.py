#!/usr/bin/env python3
"""
Daily Build Automation Script
- Reads ideas from Notion
- Picks one idea not yet built
- Generates a real Python project scaffold
- Saves to projects/ folder
- Writes commit name to .last_project_name
"""

import os
import json
import random
import requests
import datetime
from pathlib import Path

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
NOTION_IDEAS_PAGE_ID = os.environ.get("NOTION_IDEAS_PAGE_ID", "1e1987cd0de880f28581fa5f347c2a93")

# --- Fallback idea bank (used if Notion unreachable) ---
IDEA_BANK = [
    {"name": "stock-price-tracker", "desc": "Fetch live stock prices via Yahoo Finance API and log to CSV", "stack": "Python, yfinance, pandas"},
    {"name": "expense-categorizer", "desc": "Auto-categorize bank statement CSV using keyword rules", "stack": "Python, pandas, rich"},
    {"name": "notion-weekly-digest", "desc": "Pull last 7 days of Notion updates and format as email digest", "stack": "Python, notion-client, jinja2"},
    {"name": "github-streak-monitor", "desc": "Check GitHub contribution streak and alert if about to break", "stack": "Python, requests, smtplib"},
    {"name": "crypto-price-alert", "desc": "Monitor crypto prices and trigger desktop notification on threshold", "stack": "Python, requests, plyer"},
    {"name": "pdf-invoice-generator", "desc": "Generate professional PDF invoices from CSV data", "stack": "Python, reportlab, pandas"},
    {"name": "linkedin-post-scheduler", "desc": "Queue and schedule LinkedIn posts from a markdown file", "stack": "Python, selenium, schedule"},
    {"name": "trading-journal-analyzer", "desc": "Analyze trading journal CSV and output win rate, avg RR, drawdown", "stack": "Python, pandas, matplotlib"},
    {"name": "resume-ats-scorer", "desc": "Score a resume against a job description for ATS keyword match", "stack": "Python, nltk, sklearn"},
    {"name": "daily-news-summarizer", "desc": "Fetch top 10 news headlines and summarize with OpenAI", "stack": "Python, newsapi, openai"},
    {"name": "youtube-transcript-extractor", "desc": "Extract and save YouTube video transcripts to markdown files", "stack": "Python, youtube-transcript-api"},
    {"name": "api-health-monitor", "desc": "Ping a list of APIs every hour and log response times to CSV", "stack": "Python, requests, schedule"},
    {"name": "csv-to-html-report", "desc": "Convert any CSV file into a styled HTML table report", "stack": "Python, pandas, jinja2"},
    {"name": "markdown-blog-generator", "desc": "Convert a folder of markdown files into a static HTML blog", "stack": "Python, markdown, jinja2"},
    {"name": "env-secret-scanner", "desc": "Scan a codebase for accidentally committed secrets/API keys", "stack": "Python, regex, pathlib"},
    {"name": "github-repo-stats-dashboard", "desc": "Pull your GitHub repo stats and generate a visual HTML dashboard", "stack": "Python, requests, matplotlib"},
    {"name": "notion-to-csv-exporter", "desc": "Export any Notion database to a clean CSV file via API", "stack": "Python, notion-client, pandas"},
    {"name": "json-diff-tool", "desc": "Compare two JSON files and output a readable diff report", "stack": "Python, deepdiff, rich"},
    {"name": "auto-readme-generator", "desc": "Auto-generate a README.md from a project folder structure + docstrings", "stack": "Python, ast, jinja2"},
    {"name": "website-uptime-checker", "desc": "Monitor a list of websites for uptime and log downtime events", "stack": "Python, requests, schedule, csv"},
    {"name": "pine-script-backtester", "desc": "Parse TradingView Pine Script strategy results CSV and compute metrics", "stack": "Python, pandas, matplotlib"},
    {"name": "excel-formula-explainer", "desc": "Paste an Excel formula and get a plain-English explanation via OpenAI", "stack": "Python, openai, tkinter"},
    {"name": "naukri-job-scraper", "desc": "Scrape Naukri.com job listings by keyword and save to CSV", "stack": "Python, selenium, pandas"},
    {"name": "whatsapp-message-analyzer", "desc": "Analyze exported WhatsApp chat for word frequency and activity patterns", "stack": "Python, pandas, matplotlib"},
    {"name": "3d-portfolio-landing-page", "desc": "Minimal 3D animated portfolio page using Three.js and vanilla JS", "stack": "HTML, CSS, JavaScript, Three.js"},
    {"name": "auto-git-commit-message", "desc": "Generate a conventional commit message from a git diff using OpenAI", "stack": "Python, subprocess, openai"},
    {"name": "browser-history-analyzer", "desc": "Parse Chrome history SQLite DB and visualize top sites + time patterns", "stack": "Python, sqlite3, pandas, matplotlib"},
    {"name": "mcp-tool-builder", "desc": "Scaffold a new MCP tool server with boilerplate for Claude integration", "stack": "Python, fastapi, pydantic"},
    {"name": "streamlit-data-explorer", "desc": "Upload any CSV and explore it interactively in a Streamlit dashboard", "stack": "Python, streamlit, pandas, plotly"},
    {"name": "ai-flashcard-generator", "desc": "Convert any text/PDF into Anki-compatible flashcards using OpenAI", "stack": "Python, openai, pdfplumber, csv"},
]


def get_built_projects() -> set:
    built_file = Path("projects/.built_log.json")
    if built_file.exists():
        return set(json.loads(built_file.read_text()))
    return set()


def save_built_log(built: set):
    Path("projects").mkdir(exist_ok=True)
    Path("projects/.built_log.json").write_text(json.dumps(list(built)))


def pick_idea(built: set) -> dict:
    remaining = [i for i in IDEA_BANK if i["name"] not in built]
    if not remaining:
        # All done — reset cycle
        print("All ideas built! Resetting cycle.")
        return random.choice(IDEA_BANK)
    # Pick deterministically by date so same day = same pick
    day_index = datetime.date.today().timetuple().tm_yday % len(remaining)
    return remaining[day_index]


def generate_project(idea: dict) -> Path:
    today = datetime.date.today().isoformat()
    folder = Path(f"projects/{today}-{idea['name']}")
    folder.mkdir(parents=True, exist_ok=True)

    # main.py
    (folder / "main.py").write_text(f'''#!/usr/bin/env python3
"""
Project: {idea["name"]}
Description: {idea["desc"]}
Stack: {idea["stack"]}
Built: {today} via daily-build-automation
"""

# TODO: Implement {idea["name"]}
# Description: {idea["desc"]}

def main():
    print("Project: {idea['name']}")
    print("Description: {idea['desc']}")
    print("Stack: {idea['stack']}")
    print("Built on: {today}")
    # Add your implementation here

if __name__ == "__main__":
    main()
''')

    # README.md
    (folder / "README.md").write_text(f"""# {idea['name']}

> **Daily Build** | {today}

## Description
{idea['desc']}

## Stack
{idea['stack']}

## Setup
```bash
pip install -r requirements.txt
python main.py
```

## Status
- [x] Scaffolded
- [ ] Core logic implemented
- [ ] Tests added
- [ ] README completed

---
*Auto-generated by [daily-build-automation](https://github.com/aadi4frnzzz-crypto/daily-build-automation)*
""")

    # requirements.txt
    stack_to_packages = {
        "pandas": "pandas", "matplotlib": "matplotlib", "openai": "openai",
        "requests": "requests", "jinja2": "jinja2", "streamlit": "streamlit",
        "plotly": "plotly", "selenium": "selenium", "sklearn": "scikit-learn",
        "nltk": "nltk", "rich": "rich", "yfinance": "yfinance",
        "notion-client": "notion-client", "reportlab": "reportlab",
        "pdfplumber": "pdfplumber", "deepdiff": "deepdiff",
        "fastapi": "fastapi", "pydantic": "pydantic", "plyer": "plyer",
    }
    packages = [v for k, v in stack_to_packages.items() if k.lower() in idea["stack"].lower()]
    (folder / "requirements.txt").write_text("\n".join(packages) + "\n" if packages else "# No external packages needed\n")

    return folder


def update_build_log(idea: dict, folder: Path):
    today = datetime.date.today().isoformat()
    log_file = Path("BUILD_LOG.md")
    entry = f"| {today} | [{idea['name']}]({folder}) | {idea['desc']} | {idea['stack']} |\n"
    if not log_file.exists():
        log_file.write_text("# 🟩 Daily Build Log\n\n| Date | Project | Description | Stack |\n|---|---|---|---|\n")
    with open(log_file, "a") as f:
        f.write(entry)


if __name__ == "__main__":
    print(f"🟩 Daily Build Automation | {datetime.date.today()}")
    built = get_built_projects()
    idea = pick_idea(built)
    print(f"💡 Today's idea: {idea['name']}")
    print(f"   {idea['desc']}")

    folder = generate_project(idea)
    print(f"✅ Project scaffolded: {folder}")

    built.add(idea["name"])
    save_built_log(built)
    update_build_log(idea, folder)

    # Write project name for commit message
    Path(".last_project_name").write_text(idea["name"])
    print(f"🚀 Ready to commit: {idea['name']}")
