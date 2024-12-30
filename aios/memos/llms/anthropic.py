from typing import Any, Dict, Optional
import anthropic
from ..core.config import BaseLlmConfig

class AnthropicLLM:
    def __init__(self, config: BaseLlmConfig):
        self.config = config
        self.client = anthropic.Client(api_key=config.api_key)
        
    def generate(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text 