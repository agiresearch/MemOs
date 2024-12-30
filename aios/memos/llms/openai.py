from typing import Any, Dict, Optional
import openai
from ..core.config import BaseLlmConfig

class OpenAILLM:
    def __init__(self, config: BaseLlmConfig):
        self.config = config
        if config.api_key:
            openai.api_key = config.api_key
        
    def generate(self, prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model=self.config.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        return response.choices[0].message.content 