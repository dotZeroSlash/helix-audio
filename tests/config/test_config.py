import pytest
import json
from pathlib import Path
from unittest.mock import patch
from src.config.config import Config

@pytest.fixture
def mock_config_file(tmp_path):
    config_data = {
        "gemini_api_key": "test_key",
        "wake_word": "test_wake_word"
    }
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config_data))
    return config_file

def test_config_default_values():
    config = Config()
    assert config.wake_word == "helix"
    assert config.model_name == "llama3.2:latest"
    assert config.stop_command == "stop"

def test_config_load(mock_config_file):
    with patch('builtins.open', create=True) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = \
            mock_config_file.read_text()
        config = Config.load()
        assert config.gemini_api_key == "test_key"

def test_config_load_no_file():
    with patch('builtins.open', side_effect=FileNotFoundError()):
        config = Config.load()
        assert config.gemini_api_key == ""
