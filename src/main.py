import sys
import json
from typing import Optional
from pathlib import Path
import tkinter as tk
from tkinter import ttk
import threading
from src.config.config import Config
from src.core.status_indicator import StatusIndicator
from src.core.voice_assistant import VoiceAssistant
import ollama # type: ignore

def initialize_ai_client(config: Config) -> bool:
    status = StatusIndicator()
    try:
        print(f"\n⚙️| Initializing {'Gemini' if config.use_gemini else 'Ollama'}...")
        if not config.use_gemini:
            ollama.pull(config.model_name)
        status.ready()
        return True
    except Exception as e:
        status.error(f"Error initializing AI client: {e}")
        print("Please check your configuration and try again.")
        return False

def main() -> int:
    config = Config.load()
    
    if not config.gemini_api_key and config.use_gemini:
        print("❌| Gemini API key not found in config.json")
        return 1
    
    StatusIndicator.initialize_gui()
    
    if not initialize_ai_client(config):
        return 1
    
    assistant = VoiceAssistant(config)
    assistant_thread = threading.Thread(target=assistant.run, daemon=True)
    assistant_thread.start()
    
    try:
        if StatusIndicator.gui:
            StatusIndicator.gui.start()
        return 0
    except KeyboardInterrupt:
        if StatusIndicator.gui:
            StatusIndicator.gui.stop()
        print("\n👋| Stopping...")
        return 0
    except Exception as e:
        StatusIndicator.error(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
