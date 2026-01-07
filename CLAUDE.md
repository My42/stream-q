# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

StreamQ is a lightweight Twitch chat bot that detects viewer questions and automatically replies using the streamer's own FAQ knowledge base. It uses semantic search (embeddings) and a confidence threshold to avoid wrong answers. The bot runs locally on the streamer's PC with simple FAQ management, anti-spam/cooldowns, and logging for easy iteration.

## Project Status & Roadmap

**Current Status:** MVP of FAQ semantic search is complete. The bot can match questions using embeddings but is not yet connected to Twitch chat.

**Next Milestone:** Twitch integration - Connect bot to Twitch IRC and implement message listening/response functionality.

**Important:** Always read `TODO.md` at the start of each session for the complete task list, current progress, and planned features.

## Development Commands

All Python dependencies are managed with `uv`. The main codebase is in the `ai/` directory.

### Setup
```bash
cd ai
uv sync                    # Install dependencies
cp .env.example .env       # Create environment config
```

### Running
```bash
cd ai
uv run main.py            # Run the bot
uv run python -m stream_q # Run as module
```

### Testing
```bash
cd ai
uv run pytest             # Run all tests
uv run pytest tests/test_faq.py  # Run specific test file
uv run pytest -v          # Verbose output
uv run pytest -k "test_name"     # Run specific test by name
```

### Code Quality
```bash
cd ai
uv run ruff check .       # Lint code
uv run ruff format .      # Format code
```

### Dependencies
```bash
cd ai
uv add <package>          # Add production dependency
uv add --dev <package>    # Add development dependency
uv sync                   # Sync dependencies
```

## Architecture

### Core Components

The bot is structured into three main modules within `src/stream_q/`:

1. **bot/** - Twitch chat integration
   - Connects to Twitch IRC using TwitchIO
   - Listens to chat messages in configured channel(s)
   - Detects questions from viewers
   - Sends automated responses with cooldown/anti-spam controls
   - Handles authentication and connection management

2. **faq/** - FAQ knowledge base and semantic search
   - Stores FAQ entries (question/answer pairs)
   - Generates embeddings for semantic search
   - Matches incoming questions against FAQ database
   - Uses confidence threshold to determine if answer should be sent
   - Supports FAQ CRUD operations

3. **utils/** - Shared utilities
   - Configuration loading from .env
   - Logging setup and management
   - Rate limiting and cooldown mechanisms
   - Common helper functions

### Key Design Patterns

- **Confidence Threshold**: Only responds when semantic similarity exceeds threshold (default: 0.7) to avoid incorrect answers
- **Anti-spam Protection**: Configurable cooldowns and rate limits prevent bot spam
- **Local Execution**: Runs entirely on streamer's machine, no external services required
- **Async/Await**: Uses asyncio for efficient I/O operations with Twitch chat

### Configuration

Environment variables in `ai/.env`:
- `TWITCH_BOT_TOKEN`: OAuth token for bot authentication
- `TWITCH_BOT_USERNAME`: Bot's Twitch username
- `TWITCH_CHANNEL`: Channel(s) to monitor
- `CONFIDENCE_THRESHOLD`: Minimum confidence score (0-1) to send answer
- `COOLDOWN_SECONDS`: Seconds between bot responses
- `MAX_MESSAGES_PER_MINUTE`: Rate limit for bot messages

## License

MIT License - Copyright (c) 2026 Mesquita Vincent
