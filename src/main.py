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
import requests # type: ignore

def initialize_ai_client(config: Config) -> bool:
    status = StatusIndicator()
    try:
        print(f"\n⚙️| Initializing {config.ai_provider.capitalize()} client...")
        
        if config.ai_provider == "ollama":
            ollama.pull(config.model_name)
            status.ready()
            return True
        elif config.ai_provider == "gemini" and not config.gemini_api_key:
            status.error("Gemini API key not found in config.json")
            return False
        elif config.ai_provider == "perplexity" and not config.perplexity_api_key:
            status.error("Perplexity API key not found in config.json")
            return False
        else:
            # For Gemini and Perplexity with valid API keys
            status.ready()
            return True
            
    except Exception as e:
        status.error(f"Error initializing AI client: {e}")
        print("Please check your configuration and try again.")
        return False

def main() -> int:
    config = Config.load()
    
    # Check for required API keys
    if config.ai_provider == "gemini" and not config.gemini_api_key:
        print("❌| Gemini API key not found in config.json")
        return 1
    elif config.ai_provider == "perplexity" and not config.perplexity_api_key:
        print("❌| Perplexity API key not found in config.json")
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
