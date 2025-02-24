import pytest # type: ignore
from unittest.mock import Mock, patch, MagicMock
from src.core.voice_assistant import VoiceAssistant
from src.config.config import Config

@pytest.fixture
def config():
    mock_config = Mock()
    mock_config.use_gemini = False
    mock_config.model_name = "test-model"
    mock_config.stop_command = "stop"  # Add this explicit string value
    return mock_config

@pytest.fixture
def voice_assistant(config):
    with patch('src.core.audio_input.AudioInput') as mock_audio, \
         patch('src.ai.ai_client.OllamaClient') as mock_client, \
         patch('src.core.status_indicator.StatusIndicator') as mock_status, \
         patch('kokoro.KPipeline') as mock_pipeline:
        
        instance = VoiceAssistant(config)
        instance.audio_input = mock_audio
        instance.ai_client = mock_client
        instance.status = mock_status
        instance.pipeline = mock_pipeline
        return instance

def test_voice_assistant_initialization(voice_assistant, config):
    assert voice_assistant.config == config
    assert voice_assistant.audio_input is not None
    assert voice_assistant.ai_client is not None
    assert voice_assistant.status is not None
    assert voice_assistant.pipeline is not None

def test_process_command_stop(voice_assistant):
    result = voice_assistant.process_command("stop")
    assert result is False

def test_process_command_normal(voice_assistant):
    voice_assistant.ai_client.query = MagicMock(return_value="Test response")
    voice_assistant.pipeline = MagicMock()
    result = voice_assistant.process_command("test command")
    assert result is True
    voice_assistant.ai_client.query.assert_called_once_with("test command")

def test_process_command_error(voice_assistant):
    voice_assistant.ai_client.query = MagicMock(side_effect=Exception("Test error"))
    voice_assistant.pipeline = MagicMock()
    try:
        result = voice_assistant.process_command("test command")
        assert result is True
    except Exception as e:
        assert str(e) == "Test error"
