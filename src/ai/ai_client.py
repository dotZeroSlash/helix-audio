from abc import ABC, abstractmethod
from typing import List, Dict
import google.generativeai as genai # type: ignore
import ollama # type: ignore
from src.config.config import Config
from src.core.status_indicator import StatusIndicator

class AIClient(ABC):
    def __init__(self, config: Config):
        self.config = config
        self.status = StatusIndicator()
    
    @abstractmethod
    def query(self, prompt: str) -> str:
        pass

class OllamaClient(AIClient):
    def query(self, prompt: str) -> str:
        self.status.processing()
        for attempt in range(self.config.max_retries):
            try:
                response = ollama.chat(
                    model=self.config.model_name,
                    messages=self.prepare_messages(prompt)
                )
                return response['message']['content']
            except Exception as e:
                if attempt == self.config.max_retries - 1:
                    return f"Error after {self.config.max_retries} attempts: {e}"
                continue
        return "Failed to get response"
    
    def prepare_messages(self, prompt: str) -> List[Dict[str, str]]:
        return [
            {'role': 'system', 'content': self.config.system_prompt},
            {'role': 'user', 'content': prompt}
        ]

class GeminiClient(AIClient):
    def __init__(self, config: Config):
        super().__init__(config)
        genai.configure(api_key=config.gemini_api_key)
        self.model = genai.GenerativeModel(config.gemini_model)
        self.chat = self.model.start_chat(history=[])
        self.chat.send_message(self.config.system_prompt)
    
    def query(self, prompt: str) -> str:
        self.status.processing()
        for attempt in range(self.config.max_retries):
            try:
                response = self.chat.send_message(prompt)
                return response.text
            except Exception as e:
                if attempt == self.config.max_retries - 1:
                    return f"Error after {self.config.max_retries} attempts: {e}"
                continue
        return "Failed to get response"