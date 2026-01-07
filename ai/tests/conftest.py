"""Shared pytest fixtures and configuration."""

import pytest
import os
from unittest.mock import patch


@pytest.fixture(autouse=True)
def clean_env():
    """Clean environment variables before each test to ensure isolation."""
    # Store original env vars
    original_env = os.environ.copy()

    # Clear specific env vars that might affect tests
    test_env_vars = [
        "CONFIDENCE_THRESHOLD",
        "TWITCH_BOT_TOKEN",
        "TWITCH_BOT_USERNAME",
        "TWITCH_CHANNEL",
        "COOLDOWN_SECONDS",
        "MAX_MESSAGES_PER_MINUTE",
    ]

    for var in test_env_vars:
        os.environ.pop(var, None)

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def mock_env_minimal():
    """Provide minimal environment variables for testing."""
    return {
        "CONFIDENCE_THRESHOLD": "0.7",
        "COOLDOWN_SECONDS": "30",
        "MAX_MESSAGES_PER_MINUTE": "5",
    }


@pytest.fixture
def mock_env_complete():
    """Provide complete environment variables for testing."""
    return {
        "CONFIDENCE_THRESHOLD": "0.75",
        "TWITCH_BOT_TOKEN": "oauth:test_token_123",
        "TWITCH_BOT_USERNAME": "test_bot",
        "TWITCH_CHANNEL": "test_channel",
        "COOLDOWN_SECONDS": "45",
        "MAX_MESSAGES_PER_MINUTE": "8",
    }


@pytest.fixture
def sample_faq_data():
    """Provide sample FAQ data for testing across modules."""
    return [
        {
            "questions": [
                "What is your streaming schedule?",
                "When do you stream?",
                "What time do you go live?",
            ],
            "answer": "I stream Monday, Wednesday, and Friday at 7 PM EST!",
        },
        {
            "questions": [
                "What game are you playing?",
                "What's this game?",
                "What is the name of this game?",
            ],
            "answer": "I'm currently playing Elden Ring!",
        },
        {
            "questions": [
                "What are your PC specs?",
                "What computer do you use?",
                "What's your setup?",
            ],
            "answer": "I use an RTX 4090, AMD Ryzen 9 7950X, and 64GB RAM.",
        },
    ]
