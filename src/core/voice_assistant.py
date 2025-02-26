from typing import Optional
import speech_recognition as sr # type: ignore
from kokoro import KPipeline # type: ignore
import numpy as np # type: ignore
import sounddevice as sd # type: ignore
from src.config.config import Config
from src.core.audio_input import AudioInput
from src.core.status_indicator import StatusIndicator
from src.ai.ai_client import GeminiClient, OllamaClient, PerplexityClient

class VoiceAssistant:
    def __init__(self, config: Config):
        self.config = config
        self.audio_input = AudioInput(config)
        
        # Initialize the appropriate AI client based on configuration
        if config.ai_provider == "gemini":
            self.ai_client = GeminiClient(config)
        elif config.ai_provider == "perplexity":
            self.ai_client = PerplexityClient(config)
        else:  # Default to Ollama
            self.ai_client = OllamaClient(config)
            
        self.status = StatusIndicator()
        self.pipeline = KPipeline(lang_code='a')
    
    def process_command(self, command: str) -> bool:
        print(f"\n💭| Command: {command}")
        if self.config.stop_command in command:
            print("\n👋| Goodbye!")
            return False
            
        response = self.ai_client.query(command)
        generator = self.pipeline(
            response, 
            voice=self.config.tts_voice,
            speed=self.config.tts_speed, 
            split_pattern=self.config.tts_split_pattern
        )

        for i, (gs, ps, audio) in enumerate(generator):
            print(f"\n🗣️| Speaking: {gs}")
            if StatusIndicator.gui:
                StatusIndicator.gui.update_response(gs)
            audio_np = audio.numpy() if hasattr(audio, 'numpy') else np.array(audio)
            audio_float = audio_np.astype(np.float32)
            if audio_float.max() > 1 or audio_float.min() < -1:
                audio_float = np.clip(audio_float / self.config.audio_normalize_threshold, -1, 1)
            sd.play(audio_float, self.config.sample_rate)
            sd.wait()
        
        return True

    def handle_wake_word_detection(self, text: str) -> Optional[str]:
        if self.config.wake_word in text:
            self.status.listening_for_command()
            with sr.Microphone() as source:
                audio = self.audio_input.capture_audio(
                    source, 
                    timeout=self.config.command_timeout
                )
                if not audio:
                    return None
                command = self.audio_input.convert_audio_to_text(audio)
                if command:
                    return command
        return None

    def run(self) -> None:
        with sr.Microphone() as source:
            print("\n🎚️| Calibrating for ambient noise...")
            self.audio_input.recognizer.adjust_for_ambient_noise(
                source, 
                duration=self.config.ambient_calibration_duration
            )
            self.status.waiting_for_wake_word()
            
            while True:
                try:
                    audio = self.audio_input.capture_audio(
                        source, 
                        timeout=self.config.main_loop_timeout
                    ) 
                    if not audio:
                        continue
                        
                    text = self.audio_input.convert_audio_to_text(audio)
                    if not text:
                        continue
                        
                    self.status.detected(text)
                    command = self.handle_wake_word_detection(text)
                    if command and not self.process_command(command):
                        break
                    self.status.waiting_for_wake_word()
                except Exception as e:
                    self.status.error(f"Error in main loop: {e}")
                    continue
