# Contributing to TI Helper Bot

Thanks for your interest in contributing! This bot serves the Tech Immigrants community (53K+ members), so every improvement helps real people.

## Getting Started

### 1. Fork & clone

```bash
gh repo fork TechImmigrants/ti-helper-bot --clone
cd ti-helper-bot
```

### 2. Set up your environment

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Configure

```bash
cp .env.example .env
# Add your own bot token (create a test bot via @BotFather)
```

### 4. Run locally

```bash
cd src
python main.py
```

## Finding Work

- Check [issues labeled `good first issue`](https://github.com/TechImmigrants/ti-helper-bot/labels/good%20first%20issue) for beginner-friendly tasks
- Check [issues labeled `help wanted`](https://github.com/TechImmigrants/ti-helper-bot/labels/help%20wanted) for tasks where we need extra hands
- Feel free to open a new issue if you spot a bug or have a feature idea

## Making Changes

### Branch naming

```
feature/short-description
fix/what-you-fixed
docs/what-you-documented
```

### Commit messages

Keep them clear and concise:
```
Add unit tests for spam checker heuristics
Fix: welcome message not sent when user blocks bot
Update README with Docker instructions
```

### Pull Requests

1. Create a branch from `main`
2. Make your changes
3. Test locally with your own test bot
4. Push and open a PR against `main`
5. Fill in the PR description — what you changed and why
6. A maintainer will review and provide feedback

PRs require 1 approval before merging.

## Code Style

- Python 3.10+
- Use type hints where practical
- Keep functions focused and small
- Add docstrings to public functions
- No hardcoded secrets — everything goes through `.env`

## Testing

```bash
pytest tests/
```

When adding features, add corresponding tests. Mock external APIs (Telegram, Claude) in tests.

## Project Structure

```
src/
├── main.py              # Entry point
├── config.py            # Settings from environment
├── handlers/            # Telegram event handlers
├── services/            # Business logic (spam detection, analytics, etc.)
└── models/              # Database models
```

## Questions?

- Open a GitHub Discussion or Issue
- Ask in the [Telegram group](https://t.me/techimmigrants)

## Code of Conduct

Be respectful. We're all immigrants building something together. Treat contributors the way you'd want to be treated when you were new somewhere.
