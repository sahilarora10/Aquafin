# FinanceBot 💰

A Telegram AI finance advisor that listens like a human — detecting intent,
sensing financial literacy, and adapting its advice accordingly.

## Features
- Intent detection (invest, portfolio review, knowledge, goal planning, tax, market timing)
- Knowledge-level sensing (1–5 literacy scale, updates in real time)
- Confidence tracking — adapts tone to how the user feels, not just what they know
- Persistent memory per user (SQLite)
- Commands: /start, /help, /reset

## Setup

1. Clone this repo
2. Create a virtual environment: `python -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in your keys
5. Run: `python bot.py`

## Environment Variables

| Variable | Description |
|---|---|
| `TELEGRAM_BOT_TOKEN` | From @BotFather on Telegram |
| `ANTHROPIC_API_KEY` | From console.anthropic.com |

## Architecture

User → Telegram → bot.py → advisor.py → Claude API → reply
                                      ↕
                               database.py (SQLite)