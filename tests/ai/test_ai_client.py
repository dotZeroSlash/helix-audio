import pytest
from unittest.mock import patch, Mock
from src.ai.ai_client import OllamaClient, GeminiClient
from src.config.config import Config

@pytest.fixture
def config():
    return Config()

def test_ollama_client_query_success(config):
    client = OllamaClient(config)
    with patch('ollama.chat') as mock_chat:
        mock_chat.return_value = {'message': {'content': 'Test response'}}
        response = client.query("Test prompt")
        assert response == "Test response"
        mock_chat.assert_called_once()

def test_ollama_client_query_retry(config):
    client = OllamaClient(config)
    with patch('ollama.chat') as mock_chat:
        mock_chat.side_effect = [Exception("Error"), {'message': {'content': 'Test response'}}]
        response = client.query("Test prompt")
        assert response == "Test response"
        assert mock_chat.call_count == 2

def test_gemini_client_initialization(config):
    with patch('google.generativeai.configure') as mock_configure, \
         patch('google.generativeai.GenerativeModel') as mock_model:
        client = GeminiClient(config)
        mock_configure.assert_called_once_with(api_key=config.gemini_api_key)
        mock_model.assert_called_once_with(config.gemini_model)

def test_gemini_client_query(config):
    with patch('google.generativeai.configure'), \
         patch('google.generativeai.GenerativeModel') as mock_model:
        mock_chat = Mock()
        mock_response = Mock()
        mock_response.text = "Test response"
        mock_chat.send_message.return_value = mock_response
        mock_model.return_value.start_chat.return_value = mock_chat
        
        client = GeminiClient(config)
        response = client.query("Test prompt")
        assert response == "Test response"