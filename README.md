# TIHelperBot — Tech Immigrants Community Bot

A Telegram bot that manages the [Tech Immigrants](https://t.me/techimmigrants) community with automated join approval, spam moderation, analytics, and cross-platform publishing.

## Features

### Phase 1 (Current)
- **Smart join approval** — Automatically assess and approve/decline join requests based on spam signals
- **Anti-spam moderation** — Detect and remove self-promotion, warn/mute/ban repeat offenders
- **AI-assisted detection** — Uses Claude for borderline cases where heuristics aren't enough

### Phase 2 (Planned)
- Community analytics — trending topics, engagement tracking, weekly digests

### Phase 3 (Planned)
- Cross-platform publishing — auto-post channel content to LinkedIn, X, Instagram

## Setup

### 1. Create the bot

Talk to [@BotFather](https://t.me/BotFather) on Telegram:
1. `/newbot`
2. Name: `Tech Immigrants Helper`
3. Username: `TIHelperBot`
4. Copy the token

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your tokens
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add bot to your group

1. Add `@TIHelperBot` to your Telegram group
2. Promote it to admin with permissions:
   - Delete messages
   - Ban users
   - Invite users (for approving join requests)
3. Enable "Approve New Members" in group settings so join requests go through the bot

### 5. Run

```bash
cd src
python main.py
```

## Architecture

```
src/
├── main.py                 # Entry point, handler registration
├── config.py               # Environment & settings
├── handlers/
│   ├── join_requests.py    # Auto-approve/decline logic
│   ├── moderation.py       # Spam detection & enforcement
│   └── admin_commands.py   # /start, /stats, /approve_all
├── services/
│   └── spam_checker.py     # Heuristic + AI spam assessment
└── models/                 # DB models (Phase 2)
```

## Deployment

Designed for serverless (AWS Lambda + webhook) but runs in polling mode for development. See `infra/` for deployment configs (coming soon).

## License

Private — Tech Immigrants internal use.
