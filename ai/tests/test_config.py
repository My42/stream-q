"""Unit tests for configuration utilities."""

import pytest
import os
from unittest.mock import patch
from utils.config import get_config


class TestGetConfig:
    """Test configuration loading from environment variables."""

    def test_get_config_with_defaults(self):
        """Test get_config returns defaults when env vars are not set."""
        with patch.dict(os.environ, {}, clear=True):
            config = get_config()

            assert config["confidence_threshold"] == 0.7
            assert config["twitch_bot_token"] == ""
            assert config["twitch_bot_username"] == ""
            assert config["twitch_channel"] == ""
            assert config["cooldown_seconds"] == 30
            assert config["max_messages_per_minute"] == 5

    def test_get_config_with_env_vars(self):
        """Test get_config loads values from environment variables."""
        env_vars = {
            "CONFIDENCE_THRESHOLD": "0.85",
            "TWITCH_BOT_TOKEN": "oauth:test_token_12345",
            "TWITCH_BOT_USERNAME": "test_bot",
            "TWITCH_CHANNEL": "test_channel",
            "COOLDOWN_SECONDS": "60",
            "MAX_MESSAGES_PER_MINUTE": "10",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = get_config()

            assert config["confidence_threshold"] == 0.85
            assert config["twitch_bot_token"] == "oauth:test_token_12345"
            assert config["twitch_bot_username"] == "test_bot"
            assert config["twitch_channel"] == "test_channel"
            assert config["cooldown_seconds"] == 60
            assert config["max_messages_per_minute"] == 10

    def test_get_config_partial_env_vars(self):
        """Test get_config with some env vars set and some using defaults."""
        env_vars = {
            "TWITCH_BOT_TOKEN": "oauth:partial_token",
            "CONFIDENCE_THRESHOLD": "0.75",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = get_config()

            # Set values
            assert config["confidence_threshold"] == 0.75
            assert config["twitch_bot_token"] == "oauth:partial_token"

            # Default values
            assert config["twitch_bot_username"] == ""
            assert config["twitch_channel"] == ""
            assert config["cooldown_seconds"] == 30
            assert config["max_messages_per_minute"] == 5

    def test_confidence_threshold_as_float(self):
        """Test confidence threshold is properly converted to float."""
        env_vars = {
            "CONFIDENCE_THRESHOLD": "0.9",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = get_config()

            assert isinstance(config["confidence_threshold"], float)
            assert config["confidence_threshold"] == 0.9

    def test_cooldown_seconds_as_int(self):
        """Test cooldown_seconds is properly converted to int."""
        env_vars = {
            "COOLDOWN_SECONDS": "45",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = get_config()

            assert isinstance(config["cooldown_seconds"], int)
            assert config["cooldown_seconds"] == 45

    def test_max_messages_per_minute_as_int(self):
        """Test max_messages_per_minute is properly converted to int."""
        env_vars = {
            "MAX_MESSAGES_PER_MINUTE": "15",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = get_config()

            assert isinstance(config["max_messages_per_minute"], int)
            assert config["max_messages_per_minute"] == 15

    def test_config_returns_dict(self):
        """Test that get_config returns a dictionary."""
        config = get_config()

        assert isinstance(config, dict)
        assert len(config) == 6

        # Verify all expected keys are present
        expected_keys = {
            "confidence_threshold",
            "twitch_bot_token",
            "twitch_bot_username",
            "twitch_channel",
            "cooldown_seconds",
            "max_messages_per_minute",
        }
        assert set(config.keys()) == expected_keys

    def test_multiple_channels(self):
        """Test configuration with multiple channels (comma-separated)."""
        env_vars = {
            "TWITCH_CHANNEL": "channel1,channel2,channel3",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = get_config()

            # Channel is returned as-is (parsing happens in bot logic)
            assert config["twitch_channel"] == "channel1,channel2,channel3"

    def test_empty_string_env_vars(self):
        """Test behavior with explicitly empty environment variables."""
        env_vars = {
            "TWITCH_BOT_TOKEN": "",
            "TWITCH_BOT_USERNAME": "",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = get_config()

            assert config["twitch_bot_token"] == ""
            assert config["twitch_bot_username"] == ""


class TestConfigEdgeCases:
    """Test edge cases for configuration."""

    def test_invalid_float_conversion(self):
        """Test behavior when CONFIDENCE_THRESHOLD is not a valid float."""
        env_vars = {
            "CONFIDENCE_THRESHOLD": "not_a_number",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            with pytest.raises(ValueError):
                get_config()

    def test_invalid_int_conversion_cooldown(self):
        """Test behavior when COOLDOWN_SECONDS is not a valid int."""
        env_vars = {
            "COOLDOWN_SECONDS": "not_a_number",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            with pytest.raises(ValueError):
                get_config()

    def test_invalid_int_conversion_max_messages(self):
        """Test behavior when MAX_MESSAGES_PER_MINUTE is not a valid int."""
        env_vars = {
            "MAX_MESSAGES_PER_MINUTE": "not_a_number",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            with pytest.raises(ValueError):
                get_config()

    def test_negative_confidence_threshold(self):
        """Test with negative confidence threshold."""
        env_vars = {
            "CONFIDENCE_THRESHOLD": "-0.5",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = get_config()

            # Should convert but be invalid (validation happens elsewhere)
            assert config["confidence_threshold"] == -0.5

    def test_confidence_threshold_above_one(self):
        """Test with confidence threshold above 1.0."""
        env_vars = {
            "CONFIDENCE_THRESHOLD": "1.5",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = get_config()

            # Should convert but be invalid (validation happens elsewhere)
            assert config["confidence_threshold"] == 1.5

    def test_zero_values(self):
        """Test with zero values for numeric fields."""
        env_vars = {
            "CONFIDENCE_THRESHOLD": "0.0",
            "COOLDOWN_SECONDS": "0",
            "MAX_MESSAGES_PER_MINUTE": "0",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = get_config()

            assert config["confidence_threshold"] == 0.0
            assert config["cooldown_seconds"] == 0
            assert config["max_messages_per_minute"] == 0

    def test_very_large_values(self):
        """Test with very large values."""
        env_vars = {
            "COOLDOWN_SECONDS": "999999",
            "MAX_MESSAGES_PER_MINUTE": "1000000",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = get_config()

            assert config["cooldown_seconds"] == 999999
            assert config["max_messages_per_minute"] == 1000000

    def test_whitespace_in_strings(self):
        """Test that whitespace is preserved in string values."""
        env_vars = {
            "TWITCH_BOT_USERNAME": "  test_bot  ",
            "TWITCH_CHANNEL": " test_channel ",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = get_config()

            # Whitespace is preserved (trimming happens elsewhere if needed)
            assert config["twitch_bot_username"] == "  test_bot  "
            assert config["twitch_channel"] == " test_channel "

    def test_special_characters_in_token(self):
        """Test that special characters in token are preserved."""
        env_vars = {
            "TWITCH_BOT_TOKEN": "oauth:abc123!@#$%^&*()_+-=[]{}|;:',.<>?",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = get_config()

            assert config["twitch_bot_token"] == "oauth:abc123!@#$%^&*()_+-=[]{}|;:',.<>?"
