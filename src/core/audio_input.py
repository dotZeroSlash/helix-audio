from typing import Optional
import speech_recognition as sr # type: ignore
from src.config.config import Config
from src.core.status_indicator import StatusIndicator

class AudioInput:
    def __init__(self, config: Config):
        self.config = config
        self.recognizer = sr.Recognizer()
        self.status = StatusIndicator()
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = config.energy_threshold
        self.recognizer.pause_threshold = config.phrase_pause_threshold
        self.recognizer.phrase_threshold = config.phrase_threshold
        
    def capture_audio(self, source: sr.Microphone, timeout: int) -> Optional[sr.AudioData]:
        try:
            self.recognizer.adjust_for_ambient_noise(source, duration=self.config.ambient_duration)
            return self.recognizer.listen(source, 
                                        timeout=timeout,
                                        phrase_time_limit=None)
        except Exception as e:
            self.status.error(f"Error capturing audio: {e}")
            return None

    def convert_audio_to_text(self, audio: sr.AudioData) -> Optional[str]:
        try:
            return self.recognizer.recognize_google(
                audio,
                language=self.config.speech_language,
                show_all=False
            ).lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            self.status.error(f"Speech recognition error: {e}")
            return None
