from dataclasses import dataclass
import json
from pathlib import Path

@dataclass(frozen=True)
class Config:
    """Configuration settings for the voice assistant"""
    # Wake word and basic settings
    wake_word: str = "helix"
    model_name: str = "llama3.2:latest"
    stop_command: str = "stop"
    use_gemini: bool = True
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash-lite-preview-02-05"

    # Timeouts and durations
    command_timeout: int = 15
    wake_word_timeout: int = 5
    ambient_duration: int = 1
    phrase_pause_threshold: float = 1.5
    phrase_threshold: float = 0.3
    command_listen_timeout: int = 5
    main_loop_timeout: int = 30
    ambient_calibration_duration: int = 2

    # Audio processing settings
    energy_threshold: int = 4000
    sample_rate: int = 24000
    max_retries: int = 3
    audio_normalize_threshold: float = 32768.0

    # Speech recognition settings
    speech_language: str = "en-US"
    
    # TTS settings
    tts_voice: str = 'af_bella'
    tts_speed: float = 1.1
    tts_split_pattern: str = r'[\n\.]+'

    # System prompts
    system_prompt: str = """You are a concise Helix editor assistant. Provide brief, direct answers focusing on:
- Keybindings (1-2 line responses)
- Quick command reference
- Short configuration snippets
- Core features in bullet points
- Specifically windows-specific information
Avoid lengthy explanations. If asked about non-Helix topics, redirect briefly to Helix-specific information. Format responses in short, scannable bullet points when possible."""

    @staticmethod
    def load():
        try:
            with open('config.json') as f:
                config_data = json.load(f)
                return Config(gemini_api_key=config_data['gemini_api_key'])
        except FileNotFoundError:
            print("⚠️ config.json not found. Please create it with your Gemini API key.")
            return Config()
        except json.JSONDecodeError:
            print("⚠️ Invalid config.json format.")
            return Config()