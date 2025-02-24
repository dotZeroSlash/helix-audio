from typing import Optional
from src.gui.voice_assistant_gui import VoiceAssistantGUI

class StatusIndicator:
    """Handles visual status indicators for the voice assistant"""
    gui: Optional[VoiceAssistantGUI] = None
    
    @classmethod
    def initialize_gui(cls) -> None:
        cls.gui = VoiceAssistantGUI()
    
    @staticmethod
    def waiting_for_wake_word() -> None:
        if StatusIndicator.gui:
            StatusIndicator.gui.update_status("Listening for wake word... (say 'helix')", "🔵")
            StatusIndicator.gui.update_detected(None)
    
    @staticmethod
    def listening_for_command() -> None:
        if StatusIndicator.gui:
            StatusIndicator.gui.update_status("Listening for your command... (speak now)", "🟢")
    
    @staticmethod
    def processing() -> None:
        if StatusIndicator.gui:
            StatusIndicator.gui.update_status("Processing...", "⚪")
    
    @staticmethod
    def ready() -> None:
        if StatusIndicator.gui:
            StatusIndicator.gui.update_status("Ready!", "✅")
    
    @staticmethod
    def error(message: str) -> None:
        if StatusIndicator.gui:
            StatusIndicator.gui.update_status(f"Error: {message}", "❌")
    
    @staticmethod
    def detected(text: str) -> None:
        if StatusIndicator.gui:
            StatusIndicator.gui.update_detected(text)