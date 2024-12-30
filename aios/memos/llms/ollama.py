from typing import Any, Dict, Optional
import requests
from ..core.config import BaseLlmConfig

class OllamaLLM:
    def __init__(self, config: BaseLlmConfig):
        self.config = config
        self.base_url = "http://localhost:11434"
        
    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.config.model,
                "prompt": prompt,
                "temperature": self.config.temperature,
            }
        )
        return response.json()["response"] 