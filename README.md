# 🟩 Daily Build Automation

> Auto-picks a project idea from a curated bank, scaffolds it, and commits to GitHub **every day at 9:00 AM IST** — keeping your contribution calendar permanently green.

---

## ⚙️ How It Works

```
[GitHub Actions Cron: 9AM IST]
        ↓
[daily_builder.py runs]
        ↓
[Picks unused idea from IDEA_BANK (30 ideas)]
        ↓
[Generates: main.py + README + requirements.txt]
        ↓
[Commits to projects/YYYY-MM-DD-{name}/]
        ↓
[🟩 Green square on your calendar]
```

---

## 📅 Schedule

- **Automatic:** Every day at 9:00 AM IST (03:30 UTC)
- **Manual:** Go to Actions tab → `Daily Build & Commit` → `Run workflow`

---

## 🔐 Required GitHub Secrets

Go to: `Settings → Secrets and variables → Actions → New repository secret`

| Secret | Value |
|---|---|
| `NOTION_TOKEN` | Your Notion Integration Token |
| `NOTION_IDEAS_PAGE_ID` | `1e1987cd0de880f28581fa5f347c2a93` |

> **Note:** Even without secrets, the pipeline works using the built-in 30-idea bank.

---

## 📦 Project Bank (30 ideas pre-loaded)

Includes ideas across:
- 📊 Financial tools (expense tracker, trading journal, invoice generator)
- 🤖 AI tools (flashcard generator, news summarizer, commit message writer)
- 🛠️ DevOps utilities (uptime checker, secret scanner, API monitor)
- 💼 Career tools (ATS scorer, Naukri scraper, LinkedIn scheduler)
- 📈 Trading tools (Pine Script backtester, crypto alert, stock tracker)

---

## 🗡️ Manual Trigger

1. Go to [Actions tab](https://github.com/aadi4frnzzz-crypto/daily-build-automation/actions)
2. Click `🟩 Daily Build & Commit`
3. Click `Run workflow` → `Run workflow`
4. Watch it commit in ~30 seconds

---

## 📊 Build Log

See [BUILD_LOG.md](./BUILD_LOG.md) for all projects built.

---

*Built by [aadi4frnzzz-crypto](https://github.com/aadi4frnzzz-crypto) | Notion → GitHub pipeline*
