"""Configuration management for StreamQ."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_config() -> dict:
    """Get configuration from environment variables.

    Returns:
        dict: Configuration dictionary with bot settings
    """
    return {
        "confidence_threshold": float(os.getenv("CONFIDENCE_THRESHOLD", "0.7")),
        "twitch_bot_token": os.getenv("TWITCH_BOT_TOKEN", ""),
        "twitch_bot_username": os.getenv("TWITCH_BOT_USERNAME", ""),
        "twitch_channel": os.getenv("TWITCH_CHANNEL", ""),
        "cooldown_seconds": int(os.getenv("COOLDOWN_SECONDS", "30")),
        "max_messages_per_minute": int(os.getenv("MAX_MESSAGES_PER_MINUTE", "5")),
    }
