from abc import ABC, abstractmethod
from typing import List, Dict
import google.generativeai as genai # type: ignore
import ollama # type: ignore
import requests # type: ignore
import json
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

class PerplexityClient(AIClient):
    def __init__(self, config: Config):
        super().__init__(config)
        self.api_key = config.perplexity_api_key
        self.model = config.perplexity_model
        self.api_url = "https://api.perplexity.ai/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.messages = [{"role": "system", "content": config.system_prompt}]
    
    def query(self, prompt: str) -> str:
        self.status.processing()
        self.messages.append({"role": "user", "content": prompt})
        
        for attempt in range(self.config.max_retries):
            try:
                payload = {
                    "model": self.model,
                    "messages": self.messages,
                    "temperature": 0.7,
                    "max_tokens": 1024
                }
                
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    data=json.dumps(payload)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    self.messages.append({"role": "assistant", "content": content})
                    return content
                else:
                    if attempt == self.config.max_retries - 1:
                        return f"Error: API returned status code {response.status_code}"
                    continue
            except Exception as e:
                if attempt == self.config.max_retries - 1:
                    return f"Error after {self.config.max_retries} attempts: {e}"
                continue
        
        return "Failed to get response from Perplexity API"
